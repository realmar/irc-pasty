"""Mock server to test the psty IRC class.

It actually creates a socket and reponds to specific
requests from the pastybot. Aka provides integration
testablility to the pasty IRC client."""

from threading import Thread, Lock
import socket

mutex = Lock()
server_log = []

class Message(object):
    def __init__(self, message, **kwargs):
        self.message = message
        self.functions = kwargs
    
    def executeFunction(self, name):
        f = self.functions.get(name)
        if f is None:
            return None
        else:
            return f(self.message)

    @property
    def nick(self):
        self.executeFunction('nick')
    
    @property
    def channel(self):
        self.executeFunction('channel')
    
    @property
    def action(self):
        self.executeFunction('action')
    

class IRCMockServer(Thread):
    # Configuration
    HOST = ''
    PORT = 6667
    
    # Responses
    AUTH = ":mock_srv 001 {nick}"
    JOIN = ":{nick}!{nick}@127.0.0.1 JOIN {channel}"
    PART = ":{nick}!{nick}@127.0.0.1 PART {channel}"
    
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
    
    def __del__(self):
        self.conn.close()
    
    def identifyMessage(self, message):
        # NICK
        if 'NICK' in message:
            f = {
                'nick': lambda x: x.split()[1],
                'action': lambda x: x.split()[0]
            }
            return Message(message, **f)

        # USER
        if 'USER' in message:
            f = {
                'nick': lambda x: x.split()[1],
                'action': lambda x: x.split()[0]
            }
            return Message(message, **f)

        # JOIN
        if 'JOIN' in message:
            f = {
                'action': lambda x: x.split()[0],
                'channel': lambda x: x.split()[1]
            }
            return Message(message, **f)

        # PRIVMSG
        if 'PRIVMSG' in message:
            f = {
                'action': lambda x: x.split()[0],
                'channel': lambda x: x.split()[1]
            }
            return Message(message, **f)

        """
        # PART
        
        # currently not implemented by the client
        
        if 'PART' in message:
            f = {
                'nick': lambda x: x.split()[1]
                'action': lambda x: x.split()[0]
            }
            return Message(message, **f)
        """
    
    def run(self):
        # create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.HOST, self.PORT))
        sock.listen(1)
        self.conn, addr = sock.accept()
        
        while True:
            data = self.conn.recv(1024)
            
            for d in data.split('\r\n'):
                m = self.identifyMessage(d)
                self.addLog(m)
                
                print([x.message for x in server_log if x is not None])
                
                if m is None:
                    continue
                
                if m.action == 'USER':
                     self.conn.sendall(self.AUTH)
                
                if m.action == 'JOIN':
                     self.conn.sendall(self.JOIN)
    
    def addLog(self, message):
        mutex.acquire()
        server_log.append(message)
        mutex.release()