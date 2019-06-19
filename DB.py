import mysql.connector

class QDBObj():
    def __init__(self, _user, _password, _database):
        self.status = False
        try:
            self.mysqlObj = mysql.connector.MySQLConnection(user=_user, password= _password, database=  _database , charset='utf8',
                     use_unicode=True)
            self.sqlCursor = self.mysqlObj.cursor()
            self.status = True
        except Exception as e:
            print "data base openning exception", e
            self.status = False

