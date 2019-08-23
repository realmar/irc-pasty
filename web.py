#!/usr/bin/env python

"""Entry point of standalone pasty"""

import os
import yaml
import sys
import atexit
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lib.pasty_irc import IRCRunner, IRC
from flask import Flask, render_template, send_from_directory, request, abort
from lib.poster import *
from lib.tools import *
from lib.config_checker import configCheck
from datetime import datetime as dt

CONFIG_FILE = 'pasty_server.conf'
PASTY_ROOT = os.path.dirname(__file__)

irc_channels = []
config = {}


def loadConfig():
    """Load the config file into the memory and return it."""
    conff = open(os.path.join(PASTY_ROOT, CONFIG_FILE))
    config = yaml.safe_load(conff)
    conff.close()

    if not configCheck(config):
        sys.exit(1)

    return config


def setupIRCChannels():
    """Filter and Format channel names of config and return it."""
    irc_channels = []

    for c in config['irc']['channels']:
        if '#' not in c['name']:
            irc_channels.append('#' + c['name'])
        else:
            irc_channels.append(c['name'])

    return irc_channels


config = loadConfig()
irc_channels = setupIRCChannels()

app = Flask(__name__)

def setup():
    global irc_client
    irc_client = IRC(
        server=config['irc']['server'],
        port=config['irc']['port'],
        username=config['irc']['username'],
        password=config['irc'].get('password'),
        channels=config['irc']['channels'],
        encryption=config['irc'].get('encryption'))

    global irc_runner
    irc_runner = IRCRunner()
    irc_runner.start()

    def stopIRC():
        irc_client.disconnect()
        irc_runner.stop()

    atexit.register(stopIRC)


def save(
        title, content, display_mode, directory, year=None, month=None,
        day=None, hour=None, minute=None, second=None, id=None,
        irc_channel=None, sender=None, isPrivMsg=None):
    """Prepare post to be saved on filesystem, calls actual save function."""
    if content is None or title is None:
        return None

    if irc_channel is not None:
        if irc_channel not in irc_channels:
            return "ERROR: Channel not found, aborting ..., post not saved"
        else:
            if '#' not in irc_channel:
                irc_channel = '#' + irc_channel

    if display_mode is None or display_mode == '':
        display_mode = 0

    if year != None and month != None and day != None and hour != None and minute != None and second != None:
        datetime = dt.strptime(
            str(year) + makeString(month) + makeString(day) + makeString(hour) +
            makeString(minute) + makeString(second),
            "%Y%m%d%H%M%S")
    else:
        datetime = None

    if sender is None:
        final_sender = request.environ.get('REMOTE_USER')
    else:
        final_sender = sender

    url = savePostTopLevel(title, content, display_mode, datetime,
                           id, directory, request.environ.get('REMOTE_USER'))

    if irc_channel is not None:
        prestring = ''
        receiver = request.values.get('post_receiver')

        if receiver is not None:
            prestring = receiver + ': '

        if final_sender is not None:
            prestring += final_sender + ' pasted: '

        if(isPrivMsg is not None and receiver is not None):
            irc_channel = receiver

        global irc_client
        irc_client.send(
            irc_channel, prestring + config['pasty']['url'] + '/get/' + url)

    return url


@app.route("/", methods=['GET'])
def create():
    """Return create post view."""
    return render_template('post.html', view_mode="edit",
                           irc=buildIrcChannelHash(irc_channels),
                           creator=None)


@app.route("/autosave", methods=['POST'], strict_slashes=False)
@app.route(
    "/autosave/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>",
    methods=['POST'],
    strict_slashes=False)
def autosave(
        year=None, month=None, day=None, hour=None, minute=None, second=None,
        id=None):
    """Autosave route, delegates to save() function."""
    rv = save(
        request.form.get('title'),
        request.form.get('content').encode('utf-8'),
        request.form.get('display_mode'),
        os.path.join(PASTY_ROOT, 'autosave'),
        year, month, day, hour, minute, second, id, None, None)
    if rv is None:
        abort(400)
    else:
        return rv


@app.route("/save", methods=['POST'], strict_slashes=False)
@app.route(
    "/save/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>",
    methods=['POST'],
    strict_slashes=False)
def saveR(
        year=None, month=None, day=None, hour=None, minute=None, second=None,
        id=None):
    """Save route, delegates to save() function."""
    rv = save(
        request.form.get('title'),
        request.form.get('content').encode('utf-8'),
        request.form.get('display_mode'),
        os.path.join(PASTY_ROOT, 'posts'),
        year, month, day, hour, minute, second, id, request.form.get(
            'irc_channel'), request.form.get('post_sender'), request.form.get('post_privmsg'))
    if rv is None:
        abort(400)
    else:
        return rv


@app.route(
    "/get/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>")
def get(year, month, day, hour, minute, second, id):
    """Get route, return a post."""
    datetime = dt.strptime(
        str(year) + makeString(month) + makeString(day) + makeString(hour) +
        makeString(minute) + makeString(second),
        "%Y%m%d%H%M%S")
    post = getPost(os.path.join(PASTY_ROOT, 'posts'), datetime, id)
    if post is None:
        abort(404)
    elif isinstance(post, bool):
        abort(500)
    return render_template('post.html', view_mode="show",
                           post_mode=post['display_mode'],
                           post_id=post['link'],
                           post_content=post['content'],
                           post_title=post['title'],
                           irc=buildIrcChannelHash(irc_channels),
                           creator=post['user'],
                           files=buildFileList(
                               os.path.join(
                                   PASTY_ROOT, 'posts', buildDateURL(datetime),
                                   id),
                               year, month, day, id))


@app.route(
    "/getautosave/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>")
def getAutoSave(year, month, day, hour, minute, second, id):
    """Get autosaved post."""
    datetime = dt.strptime(
        str(year) + makeString(month) + makeString(day) + makeString(hour) +
        makeString(minute) + makeString(second),
        "%Y%m%d%H%M%S")
    post = getPost(os.path.join(PASTY_ROOT, 'autosave'), datetime, id)
    if post is None:
        abort(404)
    elif isinstance(post, bool):
        abort(500)

    return render_template('post.html', view_mode="edit",
                           post_mode=post['display_mode'],
                           post_id=post['link'],
                           post_content=post['content'],
                           post_title=post['title'],
                           irc=buildIrcChannelHash(irc_channels),
                           creator=post['user'],
                           files=buildFileList(
                               os.path.join(
                                   PASTY_ROOT, 'posts', buildDateURL(datetime),
                                   id),
                               year, month, day, id))


@app.route("/all")
def getAll():
    """Return all posts as a list, delegates to post collector."""
    posts = getAllPosts(os.path.join(PASTY_ROOT, 'posts'))
    if isinstance(posts, bool):
        abort(500)

    return render_template('all.html', posts=posts)


@app.route(
    "/delete/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>",
    methods=['POST'],
    strict_slashes=False)
def deletePost(year, month, day, hour, minute, second, id):
    """Delete Post route."""
    datetime_string = '/'.join([str(year), makeString(month), makeString(day)])

    rv = delete(os.path.join(PASTY_ROOT, 'posts'), datetime_string, id)
    if rv and isinstance(rv, bool):
        abort(500)
    elif rv is None:
        abort(404)
    else:
        return rv


@app.route(
    "/upload/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>",
    methods=['POST'],
    strict_slashes=False)
def upload(year, month, day, hour, minute, second, id):
    """Upload file route."""
    if 'file' not in request.files:
        abort(400)

    directory = os.path.join(
        PASTY_ROOT, 'posts', '/'.join([str(year), makeString(month), makeString(day)]), id)
    try:
        os.makedirs(directory)
    except:
        pass

    for file_store in request.files.getlist("file"):
        file_store.save(os.path.join(directory, file_store.filename))

    return render_template('files.html',
                           files=buildFileList(
                               directory, year, month, day, id))


@app.route(
    "/getfile/<int:year>/<int:month>/<int:day>/<id>/<filename>",
    methods=['GET'],
    strict_slashes=False)
def getFile(year, month, day, id, filename):
    """Return a previously uploaded file."""
    return send_from_directory(
        os.path.join(
            PASTY_ROOT, 'posts', str(year),
            makeString(month),
            makeString(day),
            id),
        filename)


@app.route(
    "/delfile/<int:year>/<int:month>/<int:day>/<id>/<filename>",
    methods=['GET'],
    strict_slashes=False)
def delFile(year, month, day, id, filename):
    """Delete an uploaded file."""
    directory = os.path.join(
        PASTY_ROOT, 'posts', makeString(year),
        makeString(month),
        makeString(day),
        id)
    rv = deleteFile(os.path.join(directory, filename))
    if rv:
        abort(500)
    else:
        return render_template(
            'files.html', files=buildFileList(
                directory, year, month, day, id))


@app.route("/getuserlist/<channel>", methods=['GET'], strict_slashes=False)
def getUserList(channel):
    """Return a JSON array of all users in the specified channel."""
    global irc_client
    return json.dumps(irc_client.getUserList('#' + channel))


#
# Error handling
#


@app.errorhandler(400)
def bad_request(e):
    """Show Bad Request error."""
    return render_template('errors/400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    """Show Not Found error."""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Show Internal Server Error."""
    return render_template('errors/500.html'), 500


if __name__ == "__main__":      # pragma: no cover
    setup()
    app.run(host='0.0.0.0', port=8080, debug=True)
