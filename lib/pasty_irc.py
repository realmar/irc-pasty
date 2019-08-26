"""Handle connection to IRC server."""

import re
from OpenSSL import SSL
from twisted.words.protocols import irc
from twisted.internet import ssl, reactor, protocol
from threading import Thread, Lock

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

    def userJoined(self, user, channel):
        """On user joined the channel event."""
        self.addUser(user, channel)

    def userQuit(self, user, channel):
        """On user quit the irc server event."""
        self.deleteUser(user, channel)

    def userLeft(self, user, channel):
        """On user left channel event."""
        self.deleteUser(user, channel)

    '''
    def joined(self, channel):
        """Send WHO to server if joined a channel."""
        self.sendLine('WHO ' + channel)
    '''

    def addUser(self, user, channel):
        """Add a user threadsave to the userlist."""
        mutex.acquire()
        if userlist.get(channel) is None:
            userlist[channel] = []

        if user not in userlist[channel]:
            userlist[channel].append(user)
        mutex.release()

    def deleteUser(self, user, channel):
        """Remove a user threadsave from the userlist."""
        mutex.acquire()
        if userlist.get(channel) is not None:
            userlist[channel].remove(user)
        mutex.release()

    def lineReceived(self, data):
        """On line received event."""
        names = ''

        for line in data.splitlines():
            """
            # WHO - this is here if the next test fails ..
            try:
                channel = line.split()[3]
            except:
                pass
            else:
                extracted_channels = [x.get('name') for x in self.factory.channels]
                if self.username in line and channel in extracted_channels and 'privmsg' not in line.lower() and 'end' not in line.lower():
                    try:
                        self.addUser(line.split()[7], channel)
                    except:
                        pass
            """

            # NAMES
            if (self.username + ' = ' in line or self.username + ' @ ' in line) and names == '':
                names = line

        users = re.sub(r'[^a-zA-Z\d\s:]', '', names[names.rfind(':') + 1:]).split()
        if len(users) > 0:
            channel = names[names.find('#'):]
            channel = channel.split()[0]

            for u in users:
                self.addUser(u, channel)

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


class IRC():
    def __init__(self, **kwargs):
        """Constructor of IRC thread."""
        self.server = kwargs.get('server')
        self.port = int(kwargs.get('port'))
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.channels = kwargs.get('channels')
        self.encryption = kwargs.get('encryption')
        self.userlist = {}

        for c in self.channels:
            if '#' not in c['name']:
                c['name'] = '#' + c['name']

        self.setup()

    def setup(self):
        """Create IRC Bot Factory and start the reactor."""
        use_tls = False
        if self.encryption is not None and self.encryption.lower() == 'tls':
            use_tls = True

        self.f = IrcBotFactory(
            self.channels, self.username, self.password, use_tls)

        if use_tls:
            self.connection = reactor.connectSSL(self.server, self.port, self.f, ClientTLSContext())
        else:
            self.connection = reactor.connectTCP(self.server, self.port, self.f)

    def send(self, channel, msg):
        """Send message to IRC server."""
        self.f.p.msg(channel.encode('utf-8'), msg.encode('utf-8'))

    def getUserList(self, channel):
        """Return list of users in a channel."""
        mutex.acquire()
        users = userlist.get(channel)
        mutex.release()

        if users is None:
            users = []

        return [x for x in users if x != '']

    def disconnect(self):
        self.f.p.quit('Bye.')
        self.connection.disconnect()


class IRCRunner(Thread):
    """Thread where the IRC client resides."""

    def __init__(self):
        self.irc = irc
        super(IRCRunner, self).__init__()
        self.daemon = True

    def run(self):
        reactor.run(installSignalHandlers=0)

    def stop(self):
        """Disconnect from IRC server."""
        try:
            reactor.stop()
        except:
            print("Failed to stop reactor, is it running?")

    def isRunning(self):
        return reactor.running
