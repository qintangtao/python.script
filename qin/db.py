#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import logging
import sqlite3


class DbSqlite3(object):

    def __init__(self, database):
        self.__open(database)

    def __del__(self):
        self.__close()

    def __open(self, database):
        try:
            self.__conn = sqlite3.connect(database)
        except Exception, e:
            logging.error(str(e))
            self.__conn = None

    def __close(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    def __executeDML(self, sql):
        # INSERT、UPDATE、DELETE
        if self.__conn:
            try:
                c = self.__conn.cursor()
                c.execute(sql)
                c.commit()
                return True
            except Exception, e:
                logging.error(str(e))
        return False

    def __executeDQL(self, sql):
        # SELECT
        if self.__conn:
            try:
                c = self.__conn.cursor()
                return c.execute(sql)
            except Exception, e:
                logging.error(str(e))
        return None
