from flask import Flask, render_template, send_from_directory
app = Flask(__name__)

@app.route("/")
def create():
    pass

@app.route("/autosave/<id>")
def autosave(id):
    pass

@app.route("/save/<id>")
def save(id):
    pass

@app.route("/get/<id>")
def get(id):
    pass

@app.route("/file/<id>/<name>")
def saveFile(id, name):
    pass

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
