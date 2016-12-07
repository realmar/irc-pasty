"""Handle connection to IRC server."""

from OpenSSL import SSL

from twisted.words.protocols import irc
from twisted.internet import ssl, reactor, protocol

from threading import Thread, Lock
from time import sleep

import re

mutex = Lock()
userlist = {}

class ClientTLSContext(ssl.ClientContextFactory):
    """TLS context creator."""

    isClient = 1

    def getContext(self):
        """Return TLSv1.2 context."""
        return SSL.Context(SSL.TLSv1_2_METHOD)


class IrcBot(irc.IRCClient):
    """IRC Bot."""
    UPDATE_USERLIST_INTERVAL = 2

    def __init__(self, use_tls=False):
        """Constructor, specify tls."""
        self.use_tls = use_tls
        self.timer = None

    def connectionMade(self):
        """On connection made."""
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        """On connection lost."""
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        """On sign on join to channels."""
        for channel in self.factory.channels:
            self.join(channel['name'], channel.get('key'))

    def updateUserlist(self, channel):
        while True:
            self.sendLine('NAMES ' + channel)
            sleep(self.UPDATE_USERLIST_INTERVAL)

    def joined(self, channel):
        t = Thread(target=self.updateUserlist, args=(channel,))
        t.daemon = True
        t.start()

    def lineReceived(self, data):
        names = ''

        for line in data.splitlines():
            if self.username + ' = ' in line:
                names = line
                break

        users = re.sub('[^a-zA-Z\d\s:]', '', names[names.rfind(':') + 1:]).split()
        if len(users) > 0:
            channel = names[names.find('#'):]
            channel = channel.split()[0]

            mutex.acquire()
            userlist[channel] = users
            mutex.release()

        irc.IRCClient.lineReceived(self, data)


class IrcBotFactory(protocol.ClientFactory):
    """IRC Bot Factory."""

    def __init__(self, channels, username, password, use_tls=False):
        """Constructor, assign channels, username, password, tls."""
        self.channels = channels
        self.username = username
        self.use_tls = use_tls
        self.password = password

    def buildProtocol(self, addr):
        """Create IRC Bot instance and configure it."""
        IrcBot.nickname = self.username
        IrcBot.username = self.username

        if self.password is not None or self.password != 'none':
            IrcBot.password = self.password

        self.p = IrcBot(self.use_tls)
        self.p.factory = self
        return self.p

    def clientConnectionLost(self, connector, reason):
        """Reconnect on connection lost."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        """Stop if connection failed."""
        print("connection failed:", reason)
        reactor.stop()


class IRC(Thread):
    """Thread where the IRC client resides."""

    def __init__(self, **kwargs):
        """Constructor of IRC thread."""
        self.server = kwargs.get('server')
        self.port = int(kwargs.get('port'))
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.channels = kwargs.get('channels')
        self.encryption = kwargs.get('encryption')
        self.userlist = {}

        super(IRC, self).__init__()

    def run(self):
        """Create IRC Bot Factory and start the reactor."""
        use_tls = False
        if self.encryption is not None and self.encryption.lower() == 'tls':
            use_tls = True

        self.f = IrcBotFactory(
            self.channels, self.username, self.password, use_tls)

        if use_tls:
            reactor.connectSSL(self.server, self.port,
                               self.f, ClientTLSContext())
        else:
            reactor.connectTCP(self.server, self.port, self.f)

        reactor.run(installSignalHandlers=0)

    def send(self, channel, msg):
        """Send message to IRC server."""
        self.f.p.msg(channel.encode('utf-8'), msg.encode('utf-8'))

    def getUserList(self, channel):
        """Return list of useres in a channel."""
        mutex.acquire()
        users = userlist.get(channel)
        mutex.release()

        if users is None:
            users = []

        return users

    def disconnect(self, *args):
        """Disconnect from IRC server."""
        try:
            self.f.p.quit('Bye.')
            reactor.stop()
        except:
            print("Failed to stop reactor, is it running?")
