import irc_mock_server as ims
from time import sleep

srv = ims.IRCMockServer()
srv.start()

block = raw_input('stuff happens')

srv.close_connection = True

print('Waiting for shutdown: (started now)')
sleep(3)