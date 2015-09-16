# warp a db connection
import mysql.connector
import functools
import threading
import types

#db connection instance
class _Engine(object):
    def __init__(self):
        self._host = '10.12.0.56'
        self._port = '3306'
        self._user = 'fanxing'
        self._pwd  = 'kugou2014'
        self._database = 'd_fanxing'
        self._connect = mysql.connector.connect(host=self._host, port=self._port, user=self._user, password=self._pwd, database=self._database, use_unicode=True)
    def connect(self):
        return self._connect
engine = _Engine()


#db_connection instance func
class _Dbctx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None 

    def init(self):
        self.connection = self._lazyConnection()
        self.transactions = 0

    def _lazyConnection(self):
        global engine
        return engine.connect()

    def cleanup(self):
        self.connection.close()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()

_db_ctx = _Dbctx()


class _Connectionctx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback): # exit?
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()

def connection():
    return _Connectionctx()

# connection decorator
def with_connection(func):
    @functools.wraps(func)
    def cwrapper(*args, **kw):
        with connection():
            return func(*args, **kw)
    return cwrapper


class _Transactionctx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        _db_ctx.transactions += 1
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions -= 1
        try:
            if _db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_cleanup:
                _db_ctx.cleanup()

    def rollback(self):
        global _db_ctx
        _db_ctx.connection.rollback()

    def commit(self):
        global _db_ctx
        try:
            _db_ctx.connection.commit()
        except:
            self.rollback()

def transaction():
    return _Transactionctx()

# transaction decorator
def with_transaction(func):
    @functools.wraps(func)
    def twrapper(*args, **kw):
        with transaction():
            return func(*args, **kw)
    return twrapper

""" class decorator todo
class With_connection(object):
    def __init__(self, func):
        self.wrapped = functools.wraps(func)

    def __call__(self, *args, **kw):
        with connection():
            return self.wrapped(*args, **kw)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)
"""

@with_connection
def select_one(sql): 
    cur = _db_ctx.cursor()
    #cur.execute('SELECT %s FROM d_fanxing_godness.t_room_barrage ORDER BY createTime desc limit 1' % 'fromIp')
    cur.execute(sql)
    res = cur.fetchall()   
    cur.close()
    return res

@with_connection
def update(sql):
    cur = _db_ctx.cursor()
    cur.execute(sql)
    _db_ctx.connection.commit()
    cur.close()


if __name__ == '__main__':
    select_one()





