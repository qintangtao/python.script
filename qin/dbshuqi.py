#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from db import DbSqlite3


class DbShuqi:

    def __init__(self, path):
        self._db = DbSqlite3(os.path.join(path, 'FuckShuqiContq1.db'))
        self._db._executeDML(
            'CREATE TABLE IF NOT EXISTS BOOK (id INT PRIMARY KEY, bookid TEXT, name TEXT, author TEXT, status INT);')
        self._db._executeDML(
            'CREATE TABLE IF NOT EXISTS SOURCE (id INT PRIMARY KEY, bookid TEXT, site TEXT, site_name TEXT, selected INT);')

if __name__ == "__main__":
    d = DbShuqi(os.getcwd())
