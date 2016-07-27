#!/usr/bin/env python3

import os, yaml, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib.pasty_irc import IRC
from flask import Flask, render_template, send_from_directory, request, abort
from lib.poster import *
from lib.tools import *
from lib.config_checker import configCheck
from datetime import datetime as dt
CONFIG_FILE = 'pasty_server.conf'
PASTY_ROOT = os.path.dirname(__file__)

conff = open(os.path.join(PASTY_ROOT, CONFIG_FILE))
config = yaml.load(conff)
conff.close()

if not configCheck(config):
    sys.exit(1)

irc_channels = []
for c in config['irc']['channels']:
    if not '#' in c:
        irc_channels.append('#' + c)
    else:
        irc_channels.append(c)

irc_client = IRC(server=config['irc']['server'], port=config['irc']['port'], username=config['irc']['username'])

app = Flask(__name__)

def save(title, content, display_mode, directory, year=None, month=None, day=None, hour=None, minute=None, second=None, id=None, irc_channel=None):
    if content == None or title == None:
        return None

    if irc_channel != None:
        if not irc_channel in irc_channels:
            return "ERROR: Channel not found, aborting ..., post not saved"
        else:
            if not '#' in irc_channel:
                irc_channel = '#' + irc_channel

    if display_mode == None or display_mode == '':
        display_mode = 0

    if year != None and month != None and day != None and hour != None and minute != None and second != None:
        datetime = dt.strptime(str(year) + makeString(month) + makeString(day) + makeString(hour) + makeString(minute) + makeString(second), "%Y%m%d%H%M%S")
    else:
        datetime = None

    url = savePostTopLevel(title, content, display_mode, datetime, id, directory, request.environ.get('REMOTE_USER'))

    if irc_channel != None:
        irc_client.send(irc_channel, os.path.join(config['pasty']['url'], 'get', url))

    return url

@app.route("/", methods=['GET'])
def create():
    return render_template('post.html', view_mode="edit", irc=buildIrcChannelHash(irc_channels), creator=None)

@app.route("/autosave", methods=['POST'], strict_slashes=False)
@app.route("/autosave/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>", methods=['POST'], strict_slashes=False)
def autosave(year=None, month=None, day=None, hour=None, minute=None, second=None, id=None):
    rv = save(request.form.get('title'), request.form.get('content'), request.form.get('display_mode'), os.path.join(PASTY_ROOT, 'autosave'), year, month, day, hour, minute, second, id, None)
    if rv == None:
        abort(400)
    else:
        return rv

@app.route("/save", methods=['POST'], strict_slashes=False)
@app.route("/save/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>", methods=['POST'], strict_slashes=False)
def saveR(year=None, month=None, day=None, hour=None, minute=None, second=None, id=None):
    rv = save(request.form.get('title'), request.form.get('content'), request.form.get('display_mode'), os.path.join(PASTY_ROOT, 'posts'), year, month, day, hour, minute, second, id, request.form.get('irc_channel'))
    if rv == None:
        abort(400)
    else:
        return rv

@app.route("/get/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>")
def get(year, month, day, hour, minute, second, id):
    datetime = dt.strptime(str(year) + makeString(month) + makeString(day) + makeString(hour) + makeString(minute) + makeString(second), "%Y%m%d%H%M%S")
    post = getPost(os.path.join(PASTY_ROOT, 'posts'), datetime, id)
    if post == None:
        abort(404)
    elif type(post) == type(bool()):
        abort(500)
    return render_template('post.html', view_mode="show", post_mode=post['display_mode'], post_id=post['link'], post_content=post['content'], post_title=post['title'], irc=buildIrcChannelHash(irc_channels), creator=post['user'], files=buildFileList(os.path.join(PASTY_ROOT, 'posts', buildDateURL(datetime), id), year, month, day, id))

@app.route("/getautosave/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>")
def getAutoSave(year, month, day, hour, minute, second, id):
    datetime = dt.strptime(str(year) + makeString(month) + makeString(day) + makeString(hour) + makeString(minute) + makeString(second), "%Y%m%d%H%M%S")
    post = getPost(os.path.join(PASTY_ROOT, 'autosave'), datetime, id)
    if post == None:
        abort(404)
    elif type(post) == type(bool()):
        abort(500)

    return render_template('post.html', view_mode="edit", post_mode=post['display_mode'], post_id=post['link'], post_content=post['content'], post_title=post['title'], irc=buildIrcChannelHash(irc_channels), creator=post['user'], files=buildFileList(os.path.join(PASTY_ROOT, 'posts', buildDateURL(datetime), id), year, month, day, id))

@app.route("/all")
def getAll():
    posts = getAllPosts(os.path.join(PASTY_ROOT, 'posts'))
    if type(posts) != type([]):
        abort(500)

    return render_template('all.html', posts=posts)

@app.route("/delete/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>", methods=['POST'], strict_slashes=False)
def deletePost(year, month, day, hour, minute, second, id):
    datetime_string = '/'.join([str(year), makeString(month), makeString(day)])

    rv = delete(os.path.join(PASTY_ROOT, 'posts'), datetime_string, id)
    if rv and type(rv) == type(bool()):
        abort(500)
    elif 'not found' in rv:
        abort(404)
    else:
        return rv

@app.route("/upload/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>", methods=['POST'], strict_slashes=False)
def upload(year, month, day, hour, minute, second, id):
    if 'file' not in request.files:
        abort(400)

    saved_files = []

    directory = os.path.join(PASTY_ROOT, 'posts', '/'.join([str(year), makeString(month), makeString(day)]), id)
    print(directory)
    try: os.makedirs(directory)
    except: pass

    for file_store in request.files.getlist("file"):
        file_store.save(os.path.join(directory, file_store.filename))


    return render_template('files.html', files=buildFileList(directory, year, month, day, id))

@app.route("/getfile/<int:year>/<int:month>/<int:day>/<id>/<filename>", methods=['GET'], strict_slashes=False)
def getFile(year, month, day, id, filename):
    print(os.path.join(PASTY_ROOT, 'posts', str(year), makeString(month), makeString(day), id, filename))
    return send_from_directory(os.path.join(PASTY_ROOT, 'posts', str(year), makeString(month), makeString(day), id), filename)

#
# Error handling
#

@app.errorhandler(400)
def internal_server_error(e):
    return render_template('errors/400.html'), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)
