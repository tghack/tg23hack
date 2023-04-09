from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response
from jinja2 import Environment
from datetime import date

app = Flask(__name__)
Jinja2 = Environment()
#app.config.from_pyfile('config.py')


@app.route("/createNote", methods=['POST'])
def createNote():
    name = request.values.get('name')
    if(name is None): name = "No Name"
    note  = request.values.get('note')

    d = date.today()
    output = Jinja2.from_string("""Note created on """+d.isoformat()+"""
"""+note+"").render()
    

    return output, 200, {'Content-Disposition': 'attachment; filename='+(name.replace(" ","_"))+".txt"}

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)