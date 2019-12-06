"""Tests for the pasty irc client."""

from time import sleep
from lib.pasty_irc import IRCRunner, IRC
from tests.mock.irc_mock_server import IRCMockServer


class TestIRC():
    irc_server = None
    irc_client = None
    irc_runner = None

    @classmethod
    def setup_class(cls):
        cls.irc_server = IRCMockServer()
        cls.irc_server.start()

        cls.irc_client = IRC(
            server='localhost',
            port='6667',
            username='pastybot',
            password=None,
            channels=[{'name': '#test'}, {'name': '#test2'}],
            encryption=None
        )

        cls.irc_runner = IRCRunner()
        cls.irc_runner.start()

    @classmethod
    def teardown_class(cls):
        cls.irc_client.disconnect()
        cls.irc_server.close_connection = True

    def setUp(self):
        assert TestIRC.irc_runner.isRunning() is True

    def test_01_login_and_join(self):
        sleep(0.5)      # let the client send auth + join

        log = TestIRC.irc_server.getLog()

        assert log[0].action == 'NICK'
        assert log[0].nick == 'pastybot'

        assert log[1].action == 'USER'
        assert log[1].nick == 'pastybot'

        assert log[2].action == 'JOIN'
        assert log[2].channel == '#test'

        assert log[3].action == 'JOIN'
        assert log[3].channel == '#test2'

    # def test_send_msg(self):
    #     sleep(0.2)
    #     TestIRC.irc_client.send('#test', 'hello world')
    #     sleep(0.5)      # wait for client to send

    #     log = TestIRC.irc_server.getLog()

    #     assert log[-1].action == 'PRIVMSG'
    #     assert log[-1].channel == '#test'
    #     assert 'hello world' in log[-1].message

    def test_02_userlist(self):
        ul_test = TestIRC.irc_client.getUserList('#test')
        ul_test2 = TestIRC.irc_client.getUserList('#test2')

        assert len(ul_test) == 2
        assert len(ul_test2) == 2

        assert ul_test[0] == 'pastybot'
        assert ul_test[1] == 'randomdude'

        assert ul_test2[0] == 'pastybot'
        assert ul_test2[1] == 'randomdude'

    def test_03_user_join_leave(self):
        TestIRC.irc_server.sendAll(TestIRC.irc_server.JOIN.format(nick='someone', channel='#test'))
        sleep(0.5)

        userlist = TestIRC.irc_client.getUserList('#test')

        assert len(userlist) == 3
        assert userlist[-1] == 'someone'

        TestIRC.irc_server.sendAll(TestIRC.irc_server.PART.format(nick='someone', channel='#test'))
        sleep(0.5)

        userlist = TestIRC.irc_client.getUserList('#test')

        assert len(userlist) == 2
