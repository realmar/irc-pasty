from flask import Flask, render_template, send_from_directory, request, abort
from lib.poster import *
from lib.tools import *
app = Flask(__name__)

@app.route("/")
def create():
    return render_template('post.html', view_mode="edit")

@app.route("/autosave/<id>", methods=['POST'])
def autosave(id):
    rv = savePostTopLevel(request.form.get('input'), request.form.get('title'), id, 'autosave')

    if rv == None:
        abort(405)
    else:
        return rv

@app.route("/save/<id>", methods=['POST'])
def save(id):
    rv = savePostTopLevel(request.form.get('input'), request.form.get('title'), id, 'posts')

    if rv == None:
        abort(405) # implement error handling
    else:
        return rv

@app.route("/get/<id>")
def get(id):
    post = getPost('posts', id)
    if post == None:
        pass # do 404
    if post == False:
        pass # do 500
    return render_template('post.html', view_mode="show", post_id=id, post_content=post['content'], post_title=post['title'])

@app.route("/getautosave/<id>")
def getAutoSave(id):
    post = getPost('autosave', id)
    if post == None:
        pass # do 404
    if post == False:
        pass # do 500
    return render_template('post.html', view_mode="edit", post_id=id, post_content=post['content'], post_title=post['title'])

@app.route("/all")
def getAll():
    return render_template('all.html', posts=getAllPosts())

@app.route("/file/<id>/<name>")
def saveFile(id, name):
    pass

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
