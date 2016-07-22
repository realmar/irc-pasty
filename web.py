from flask import Flask, render_template, send_from_directory, request, abort
from lib.saver import *
from lib.tools import *
app = Flask(__name__)

@app.route("/")
def create():
    return render_template('post.html')

@app.route("/autosave/<id>", methods=['POST'])
def autosave(id):
    content = request.form.get('input')
    title = request.form.get('title')

    if content == None or title == None:
        abort(405)      # choose an approptiate error code

    if id == 'None':
        id = generateID()
    if not savePost('autosave', id, content, title):
        return id
    else:
        return '1'

@app.route("/save/<id>", methods=['POST'])
def save(id):
    content = request.form.get('input')
    title = request.form.get('title')
    if content == None or title == None:
        abort(405)      # choose an approptiate error code

    if id == 'None':
        id = generateID()
    if not savePost('posts', id, content, title):
        return id
    else:
        return '1'

@app.route("/get/<id>")
def get(id):
    pass

@app.route("/all")
def getAll():
    pass

@app.route("/file/<id>/<name>")
def saveFile(id, name):
    pass

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
