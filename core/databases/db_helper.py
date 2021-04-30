# -*- coding: utf-8 -*-
"""
author: lufoqin
func: 数据库操作入口，用于分发不同类型数据库的操作
"""

from .mysql_helper import MysqlHandler


class DbHelper(object):
    def __init__(self, *args, **kwargs):
        pass

    def _dispatch(self, *args, **kwargs):
        ip = kwargs.get('ip')
        port = kwargs.get('port')
        user = kwargs.get('user')
        pwd = kwargs.get('pwd')
        db_type = kwargs.get('db_type') or "mysql"
        sql = kwargs.get('sql')
        method = kwargs.get('method') or "query"
        db = kwargs.get('db')

        if db_type.lower() == "mysql":
            if not ip or not port or not user or not pwd or not sql:
                raise ValueError("exec mysql db, ip/port/users/pwd/sql params is required")
            return self.mysql(ip, port, user, pwd, sql, method, db)
        elif db_type.lower() == "sqlserver":
            return self.sqlserver()
        elif db_type.lower() == "redis":
            return self.redis()
        elif db_type.lower() == "mongodb":
            return self.mongodb()
        else:
            return "database type not supported"

    def query(self, *args, **kwargs):
        return self._dispatch(method='query', **kwargs)

    @classmethod
    def mysql(cls, ip, port, user, pwd, sql, method, db=None):
        with MysqlHandler(ip, port, user, pwd, db) as mysqlhp:
            if method == "query":
                return mysqlhp.query(sql)
            elif method == "insert":
                pass

    def sqlserver(self):
        pass

    def redis(self):
        pass

    def mongodb(self):
        pass
