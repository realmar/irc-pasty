import os, sys, shutil
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime as dt
from werkzeug.datastructures import MultiDict

import web as pasty
from lib.tools import getDisplayMode
from tests.helpers import *

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

    def test_autosave_wrong_method(self):
        rv = self.pastyGetRequestBuilder('/autosave/', self.buildStandardSaveData())
        assert rv.status_code == 405

    def test_autosave_nonexisting(self):
        rv = self.pastyPostRequestBuilder('/autosave/2016/01/01/00/00/00/hjdhgJJH8923hJSDSDS', self.buildStandardSaveData())
        assert rv.status_code == 200

    def test_save(self):
        self.saver('save', 'posts')

    def test_save_wrong_method(self):
        rv = self.pastyGetRequestBuilder('/save/', self.buildStandardSaveData())
        assert rv.status_code == 405

    def test_save_wrong_channel(self):
        std_data = self.buildStandardSaveData()
        std_data['irc_channel'] = '#nonexistingchannel'
        rv = self.pastyPostRequestBuilder('save', std_data)
        assert b'ERROR' in rv.data

    def test_save_nonexisting(self):
        rv = self.pastyPostRequestBuilder('/save/2016/01/01/00/00/00/hjdhgJJH8923hJSDSDS', self.buildStandardSaveData())
        print(rv)
        assert rv.status_code == 400

    def test_get(self):
        self.getter(save_route='/save/', get_route='/get/')

    def test_getautosave(self):
        self.getter(save_route='/autosave/', get_route='/getautosave/')

    def test_get_nonexisting(self):
        rv = self.pastyGetRequestBuilder('/get/2016/01/01/00/00/00/hjdhgJJH8923hJSDSDS')
        assert rv.status_code == 404

    def test_getautosave_nonexisting(self):
        rv = self.pastyGetRequestBuilder('/getautosave/2016/01/01/00/00/00/hjdhgJJH8923hJSDSDS')
        assert rv.status_code == 404

    def test_get_all(self):
        assert self.pastyPostRequestBuilder('save', self.buildStandardSaveData()).status_code == 200
        title = 'hello world'
        assert self.pastyPostRequestBuilder('save', self.buildStandardSaveData(title=title)).status_code == 200
        rv = self.pastyGetRequestBuilder('all')
        assert rv.status_code == 200
        std_data = self.buildStandardSaveData()
        assert std_data.get('title') in decodeUTF8(rv.data)
        assert title in decodeUTF8(rv.data)

        curr_date = dt.today()
        curr_date_str = curr_date.strftime('%Y/%m/%d')

        assert curr_date_str in decodeUTF8(rv.data)

    def test_delete(self):
        rv = self.pastyPostRequestBuilder('save', self.buildStandardSaveData())
        assert rv.status_code == 200
        rv = self.pastyPostRequestBuilder('/delete/' + decodeUTF8(rv.data))
        assert rv.status_code == 200
        assert b'Post deleted' in rv.data

    def test_delete_nonexistent(self):
        rv = self.pastyPostRequestBuilder('/delete/2016/01/01/00/00/00/hjdhgJJH8923hJSDSDS')
        assert rv.status_code == 404

    def test_upload(self):
        rv = self.standardFileUpload()
        assert 'web.py' in decodeUTF8(rv.get('file').data)
        assert os.path.isfile(os.path.join('tests', 'tmp', 'posts', self.buildFileURL(decodeUTF8(rv.get('post').data)), 'web.py'))

    def test_upload_empty(self):
        rvf = self.pastyUpload('/upload/2016/01/01/00/00/00/hjdhgJJH8923hJSDSDS', MultiDict())
        assert rvf.status_code == 400

    def test_multi_upload(self):
        rv = self.pastyPostRequestBuilder('save', self.buildStandardSaveData())
        assert rv.status_code == 200
        rvf = self.pastyUpload('/upload/' + decodeUTF8(rv.data), self.buildStandardFiles(['web.py', 'README.md', 'pasty_server.conf', 'pasty']))
        assert rv.status_code == 200
        assert 'web.py' in decodeUTF8(rvf.data)
        assert 'README.md' in decodeUTF8(rvf.data)
        assert 'pasty_server.conf' in decodeUTF8(rvf.data)
        assert 'pasty' in decodeUTF8(rvf.data)
        assert os.path.isfile(os.path.join('tests', 'tmp', 'posts', self.buildFileURL(decodeUTF8(rv.data)), 'web.py'))
        assert os.path.isfile(os.path.join('tests', 'tmp', 'posts', self.buildFileURL(decodeUTF8(rv.data)), 'README.md'))
        assert os.path.isfile(os.path.join('tests', 'tmp', 'posts', self.buildFileURL(decodeUTF8(rv.data)), 'pasty_server.conf'))
        assert os.path.isfile(os.path.join('tests', 'tmp', 'posts', self.buildFileURL(decodeUTF8(rv.data)), 'pasty'))

    def test_get_file(self):
        rv = self.standardFileUpload()
        file_url = decodeUTF8(rv.get('post').data)
        rv = self.pastyGetRequestBuilder('/getfile/' + self.buildFileURL(file_url) + '/web.py')
        assert rv.status_code == 200
        file = open('web.py', 'rb')
        file_content = file.read()
        file.close()
        assert rv.data == file_content

    def test_delete_file(self):
        rv = self.standardFileUpload()
        file_url = decodeUTF8(rv.get('post').data)
        rvf = self.pastyGetRequestBuilder('/delfile/' + self.buildFileURL(file_url) + '/web.py')
        assert rvf.status_code == 200
        assert not os.path.isfile(os.path.join('tests', 'tmp', 'posts', self.buildFileURL(decodeUTF8(rv.get('post').data)), 'web.py'))
        rvf = self.pastyGetRequestBuilder('/getfile/' + self.buildFileURL(file_url) + '/web.py')
        assert rvf.status_code == 404

    def buildFileURL(self, url):
        id = url.rpartition('/')[2]
        file_url = url.rpartition('/')[0].rpartition('/')[0].rpartition('/')[0].rpartition('/')[0]

        return file_url + '/' + id

    def standardFileUpload(self):
        rv = self.pastyPostRequestBuilder('save', self.buildStandardSaveData())
        assert rv.status_code == 200
        rvf = self.pastyUpload('/upload/' + decodeUTF8(rv.data), self.buildStandardFiles())
        assert rvf.status_code == 200

        return { 'post' : rv, 'file' : rvf }

    def buildStandardFiles(self, files=['web.py']):
        d = MultiDict()
        for file in files:
            d.add('file', open(file, 'rb'))

        return d

    def closeAllFiles(files):
        for file in files.getlist('file'):
            file.close()

    def buildStandardSaveData(self, title='test', content='this is the test content', display_mode='0'):
        return {
            'title' : title,
            'content' : content,
            'display_mode' : display_mode
        }

    def pastyUpload(self, route, files):
        return self.app.post(route, data=files, content_type='multipart/form-data')
        self.closeAllFiles(files)

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

        rv = self.pastyPostRequestBuilder('/' + route + '/' + decodeUTF8(rv.data), self.buildStandardSaveData(title, content, display_mode))

        assert rv.status_code == 200
        checkFile(directory, title, content, display_mode, 'None')

    def getter(self, **kwargs):
        rv = self.pastyPostRequestBuilder(kwargs.get('save_route'), self.buildStandardSaveData())
        assert rv.status_code == 200
        rv = self.pastyGetRequestBuilder(kwargs.get('get_route') + decodeUTF8(rv.data))
        assert rv.status_code == 200
        std_data = self.buildStandardSaveData()
        assert std_data.get('content') in decodeUTF8(rv.data)
        assert 'value="' + std_data.get('title') + '"' in decodeUTF8(rv.data)
