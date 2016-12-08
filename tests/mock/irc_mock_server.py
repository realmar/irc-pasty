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
            return ''
        else:
            return f(self.message)

    @property
    def nick(self):
        return self.executeFunction('nick')
    
    @property
    def channel(self):
        return self.executeFunction('channel')
    
    @property
    def action(self):
        return self.executeFunction('action')


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
        self.close_connection = False
    
    def __del__(self):
        try:
            self.conn.close()
        except:
            pass
    
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
        self.conn.settimeout(2)
        
        while True:
            try:
                data = self.conn.recv(1024)
                print('data: ' + data)
            except socket.timeout as e:
                if self.close_connection:
                    break
                else:
                    # we received nothing so we continue
                    # sleep(1)
                    continue
            except socket.error as e:
                print('Socket error: ' + e.args[0])
                break
            except:
                print('Unknown socket error')
                break
            
            for d in data.split('\r\n'):
                m = self.identifyMessage(d)
                self.addLog(m)
                
                mutex.acquire()
                print([x.message for x in server_log if x is not None])
                mutex.release()
                
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
    
    def clearLog(self):
        mutex.acquire()
        server_log = []
        mutex.release()
    
    def getLog(self):
        mutex.acquire()
        l = list(server_log)
        mutex.release()
        
        return l[:-1]