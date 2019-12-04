"""Mock server to test the psty IRC class.

It actually creates a socket and reponds to specific
requests from the pastybot. Aka provides integration
testablility to the pasty IRC client."""

from threading import Thread, Lock, current_thread
import socket
import select

from time import sleep

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
    AUTH = ":mock_srv 001 {nick}\r\n"
    JOIN = ":{nick}!{nick}@127.0.0.1 JOIN {channel}\r\n"
    NAMES = ":mock_srv 353 {nick} = {channel} :{users}\r\n"
    PART = ":{nick}!{nick}@127.0.0.1 PART {channel}\r\n"
    
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.close_connection = False
        self.connections = []
    
    def __del__(self):
        try:
            self.conn.close()
        except Exception:
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
    
    def handleClient(self, conn):
        def closeConnection():
            print('Closing Client connection')
            conn.shutdown(2)
            conn.close()
            self.connections.remove(conn)
        
        while True:
            try:
                data = conn.recv(1024).decode('utf8')
            except socket.timeout:
                if self.close_connection:
                    closeConnection()
                    return
                else:
                    continue
            except socket.error:
                print('Socket error')
                closeConnection()
                return
            except Exception:
                print('Unknown error occured')
                return

            if data.strip() == '':
                closeConnection()
                return

            for d in data.split('\r\n'):
                m = self.identifyMessage(d)
                self.addLog(m)
                
                # mutex.acquire()
                # print([x.message for x in server_log if x is not None])
                # mutex.release()
                
                if m is None:
                    continue
                
                print(m.message)
                
                if m.action == 'USER':
                    print('send auth')
                    conn.send(self.AUTH.format(nick=m.nick).encode('utf8'))

                if m.action == 'JOIN':
                    print('send join')
                    conn.send(self.JOIN.format(nick=m.nick, channel=m.channel).encode('utf8'))
                    conn.send(self.NAMES.format(nick='pastybot', channel=m.channel, users='pastybot randomdude').encode('utf8'))

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.HOST, self.PORT))
        sock.listen(2)
        sock.settimeout(2)
        
        while(True):
            try:
                conn, addr = sock.accept()
                conn.settimeout(2)
                
                self.connections.append(conn)
                
                Thread(target=self.handleClient, args=(conn,)).start()
            except socket.timeout:
                print('No one connected retry')
                if self.close_connection:
                    print('Closing Server connection')
                    sock.close()
                    break
                else:
                    continue
            except socket.error:
                print('Socket error')
                break
            except Exception:
                print('Unknown accept error')
                break
    
    def sendAll(self, message):
        for c in self.connections:
            c.send(message.encode('utf8'))

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
        
        return [x for x in l if x is not None]