from irc.client import SimpleIRCClient, ServerConnectionError

class IRC(SimpleIRCClient):
    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.port = int(kwargs.get('port'))
        self.username = kwargs.get('username')

        super(IRC, self).__init__();

        # self.connect()

    def __del__(self):
        self.disconnect()

    def connect(self):
        try:
            super(IRC, self).connect(self.server, self.port, self.username)
        except ServerConnectionError:
            print('IRC client connection error')

    def disconnect(self):
        try:
            self.connection.quit()
        except:
            print('Failed to disconnect from IRC server')

    # TODO: do not connect and disconnect for every message
    # the reason for this is that the irc client may not send any message
    # if the connect is done in the constructor and the connection is being
    # held open
    def send(self, channel, msg, failcount = 0):
        self.connect()
        try:
            self.connection.privmsg(channel, msg)
        except:
            print('Failed to send message to IRC server')
            if failcount < 4:
                self.send(channel, msg, failcount + 1)
        finally:
            self.disconnect()
