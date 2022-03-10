import time
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def convert_json_from_lists(keys, data):
    container = []
    if data:
        for e in data:
            j = {}
            for k, v in enumerate(e):
                j[keys[k]] = v
            container.append(j)
    return container


class Connection():
    def cursor() -> None:
        ...

    def close() -> None:
        ...


class DBTypes(Enum):
    Oracle = 1
    Sqlite3 = 2
    MySql = 3
    ElasticSearch = 4


class Stream():
    def __init__(self, iterable) -> None:
        self.__iterable = iterable

    def foreach(self, fun):
        for e in self.__iterable:
            fun(e)


class DataSource(object):
    __conn = None

    def __init__(self,
                 dbType=None,
                 user=None,
                 password=None,
                 ip=None,
                 port=None,
                 db=None) -> None:
        self.__dbType = dbType
        self.__user = user
        self.__password = password
        self.__ip = ip
        self.__port = port
        # Sqlite3: db file name ; Others: database name.
        self.__db = db

    def db_type(self):
        return self.__dbType

    def get_conn(self) -> Connection:
        if self.__conn:
            return self.__conn
        if self.__dbType is None:
            return None
        elif self.__dbType == DBTypes.Oracle:
            # 'user/password@ip:port/sid'
            import cx_Oracle
            self.__conn = cx_Oracle.connect('{}/{}@{}:{}/{}'.format(
                self.__user, self.__password, self.__ip, self.__port,
                self.__db))
        elif self.__dbType == DBTypes.Sqlite3:
            import sqlite3
            self.__conn = sqlite3.connect(self.__db)
        elif self.__dbType == DBTypes.MySql:
            import pymysql
            print(self.__ip,
                  self.__user,
                  self.__password,
                  self.__db)
            self.__conn = pymysql.connect(
                host=self.__ip,
                user=self.__user,
                port=self.__port,
                passwd=self.__password,
                db=self.__db)
        return self.__conn

    def close_conn(self):
        self.__conn.close()
        self.__conn = None


class PySqlTemplate():
    data_source = DataSource
    __params = None

    def __init__(self, statement) -> None:
        self.__statement = statement

    @staticmethod
    def statement(statement):
        return PySqlTemplate(statement)

    @staticmethod
    def set_data_source(data_source):
        PySqlTemplate.data_source = data_source

    def __prepare(self):
        if PySqlTemplate.data_source.db_type() == DBTypes.Oracle:
            i = 1
            params_map = {}
            for p in self.__params:
                params_map['P' + str(i)] = p
                i += 1
            self.__params = params_map
            self.__statement = self.__statement.replace('?', '{}').format(
                *map(lambda k: ':' + str(k), params_map.keys())).upper()
        elif PySqlTemplate.data_source.db_type() == DBTypes.MySql:
            self.__statement = self.__statement.replace('?', '%s')

    def params(self, *params):
        self.__params = params
        self.__prepare()
        return self

    def list_all(self):
        conn = PySqlTemplate.data_source.get_conn()
        cur = conn.cursor()
        log.warn('_params: %s', self.__params)
        log.warn('__statement: %s', self.__statement)
        cur.execute(self.__statement, self.__params if self.__params else {})
        cols = [item[0] for item in cur.description]
        log.warn(','.join(cols))
        res = cur.fetchall()
        cur.close()
        PySqlTemplate.data_source.close_conn()
        return [list(e) if len(cols) > 1 else e[0] for e in res]

    def list_csv(self):
        conn = PySqlTemplate.data_source.get_conn()
        cur = conn.cursor()
        log.warn('_params: %s', self.__params)
        log.warn('__statement: %s', self.__statement)
        cur.execute(self.__statement, self.__params if self.__params else {})
        cols = [item[0] for item in cur.description]
        log.warn(','.join(cols))
        res = cur.fetchall()
        cur.close()
        PySqlTemplate.data_source.close_conn()
        dt = [','.join(list(e)) if len(cols) > 1 else e[0] for e in res]
        dt.insert(0, ','.join(cols))
        return '\n'.join(dt)

    def list_json(self):
        conn = PySqlTemplate.data_source.get_conn()
        cur = conn.cursor()
        log.warn('_params: %s', self.__params)
        log.warn('__statement: %s', self.__statement)
        cur.execute(self.__statement, self.__params if self.__params else {})
        cols = [item[0] for item in cur.description]
        log.warn(','.join(cols))
        res = cur.fetchall()
        cur.close()
        PySqlTemplate.data_source.close_conn()
        dt = [list(e) if len(cols) > 1 else e[0] for e in res]
        return convert_json_from_lists(cols, dt)


def query_mysql():
    PySqlTemplate.set_data_source(
        DataSource(
            dbType=DBTypes.MySql,
            user='root',
            password='root',
            ip='127.0.0.1',
            port=3306,
            db='billing')
    )
    re = PySqlTemplate.statement(
        'SELECT * FROM BALANCE'
    ).list_all()
    Stream(re).foreach(log.info)
    re = PySqlTemplate.statement(
        'SELECT * FROM BALANCE'
    ).list_all()
    Stream(re).foreach(log.info)


query_mysql()


def query_oracle():
    PySqlTemplate.set_data_source(
        DataSource(
            dbType=DBTypes.Oracle,
            user='scott',
            password='123456',
            ip='localhost',
            port=1521,
            db='orcl'))

    re = PySqlTemplate.statement(
        'select * from DEPT t where deptno >= ?'
    ).params(20).list_all()

    Stream(re).foreach(log.info)


def query_sqlite3():
    PySqlTemplate.set_data_source(
        DataSource(
            dbType=DBTypes.Sqlite3,
            db='test.db'))
    re = PySqlTemplate.statement(
        'select count(timestamp) from record where timestamp>?'
    ).params(int(time.time()-(3600*24*30))).list_all()
    Stream(re).foreach(log.info)
