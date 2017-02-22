import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from myconfig import host, user, password, database
from util import randomString

class dbhandler:
    def __init__(self, host = host, user = user, password = password, database = database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.retcode = 0

    def __del__(self):
        try:
            self.c.close()
            self.conn.close()
        except:
            pass

    def connect(self):
        self.conn = MySQLdb.connect(self.host, self.user, self.password, self.database)
        self.c = self.conn.cursor()

    def disconnect(self):
        return
        self.c.close()
        self.conn.close()

    def eternal(self):
        while(True):
            try:
                self.c.execute('select now()')
                break
            except:
                self.connect()

    def adminExist(self, username, wait = False):
        self.eternal()

        self.c.execute('select 1 from admin where username = %s', (username, ))
        ret = (self.c.rowcount > 0)
        return ret

    def registerAdmin(self, username, password, wait = False):
        if self.adminExist(username, wait = True):
            ret = False
            if not(wait):
                self.disconnect()
            return ret

        self.eternal()
        self.c.execute('insert into admin (username, password) values (%s, %s)', (username, generate_password_hash(password)))
        self.conn.commit()

        ret = True
        if not(wait):
            self.disconnect()
        return ret

    def getUsername(self, token, wait = False):
        self.eternal()

        self.c.execute('select username from session where token=%s', (token, ))

        if (self.c.rowcount > 0):
            ret = self.c.fetchone()[0]
            if not(wait):
                self.disconnect()
            return ret
        else:
            ret = False
            if not(wait):
                self.disconnect()
            return ret

    def newToken(self, username, wait = False):
        self.eternal()

        token = randomString(16)
        while(self.getUsername(token, wait = True)):
            token = randomString(16)

        self.c.execute('insert into session (token, username) values (%s, %s)', (token, username))
        self.conn.commit()

        ret = token
        if not(wait):
            self.disconnect()
        return ret

    def loginAdmin(self, username, password, wait = False):
        self.eternal()

        self.c.execute('select password from admin where username = %s', (username, ))

        if self.c.rowcount > 0:
            res = self.c.fetchone()[0]
            if check_password_hash(res, password):
                ret = self.newToken(username, wait = True)
                if not(wait):
                    self.disconnect()
                return ret
            else:
                ret = False
                if not(wait):
                    self.disconnect()
                return ret
        else:
            ret = False
            if not(wait):
                self.disconnect()
            return ret

    def logoutAdmin(self, token, wait = False):
        self.eternal()

        self.c.execute('delete from session where token=%s', (token,))
        self.conn.commit()

        if not(wait):
            self.disconnect()

    def addPlayer(self, playerId, name, wait = False):
        self.eternal()

        self.c.execute('insert into user (playerId, name) values(%s, %s)', (playerId, name))
        self.conn.commit()
        if not(wait):
            self.disconnect()

    def addOut(self, playerId, message, wait = False):
        self.eternal()

        self.c.execute('insert into out_message (playerId, message) values(%s, %s)', (playerId, message))
        self.conn.commit()
        if not(wait):
            self.disconnect()

    def addIn(self, playerId, message, wait = False):
        self.eternal()

        self.c.execute('insert into in_message (playerId, message) values(%s, %s)', (playerId, message))
        self.conn.commit()
        if not(wait):
            self.disconnect()

    def addAction(self, playerId, actionType, info = None, wait = False):
        self.eternal()

        if info != None:
            self.c.execute('insert into action_queue (action_type, playerId, info) values(%s, %s, %s)', (actionType, playerId, info))
            self.conn.commit()
            if not(wait):
                self.disconnect()
        else:
            self.c.execute('insert into action_queue (action_type, playerId) values(%s, %s)', (actionType, playerId))
            self.conn.commit()
            if not(wait):
                self.disconnect()

    def incPointer(self, tipe, id, wait = False):
        self.eternal()

        self.c.execute('update pointer set id = id + %s where name = %s', (id, tipe))
        self.conn.commit()
        if not(wait):
            self.disconnect()

    def getPlayerName(self, playerId, wait = False):
        self.eternal()

        self.c.execute('select name from user where playerId = %s', (playerId, ))
        if self.c.rowcount > 0:
            ret = self.c.fetchone()[0]
            if not(wait):
                self.disconnect()
            return ret
        else:
            ret = False
            if not(wait):
                self.disconnect()
            return ret

    def getOutMessage(self, lastId = 0, playerId = None, wait = False):
        self.eternal()

        if playerId == None:
            self.c.execute('select out_message.time, user.playerId, user.name, out_message.message from user,out_message where out_message.id > %s and user.playerId = out_message.playerId order by out_message.time desc', (lastId,))
        else:
            self.c.execute('select out_message.time, user.playerId, user.name, out_message.message from user,out_message where out_message.id > %s and user.playerId = out_message.playerId and user.playerId = %s order by out_message.time desc', (lastId, playerId))

        ret = self.c.fetchall()
        if not(wait):
            self.disconnect()
        return ret

    def getInMessage(self, lastId = 0, playerId = None, wait = False):
        self.eternal()

        if playerId == None:
            self.c.execute('select in_message.time, user.playerId, user.name, in_message.message from user,in_message where in_message.id > %s and user.playerId = in_message.playerId order by in_message.time desc', (lastId,))
        else:
            self.c.execute('select in_message.time, user.playerId, user.name, in_message.message from user,in_message where in_message.id > %s and user.playerId = in_message.playerId and user.playerId = %s order by in_message.time desc', (lastId, playerId))

        ret = self.c.fetchall()
        if not(wait):
            self.disconnect()
        return ret

    def getPointer(self, tipe, wait = False):
        self.eternal()

        self.c.execute("select id from pointer where name = %s", (tipe,))
        ret = self.c.fetchone()[0]
        if not(wait):
            self.disconnect()
        return ret

    def getAction(self, lastId, wait = False):
        self.eternal()

        self.c.execute('select action_queue.action_type, user.playerId, user.name, action_queue.info from action_queue, user where action_queue.id > %s and action_queue.playerId = user.playerId', (lastId, ))
        ret = self.c.fetchall()
        if not(wait):
            self.disconnect()
        return ret

    def getPlayer(self, wait = False):
        self.eternal()

        self.c.execute('select playerId, name from user')
        ret = self.c.fetchall()
        if not(wait):
            self.disconnect()
        return ret
