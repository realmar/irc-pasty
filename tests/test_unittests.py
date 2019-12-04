import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib.config_checker import configCheck
from lib.poster import delete, deleteFile, getAllPosts
from lib.tools import sanitize_filename


def test_config():
    assert configCheck(None) is False
    assert configCheck({}) is False

    assert os.path.exists('pasty_server.conf')


def test_invalid_deleteFile():
    assert deleteFile('/some/noneexisting/file')


def test_invalid_delete():
    ret = delete('/some/noneexisting/directory', 'file', 'id')
    assert ret or ret is None


def test_invalid_getAllPosts():
    assert getAllPosts('/some/noneexisting/directory')


def test_sanitize_spaces():
    assert '_n_o_s_p_a_c_e_s_' in sanitize_filename(' n o s p a c e s ')


def test_sanitize_slash():
    assert 'noslashes' in sanitize_filename('/n/o/s/l/a\\s\\h\\e\\s\\')


def test_sanitize_combined():
    assert 'Hello_World' in sanitize_filename('[Hel\\l/o W\\or/ld]')
