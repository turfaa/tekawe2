import os
import sys

import json

from flask import Flask
from flask import url_for

from api import api
from line import line
from web import web

app = Flask(__name__)
app.register_blueprint(api, url_prefix = '/api')
app.register_blueprint(line)
app.register_blueprint(web)
app.secret_key = os.urandom(22)

with app.test_request_context():
    app.config['css'] = [url_for('static', filename='css/bootstrap.min.css'), url_for('static', filename='css/bootstrap-material-design.min.css'), url_for('static', filename='css/ripples.min.css')]

    app.config['js'] = [url_for('static', filename='js/jquery.min.js'), url_for('static', filename='js/bootstrap.min.js'), url_for('static', filename='js/material.min.js'), url_for('static', filename='js/ripples.min.js'), url_for('static', filename='js/init.js')]

if __name__ == "__main__":
    app.run(port=80, host = '0.0.0.0', debug = 1, threaded = True)
