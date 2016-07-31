import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.config_checker import *

def test_config():
    assert configCheck(None) == False
    assert configCheck({}) == False
