import json

from flask import session
from flask import Blueprint
from flask import make_response
from flask import request

from dbhandler import dbhandler

api = Blueprint('api', __name__)

@api.route('/newAdmin', methods=['POST'])
def newAdminAPI():
    if not('token' in request.form):
        return local_make_response(json.dumps({'status' : False, 'message' : 'You are not logged in'}))

    db = dbhandler()

    if not(db.getUsername(request.form['token'])):
        return local_make_response(json.dumps({'status' : False, 'message' : 'Session not found'}))

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
        db = dbhandler()
        token = db.loginAdmin(request.form['username'], request.form['password'])
        if token:
            return local_make_response(json.dumps({'status' : True, 'token' : token}))
        else:
            return local_make_response(json.dumps({'status' : False, 'message' : 'Username/password is wrong'}))
    else:
        return local_make_response(json.dumps({'status' : False, 'message' : 'Form is not complete'}))

@api.route('/logout')
def logoutAPI():
    db = dbhandler()
    db.logoutAdmin(request.args.get('token'))
    return local_make_response(json.dumps({'status' : True}))

@api.route('/getPlayer')
def getPlayer():
    db = dbhandler()
    if not(db.getUsername(request.args.get('token'))):
        return local_make_response(json.dumps({'status' : False, 'message' : 'Session not found'}))

    print(db.getUsername(request.args.get('toke')))
    result = list(db.getPlayer())

    for i in range(len(result)):
        result[i] = list(result[i])
    return local_make_response(json.dumps({'status' : True, 'data' : result}))

@api.route('/getInMessage/', defaults={'playerId' : None, 'lastId' : 0})
@api.route('/getInMessage/<playerId>/<int:lastId>/')
def getInMessageAPI(playerId, lastId):
    db = dbhandler()
    if not(db.getUsername(request.args.get('token'))):
        return local_make_response(json.dumps({'status' : False, 'message' : 'Session not found'}))

    result = list(db.getInMessage(lastId = lastId, playerId = playerId))

    for i in range(len(result)):
        result[i] = list(result[i])
        result[i][0] = result[i][0].strftime('%m/%d/%Y (%H:%M:%S)')
    return local_make_response(json.dumps({'status' : True, 'data' : result}))

def local_make_response(original, code = 200):
    r = make_response(original)
    r.headers['Content-Type'] = 'application/json; charset=utf-8'

    return r
