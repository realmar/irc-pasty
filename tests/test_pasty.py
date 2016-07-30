import os, sys, shutil
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime as dt

import web as pasty
from lib.tools import getDisplayMode

def checkFile(directory, title, content, display_mode, creator):
    curr_date = dt.today()
    dir = os.path.join('tests', 'tmp', directory, curr_date.strftime('%Y/%m/%d'))
    assert os.path.isdir(dir)
    assert len(os.listdir(dir)) == 1
    filename = os.listdir(dir)[0]
    file = open(os.path.join(dir, filename), 'r')
    file_content = file.read()
    file.close()
    assert content in file_content
    assert title in filename
    assert display_mode in getDisplayMode(filename)
    assert creator in filename.rpartition('-')[2]

class TestPasty():
    def setUp(self):
        pasty.CONFIG_FILE = 'tests/mock/pasty_server.conf'
        pasty.PASTY_ROOT = os.path.join('tests', 'tmp')
        pasty.app.config['TESTING'] = True
        self.app = pasty.app.test_client()

    def tearDown(self):
        try: shutil.rmtree('tests/tmp/autosave')
        except: pass
        try: shutil.rmtree('tests/tmp/posts')
        except: pass

    def test_root(self):
        rv = self.app.get('/')
        assert b'Currently no files saved' in rv.data

    def test_autosave(self):
        self.saver('autosave', 'autosave')

    def test_save(self):
        self.saver('save', 'posts')

    def test_get(self):
        self.getter(save_route='/save/', get_route='/get/')

    def test_getautosave(self):
        self.getter(save_route='/autosave/', get_route='/getautosave/')

    def buildStandardSaveData(self, title='test', content='this is the test content', display_mode='0'):
        return {
            'title' : title,
            'content' : content,
            'display_mode' : display_mode
        }

    def pastyPostRequestBuilder(self, route, data={}):
        return self.app.post(route, data=data)

    def pastyGetRequestBuilder(self, route, data={}):
        return self.app.get(route, data=data)

    def saver(self, route, directory):
        rv = self.pastyPostRequestBuilder('/' + route + '/', self.buildStandardSaveData())

        assert rv.status_code == 200
        std_data = self.buildStandardSaveData()
        checkFile(directory, std_data.get('title'), std_data.get('content'), std_data.get('display_mode'), 'None')

        title = 'testextended'
        content = 'this is the test content extended'
        display_mode = '1'

        rv = self.pastyPostRequestBuilder('/' + route + '/' + rv.data.decode('utf-8'), self.buildStandardSaveData(title, content, display_mode))

        assert rv.status_code == 200
        checkFile(directory, title, content, display_mode, 'None')

    def getter(self, **kwargs):
        rv = self.pastyPostRequestBuilder(kwargs.get('save_route'), self.buildStandardSaveData())
        assert rv.status_code == 200
        rv = self.pastyGetRequestBuilder(kwargs.get('get_route') + rv.data.decode('utf-8'))
        assert rv.status_code == 200
        std_data = self.buildStandardSaveData()
        assert std_data.get('content') in rv.data.decode('utf-8')
        assert 'value="' + std_data.get('title') + '"' in rv.data.decode('utf-8')
