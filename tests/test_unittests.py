import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.config_checker import *
from lib.poster import *

def test_config():
    assert configCheck(None) == False
    assert configCheck({}) == False
    
    assert os.path.exists('pasty_server.conf')

def test_invalid_deleteFile():
    assert deleteFile('/some/noneexisting/file')

def test_invalid_delete():
    ret = delete('/some/noneexisting/directory', 'file', 'id')
    assert ret or ret == None

def test_invalid_getAllPosts():
    assert getAllPosts('/some/noneexisting/directory')