import json

from flask import session
from flask import Blueprint
from flask import make_response
from flask import request

from dbhandler import dbhandler

api = Blueprint('api', __name__)
db = dbhandler()

@api.route('/newAdmin', methods=['POST'])
def newAdminAPI():
    if not('loggedIn' in session):
        return local_make_response(json.dumps({'status' : False, 'message' : 'You are not logged in'}))

    if ('username' in request.form) & ('password' in request.form):
        if db.registerAdmin(request.form['username'], request.form['password']):
            return local_make_response(json.dumps({'status' : True}))
        else:
            return local_make_response(json.dumps({'status' : False, 'message' : 'Username is already taken'}))
    else:
        return local_make_response(json.dumps({'status' : False, 'message' : 'Form is not complete'}))

@api.route('/login', methods=['POST'])
def loginAPI():
    if ('username' in request.form) & ('password' in request.form):
        if db.loginAdmin(request.form['username'], request.form['password']):
            session['loggedIn'] = request.form['username']
            return local_make_response(json.dumps({'status' : True}))
        else:
            return local_make_response(json.dumps({'status' : False, 'message' : 'Username/password is wrong'}))
    else:
        return local_make_response(json.dumps({'status' : False, 'message' : 'Form is not complete'}))

@api.route('/getPlayer')
def getPlayer():
    if not('loggedIn' in session):
        return local_make_response(json.dumps({'status' : False, 'message' : 'You are not logged in'}))

    result = list(db.getPlayer())

    for i in range(len(result)):
        result[i] = list(result[i])
    return local_make_response(json.dumps({'status' : True, 'data' : result}))

@api.route('/getInMessage/', defaults={'playerId' : None, 'lastId' : 0})
@api.route('/getInMessage/<playerId>/<int:lastId>/')
def getInMessageAPI(playerId, lastId):
    if not('loggedIn' in session):
        return local_make_response(json.dumps({'status' : False, 'message' : 'You are not logged in'}))

    result = list(db.getInMessage(lastId = lastId, playerId = playerId))

    for i in range(len(result)):
        result[i] = list(result[i])
        result[i][0] = result[i][0].strftime('%m/%d/%Y (%H:%M:%S)')
    return local_make_response(json.dumps({'status' : True, 'data' : result}))

def local_make_response(original, code = 200):
    r = make_response(original)
    r.headers['Content-Type'] = 'application/json; charset=utf-8'

    return r
