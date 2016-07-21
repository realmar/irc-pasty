from flask import Flask, render_template, send_from_directory, request
from lib.saver import *
from lib.tools import *
app = Flask(__name__)

@app.route("/")
def create():
    return render_template('new.html')

@app.route("/autosave/<id>", methods=['POST'])
def autosave(id):
    if id == 'None':
        id = generateID()
    if not save('autosave', id, request.form.get('input')):
        return id
    else:
        return '1'

@app.route("/save/<id>", methods=['POST'])
def save(id):
    print(request.form.get('input'))
    if id == 'None':
        id = generateID()
    if not save('posts', id, request.form.get('input')):
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
