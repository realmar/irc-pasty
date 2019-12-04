"""Tests for the pasty irc client."""

from time import sleep
from lib.pasty_irc import IRCRunner, IRC
from tests.mock.irc_mock_server import IRCMockServer


class TestIRC():
    @classmethod
    def setup_class(self):
        self.server = IRCMockServer()
        self.server.start()

        self.irc_client = IRC(
            server='localhost',
            port='6667',
            username='pastybot',
            password=None,
            channels=[{'name' : '#test'},{'name' : '#test2'}],
            encryption=None
        )

        self.irc_runner = IRCRunner()
        self.irc_runner.start()

    @classmethod
    def teardown_class(self):
        self.irc_client.disconnect()
        self.server.close_connection = True

    def setUp(self):
        assert self.irc_runner.isRunning() == True

    def test_01_login_and_join(self):
        sleep(0.5)      # let the client send auth + join

        log = self.server.getLog()

        assert log[0].action == 'NICK'
        assert log[0].nick == 'pastybot'

        assert log[1].action == 'USER'
        assert log[1].nick == 'pastybot'

        assert log[2].action == 'JOIN'
        assert log[2].channel == '#test'

        assert log[3].action == 'JOIN'
        assert log[3].channel == '#test2'

    def test_send_msg(self):
        self.irc_client.send('#test', 'hello world')
        sleep(0.5)      # wait for client to send

        log = self.server.getLog()

        assert log[-1].action == 'PRIVMSG'
        assert log[-1].channel == '#test'
        assert 'hello world' in log[-1].message

    def test_02_userlist(self):
        ul_test = self.irc_client.getUserList('#test')
        ul_test2 = self.irc_client.getUserList('#test2')

        assert len(ul_test) == 2
        assert len(ul_test2) == 2

        assert ul_test[0] == 'pastybot'
        assert ul_test[1] == 'randomdude'

        assert ul_test2[0] == 'pastybot'
        assert ul_test2[1] == 'randomdude'

    def test_03_user_join_leave(self):
        self.server.sendAll(self.server.JOIN.format(nick='perfectionist', channel='#test'))
        sleep(0.5)

        userlist = self.irc_client.getUserList('#test')

        assert len(userlist) == 3
        assert userlist[-1] == 'perfectionist'

        self.server.sendAll(self.server.PART.format(nick='perfectionist', channel='#test'))
        sleep(0.5)

        userlist = self.irc_client.getUserList('#test')

        assert len(userlist) == 2
