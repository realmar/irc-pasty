from OpenSSL import SSL

from twisted.words.protocols import irc
from twisted.internet import ssl, reactor, protocol
from twisted.python import log

from threading import Thread

class ClientTLSContext(ssl.ClientContextFactory):
    isClient = 1
    def getContext(self):
        return SSL.Context(SSL.TLSv1_2_METHOD)

class IrcBot(irc.IRCClient):
    def __init__(self, use_tls = False):
        self.use_tls = use_tls

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel['name'], channel.get('key'))

class IrcBotFactory(protocol.ClientFactory):
    def __init__(self, channels, username, password, use_tls = False):
        self.channels = channels
        self.username = username
        self.use_tls = use_tls
        self.password = password

    def buildProtocol(self, addr):
        IrcBot.nickname = self.username
        IrcBot.username = self.username

        if self.password != None or self.password != 'none':
            IrcBot.password = self.password

        self.p = IrcBot(self.use_tls)
        self.p.factory = self
        return self.p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print("connection failed:", reason)
        reactor.stop()

class IRC(Thread):
    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.port = int(kwargs.get('port'))
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.channels = kwargs.get('channels')
        self.encryption = kwargs.get('encryption')

        super(IRC, self).__init__()

    def run(self):
        use_tls = False
        if self.encryption != None and self.encryption.lower() == 'tls':
            use_tls = True

        self.f = IrcBotFactory(self.channels, self.username, self.password, use_tls)

        if use_tls:
            reactor.connectSSL(self.server, self.port, self.f, ClientTLSContext())
        else:
            reactor.connectTCP(self.server, self.port, self.f)

        reactor.run(installSignalHandlers=0)

    def send(self, channel, msg):
        self.f.p.msg(channel.encode('utf-8'), msg.encode('utf-8'))

    def disconnect(self):
        reactor.stop()
