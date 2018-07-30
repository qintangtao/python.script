#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import sqlite3


class DbSqlite3(object):

    def __init__(self, database):
        self._open(database)

    def __del__(self):
        self._close()

    def _open(self, database):
        try:
            self._conn = sqlite3.connect(database)
        except Exception, e:
            logging.error(str(e))
            self._conn = None

    def _close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def _executeDML(self, sql):
        # INSERT、UPDATE、DELETE
        if self._conn:
            try:
                c = self._conn.cursor()
                c.execute(sql)
                self._conn.commit()
                return True
            except Exception, e:
                logging.error(str(e))
        return False

    def _executeDQL(self, sql):
        # SELECT
        if self._conn:
            try:
                c = self._conn.cursor()
                return c.execute(sql)
            except Exception, e:
                logging.error(str(e))
        return None
