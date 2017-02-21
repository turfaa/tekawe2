import os
import sys

import json

from flask import Flask
from flask import make_response
from flask import session

from api import api
from line import line

app = Flask(__name__)
app.register_blueprint(api, url_prefix = '/api')
app.register_blueprint(line)
app.secret_key = os.urandom(22)

@app.route('/')
def index():
    return make_response(json.dumps([x for x in session]))

if __name__ == "__main__":
    app.run(port=80, host = '0.0.0.0', debug = 1)
