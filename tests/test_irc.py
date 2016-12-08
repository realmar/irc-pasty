"""Tests for the pasty irc client."""


import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.pasty_irc import IRC

class TestIRC():
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup(self):
        self.irc_client = IRC(
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

    def teardown(self):
        pass

    def test_dummy(self):
        pass