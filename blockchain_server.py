from concurrent.futures import thread
import json
from xml.dom.minidom import Document
from flask import Flask
from flask import jsonify

import blockchain


app = Flask(__name__)
@app.route('/')
def helloworld():
    return 'HelloWorld🚀'
@app.route('/show')
def show():
    
    return '<h1>🚀😍⛓️❤️💥</h1>'
app.run(host='0.0.0.0',port='5000')