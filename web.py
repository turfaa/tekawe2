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
req = HTTPRequest('http://localhost/api/')

@web.route('/')
def index():
    if not('token' in session):
        return render_template('login.html', css = current_app.config['css'], js = current_app.config['js'], formAction = url_for('web.login'), home = url_for('web.index'))

    user = json.loads(req.GET('getPlayer', {'token' : session['token']}))

    if user['status']:
        user = user['data']
    else:
        return redirect(url_for('web.logout'))

    for i in range(len(user)):
        user[i] = {'name' : user[i][1], 'link' : url_for('web.showChat', playerId = user[i][0])}

    return render_template('dashboard.html',css = current_app.config['css'], js = current_app.config['js'], loggedIn = True, logout = url_for('web.logout'), users = user, home = url_for('web.index'))

@web.route('/login', methods = ['POST'])
def login():
    if (('username' in request.form) & ('password' in request.form)):
        result = json.loads(req.POST('login',{'username' : request.form['username'], 'password' : request.form['password']}))

        if result['status']:
            session['token'] = result['token']

    return redirect(url_for('web.index'))

@web.route('/logout')
def logout():
    if ('token' in session):
        req.GET('logout', {'token' : session['token']})
        session.pop('token', None)

    return redirect(url_for('web.index'))

@web.route('/showChat/', defaults = {'playerId' : None})
@web.route('/showChat/<playerId>')
def showChat(playerId):
    if not('token' in session):
        return render_template('login.html', css = current_app.config['css'], js = current_app.config['js'], formAction = url_for('web.login'), home = url_for('web.index'))

    print('getInMessage/{}/'.format(playerId))
    chat = json.loads(req.GET('getInMessage/{}/0'.format(playerId), {'token' : session['token']}))
    if chat['status']:
        chat = chat['data']
    else:
        return redirect(url_for('web.logout'))

    for i in range(len(chat)):
        chat[i] = {'time' : chat[i][0], 'name' : chat[i][2], 'message' : chat[i][3]}

    return render_template('chat.html',css = current_app.config['css'], js = current_app.config['js'], loggedIn = True, logout = url_for('web.logout'), chats = chat, home = url_for('web.index'))
