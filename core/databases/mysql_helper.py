# -*- coding: utf-8 -*-
"""
author:lufoqin
func:二次封装mysql操作，基于pymysql库
"""

import pymysql
from core.logs import log
from string import Template


class MysqlHandler(object):
    def __init__(self, hostname, port, username, password, database=None, charset='utf8mb4'):
        self.cfg = {
            'host': hostname,
            'port': port,
            'user': username,
            'passwd': password,
            'db': database,
            'cursorclass': pymysql.cursors.DictCursor,
            'charset': charset
        }
        self.database = None
        self.__conn = self.build_connection()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def build_connection(self):
        try:
            self.database = pymysql.connect(**self.cfg)
            log.info('connect mysql success')
            return self.database
        except Exception as e:
            log.error(Template('connect mysql fail, the error info: $e, the database config info: $cfg'
                               '').substitute(e=e, cfg=self.cfg))

    @property
    def connect(self):
        return self.__conn

    def query(self, sql):
        with self.__conn.cursor() as cursor:
            log.info('query sql is: {}'.format(sql))
            try:
                cursor.execute(sql)
                # data_one = cursor.fetchone()
                data_all = cursor.fetchall()
                log.debug(Template('query results is: $all').substitute(all=data_all))
                return data_all
            except Exception as e:
                log.error('query fail, error info: {}, the sql is: {}'.format(str(e), str(sql)))
                return False

    def close(self):
        log.info('close connect')
        self.__conn.close()
