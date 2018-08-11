#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from qin.db import DbSqlite3


class DbShuqi:

    def __init__(self, path):
        self._db = DbSqlite3(os.path.join(path, 'FuckShuqiContq1.db'))
        self._db._executeDML(
            'CREATE TABLE IF NOT EXISTS BOOK (id INTEGER PRIMARY KEY NOT NULL, bid TEXT NOT NULL UNIQUE, name TEXT NOT NULL, author TEXT NOT NULL, status INTEGER NOT NULL, time DATE DEFAULT (datetime(\'now\',\'localtime\')));')
        self._db._executeDML(
            'CREATE TABLE IF NOT EXISTS SOURCE (id INTEGER PRIMARY KEY NOT NULL, bid TEXT NOT NULL, site TEXT NOT NULL, site_name TEXT NOT NULL, total INTEGER DEFAULT 0, idx INTEGER DEFAULT 0);')

    def insert_book(self, dict):
        return self._db._executeDML('INSERT INTO BOOK (bid, name, author, status) values(\'%s\', \'%s\', \'%s\', %d)' % (dict['bid'], dict['name'], dict['author'], dict['status']))

    def update_book_time(self, bid):
        return self._db._executeDML('UPDATE BOOK SET time=datetime(\'now\',\'localtime\') WHERE bid=\'%s\'' % bid)

    def query_book(self, status, start, limit):
        cursor = None
        if status == -1:
            cursor = self._db._executeDQL(
                'SELECT bid, name, author, status from BOOK ORDER BY time DESC LIMIT %d, %d' % (start, limit))
        else:
            cursor = self._db._executeDQL(
                'SELECT bid, name, author, status from BOOK WHERE status=%d ORDER BY time DESC LIMIT %d, %d' % (status, start, limit))
        if cursor is None:
            return None
        listdata = []
        for row in cursor:
            listdata.append({'id': row[0], 'name': row[1],
                             'author': row[2], 'status': row[3]})
        return listdata

    def exists_book(self, bid):
        cursor = self._db._executeDQL(
            'SELECT * from BOOK WHERE bid=\'%s\'' % bid)
        if cursor is not None and len(cursor.fetchall()) > 0:
            return True
        return False

    def count_book(self, status):
        cursor = None
        if status == -1:
            cursor = self._db._executeDQL(
                'SELECT bid, name, author, status from BOOK')
        else:
            cursor = self._db._executeDQL(
                'SELECT bid, name, author, status from BOOK WHERE status=%d' % status)
        if cursor is not None:
            return len(cursor.fetchall())
        return 0

    def query_source(self, dict):
        cursor = self._db._executeDQL(
            'SELECT total, idx from SOURCE WHERE bid=\'%s\' and site=\'%s\'' % (dict['bid'], dict['site']))
        if cursor is None:
            return None
        listdata = []
        for row in cursor:
            listdata.append({'total': row[0], 'index': row[1]})
        return listdata

    def insert_source(self, dict):
        if self.exists_source(dict):
            return self.update_source(dict)
        return self._db._executeDML('INSERT INTO SOURCE (bid, site, site_name, total, idx) values(\'%s\', \'%s\', \'%s\', %d, %d)' % (dict['bid'], dict['site'], dict['site_name'], dict['total'], dict['idx']))

    def update_source(self, dict):
        return self._db._executeDML('UPDATE SOURCE SET site_name=\'%s\', total=%d, idx=%d WHERE bid=\'%s\' and site=\'%s\'' % (dict['site_name'], dict['total'], dict['idx'], dict['bid'], dict['site']))

    def exists_source(self, dict):
        cursor = self._db._executeDQL(
            'SELECT * from SOURCE WHERE bid=\'%s\' and site=\'%s\'' % (dict['bid'], dict['site']))
        if cursor is not None and len(cursor.fetchall()) > 0:
            return True
        return False


if __name__ == "__main__":
    d = DbShuqi(os.getcwd())
    d.exists_source({'site': 'www.aaa.com'})
