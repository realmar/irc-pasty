"""Tests for the pasty irc client."""


import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from time import sleep

from lib.pasty_irc import IRC
from tests.mock.irc_mock_server import IRCMockServer

class TestIRC():
    @classmethod
    def setup_class(self):
        self.server = IRCMockServer()
        self.server.start()

    @classmethod
    def teardown_class(self):
        self.server.close_connection = True
        del(self.server)

    @classmethod
    def createIRCClient(self):
        irc_client = IRC(
            server='localhost',
            port='6667',
            username='pastybot',
            password=None,
            channels=[
                {'name' : '#test'},
                {'name' : '#test2'}
            ],
            encryption=None
        )
        irc_client.start()
        
        return irc_client

    def test_login(self):
        self.server.clearLog()
        client = self.createIRCClient()
        
        sleep(1)
        
        log = self.server.getLog()
        
        print(log)
        print(log[-1])
        
        assert log[-1].action == 'USER'
        assert log[-1].nick == 'pastybot'
        
        assert log[-2].action == 'NICK'
        assert log[-2].nick == 'pastybot'