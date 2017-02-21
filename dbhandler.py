import MySQLdb
from myconfig import host, user, password, database

class dbhandler:
    def __init__(self, host = host, user = user, password = password, database = database):
        try:
            self.conn = MySQLdb.connect(host, user, password, database)
            self.c = self.conn.cursor()
            self.retcode = 0
        except:
            self.retcode = 1

    def eternal(self):
        while(True):
            try:
                self.c.execute('select now()')
                break
            except:
                self.__init__()

    def addPlayer(self, playerId, name):
        self.eternal()

        self.c.execute('insert into user (playerId, name) values(%s, %s)', (playerId, name))
        self.conn.commit()

    def addOut(self, playerId, message):
        self.eternal()

        self.c.execute('insert into out_message (playerId, message) values(%s, %s)', (playerId, message))
        self.conn.commit()

    def addIn(self, playerId, message):
        self.eternal()

        self.c.execute('insert into in_message (playerId, message) values(%s, %s)', (playerId, message))
        self.conn.commit()

    def addAction(self, playerId, actionType, info = None):
        self.eternal()

        if info != None:
            self.c.execute('insert into action_queue (action_type, playerId, info) values(%s, %s, %s)', (actionType, playerId, info))
            self.conn.commit()
        else:
            self.c.execute('insert into action_queue (action_type, playerId) values(%s, %s)', (actionType, playerId))
            self.conn.commit()

    def incPointer(self, tipe, id):
        self.eternal()

        self.c.execute('update pointer set id = id + %s where name = %s', (id, tipe))
        self.conn.commit()

    def getPlayerName(self, playerId):
        self.eternal()

        self.c.execute('select name from user where playerId = %s', (playerId, ))
        if self.c.rowcount > 0:
            return self.c.fetchone()[0]
        else:
            return False

    def getOutMessage(self, lastId = 0, playerId = None):
        self.eternal()

        if playerId == None:
            self.c.execute('select user.playerId, user.name, out_message.message from user,out_message where out_message.id > %s and user.playerId = out_message.playerId', (lastId,))
        else:
            self.c.execute('select user.playerId, user.name, out_message.message from user,out_message where out_message.id > %s and user.playerId = out_message.playerId and user.playerId = %s', (lastId, playerId))

        return self.c.fetchall()

    def getInMessage(self, lastId = 0, playerId = None):
        self.eternal()

        if playerId == None:
            self.c.execute('select user.playerId, user.name, in_message.message from user,in_message where in_message.id > %s and user.playerId = in_message.playerId', (lastId,))
        else:
            self.c.execute('select user.playerId, user.name, in_message.message from user,in_message where in_message.id > %s and user.playerId = in_message.playerId and user.playerId = %s', (lastId, playerId))

        return self.c.fetchall()

    def getPointer(self, tipe):
        self.eternal()

        self.c.execute("select id from pointer where name = %s", (tipe,))
        return self.c.fetchone()[0]

    def getAction(self, lastId):
        self.eternal()

        self.c.execute('select action_queue.action_type, user.playerId, user.name, action_queue.info from action_queue, user where action_queue.id > %s and action_queue.playerId = user.playerId', (lastId, ))
        return self.c.fetchall()

    def getPlayer(self):
        self.eternal()

        self.c.execute('select playerId, name from user')
        return self.c.fetchall()

    def watch(self):
        self.eternal()

        self.c.execute('select in_message.time, user.name, in_message.message from user, in_message where user.playerId = in_message.playerId order by in_message.time desc')
        return self.c.fetchall()
