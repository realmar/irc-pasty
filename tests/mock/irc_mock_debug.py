import irc_mock_server as ims

srv = ims.IRCMockServer()
srv.start()

block = input('stuff happens')