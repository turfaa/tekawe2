import json

from flask import Blueprint
from flask import make_response
from flask import session
from flask import render_template
from flask import url_for
from flask import current_app
from flask import request
from flask import redirect

from httpHandler import HTTPRequest

web = Blueprint('web', __name__)

@web.route('/')
def index():
    if not('token' in session):
        return render_template('login.html', css = current_app.config['css'], js = current_app.config['js'], formAction = url_for('web.login'))

    return render_template('dashboard.html',css = current_app.config['css'], js = current_app.config['js'], logout = url_for('web.logout'))

@web.route('/login', methods = ['POST'])
def login():
    if (('username' in request.form) & ('password' in request.form)):
        req = HTTPRequest('http://localhost/')
        result = json.loads(req.POST('api/login',{'username' : request.form['username'], 'password' : request.form['password']}))

        if result['status']:
            session['token'] = result['token']

    return redirect(url_for('web.index'))

@web.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('web.index'))
