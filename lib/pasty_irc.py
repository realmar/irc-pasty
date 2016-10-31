from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

from threading import Thread

class IrcBot(irc.IRCClient):
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)

class IrcBotFactory(protocol.ClientFactory):
    def __init__(self, channels, username):
        self.channels = channels
        self.username = username

    def buildProtocol(self, addr):
        IrcBot.nickname = self.username

        self.p = IrcBot()
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

        super(IRC, self).__init__()
        print("creating instance")

    def run(self):
        self.f = IrcBotFactory(self.channels, self.username)
        reactor.connectTCP(self.server, self.port, self.f)
        reactor.run(installSignalHandlers=0)

    def send(self, channel, msg):
        self.f.p.msg(channel.encode('utf-8'), msg.encode('utf-8'))

    def disconnect(self):
        reactor.stop()
