#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from qin.db import DbSqlite3


class DbShuqi:

    def __init__(self, path):
        self._db = DbSqlite3(os.path.join(path, 'FuckShuqiContq1.db'))
        self._db._executeDML(
            'CREATE TABLE IF NOT EXISTS BOOK (id INTEGER PRIMARY KEY NOT NULL, bid TEXT NOT NULL UNIQUE, name TEXT NOT NULL, author TEXT NOT NULL, status INTEGER NOT NULL, time DATE DEFAULT (datetime(\'now\',\'localtime\')));')

    def insert(self, dict):
        return self._db._executeDML('INSERT INTO BOOK (bid, name, author, status) values(\'%s\', \'%s\', \'%s\', %d)' % (dict['bid'], dict['name'], dict['author'], dict['status']))

    def update_time(self, bid):
        return self._db._executeDML('UPDATE BOOK SET time=datetime(\'now\',\'localtime\') WHERE bid=\'%s\'' % bid)

    def query(self, status, start, limit):
        if status == -1:
            return self._db._executeDQL('SELECT bid, name, author, status from BOOK ORDER BY time DESC LIMIT %d, %d' % (start, limit))
        else:
            return self._db._executeDQL('SELECT bid, name, author, status from BOOK WHERE status=%d ORDER BY time DESC LIMIT %d, %d' % (status, start, limit))

    def exists(self, bid):
        cursor = self._db._executeDQL(
            'SELECT * from BOOK WHERE bid=\'%s\'' % bid)
        if cursor is not None and len(cursor.fetchall()) > 0:
            return True
        return False

    def count(self, status):
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

if __name__ == "__main__":
    d = DbShuqi(os.getcwd())
    # d.insert({'bid': 'bid', 'name': 'name',
    #         'author': 'author', 'status': 1})
    cursor = d.query(1, 1, 4)
    for row in cursor:
        print row[0]
    print d.count(1)
