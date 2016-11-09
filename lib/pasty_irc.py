from twisted.words.protocols import irc
from twisted.internet import ssl, reactor, protocol
from twisted.python import log

from threading import Thread

class IrcBot(irc.IRCClient):
    def __init__(self, use_tls = False):
        self.use_tls = use_tls

    def connectionMade(self):
        if self.use_tls:
            self.transport.startTLS(ssl.ClientContextFactory(), self.factory)

        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)

class IrcBotFactory(protocol.ClientFactory):
    def __init__(self, channels, username, use_tls = False):
        self.channels = channels
        self.username = username
        self.use_tls = use_tls

    def buildProtocol(self, addr):
        IrcBot.nickname = self.username

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
        self.channels = kwargs.get('channels')
        self.encryption = kwargs.get('encryption')

        super(IRC, self).__init__()

    def run(self):
        use_tls = False
        if self.encryption.lower() == 'tls':
            use_tls = True

        self.f = IrcBotFactory(self.channels, self.username, use_tls)

        if self.encryption.lower() == 'ssl':
            reactor.connectSSL(self.server, self.port, self.f, ssl.ClientContextFactory())
        elif self.encryption.lower() == 'tls':
            reactor.connectTCP(self.server, self.port, self.f)
        else:
            reactor.connectTCP(self.server, self.port, self.f)

        reactor.run(installSignalHandlers=0)

    def send(self, channel, msg):
        self.f.p.msg(channel.encode('utf-8'), msg.encode('utf-8'))

    def disconnect(self):
        reactor.stop()
