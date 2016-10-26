from irc.client import *
from threading import Thread
from time import sleep
import sys

class IRCMessage():
    def __init__(self, channel, msg):
        self.channel = channel
        self.msg = msg

class IRC(Thread, SimpleIRCClient):
    def __init__(self, **kwargs):
        self.server = kwargs.get('server')
        self.port = int(kwargs.get('port'))
        self.username = kwargs.get('username')
        self.targets = kwargs.get('targets')

        Thread.__init__(self)

        # TODO: make this a queue
        self.msg_queue = []
        self.send_messages = True

    def run(self):
        try:
            SimpleIRCClient.__init__(self)
            self.connect(self.server, self.port, self.username)

            while self.send_messages:
                for packet in self.msg_queue:
                    self.connection.privmsg(packet.channel, packet.msg)

                self.msg_queue = []
                if sys.version_info < (3, 0):
                    self.ircobj.process_once(0.2)
                else:
                    self.reactor.process_once(0.2)

        except KeyboardInterrupt as e:
            pass
        finally:
            # teardown
            self.connection.disconnect()

    def on_welcome(self, connection, event):
        for target in self.targets:
            if is_channel(target):
                connection.join(target)

    def send(self, channel, msg):
        self.msg_queue.append(IRCMessage(channel, msg))

    def shutdown(self):
        self.send_messages = False
