#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory, request, abort
from lib.poster import *
from lib.tools import *
from datetime import datetime as dt
app = Flask(__name__)

def save(title, content, directory, year=None, month=None, day=None, hour=None, minute=None, second=None, id=None):
    if content == None or title == None:
        return None

    if year != None and month != None and day != None and hour != None and minute != None and second != None:
        datetime = dt.strptime(str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second), "%Y%m%d%H%M%S")
    else:
        datetime = None

    return savePostTopLevel(title, content, datetime, id, directory)

@app.route("/")
def create():
    return render_template('post.html', view_mode="edit")

@app.route("/autosave", methods=['POST'], strict_slashes=False)
@app.route("/autosave/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>", methods=['POST'], strict_slashes=False)
def autosave(year=None, month=None, day=None, hour=None, minute=None, second=None, id=None):
    rv = save(request.form.get('title'), request.form.get('content'), 'autosave', year, month, day, hour, minute, second, id)
    if rv == None:
        abort(400)
    else:
        return rv

@app.route("/save", methods=['POST'], strict_slashes=False)
@app.route("/save/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>", methods=['POST'], strict_slashes=False)
def saveR(year=None, month=None, day=None, hour=None, minute=None, second=None, id=None):
    rv = save(request.form.get('title'), request.form.get('content'), 'posts', year, month, day, hour, minute, second, id)
    if rv == None:
        abort(400)
    else:
        return rv

@app.route("/get/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>")
def get(year, month, day, hour, minute, second, id):
    datetime = dt.strptime(str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second), "%Y%m%d%H%M%S")
    post = getPost('posts', datetime, id)
    if post == None:
        abort(404)
    elif type(post) == type(bool()):
        abort(500)
    return render_template('post.html', view_mode="show", post_id=post['link'], post_content=post['content'], post_title=post['title'])

@app.route("/getautosave/<int:year>/<int:month>/<int:day>/<int:hour>/<int:minute>/<int:second>/<id>")
def getAutoSave(year, month, day, hour, minute, second, id):
    datetime = dt.strptime(str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second), "%Y%m%d%H%M%S")
    post = getPost('autosave', datetime, id)
    if post == None:
        abort(404)
    elif type(post) == type(bool()):
        abort(500)
    return render_template('post.html', view_mode="edit", post_id=post['link'], post_content=post['content'], post_title=post['title'])

@app.route("/all")
def getAll():
    posts = getAllPosts()
    if type(posts) != type([]):
        abort(500)

    return render_template('all.html', posts=posts)

@app.route("/file/<id>/<name>")
def saveFile(id, name):
    pass

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
  app.run(host='0.0.0.0', debug=True)
