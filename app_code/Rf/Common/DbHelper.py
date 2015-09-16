# DbHelper.py
#_*_coding:utf-8_*_
import sys
sys.path.append('../../')

from System.Db.mcpWrapper import *


class DbHelper(object):
    
    @with_connection
    #def query(self, column, dbname, tablename):
    def query(self):
        cur = _db_ctx.cursor()
        cur.execute('SELECT %s FROM d_fanxing_godness.t_room_barrage ORDER BY createTime desc limit 1' % 'fromIp')
        print cur.fetchall()   
        cur.close()

    @with_connection
    def update(self):
        pass


    @with_transaction
    def querymutil(self):
        pass

    @with_transaction
    def updatemutil(self):
        pass


if __name__ == '__main__':
    DbHelper = DbHelper()
    DbHelper.query()




"""
dbhost = '10.12.0.56'
dbport = '3306'
databases = 'd_fanxing'
username = 'fanxing'
pwd = "kugou2014"


conn = mysql.connector.connect(host=dbhost, port=dbport, user=username, password=pwd, database=databases, use_unicode=True)

#conn_info = ('Driver={MySQL ODBC 5.3 Unicode Driver};Server=%s;Port=%s;Database=%s;User=%s; Password=%s;Option=3;' % (host, port, database, user, pwd))
#conn = pyodbc.connect(conn_info)
cursor = conn.cursor()

cursor.execute('SELECT %s FROM d_fanxing_godness.t_room_barrage ORDER BY createTime desc limit 1' % 'fromIp')
res = cursor.fetchall()

print res
"""












