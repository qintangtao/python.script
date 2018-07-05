#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import logging
import zsapi
from PyQt4 import QtCore
from config import ConfigFile


class DumpThread(QtCore.QThread):

    signal_list = QtCore.pyqtSignal(list)
    signal_start = QtCore.pyqtSignal(int)
    signal_title = QtCore.pyqtSignal(str)
    signal_log = QtCore.pyqtSignal(str)

    def __init__(self, token, path, gender, _type, major, minor, start, limit, parent=None):
        super(DumpThread, self).__init__(parent)
        self.token = token
        self.path = path
        self.gender = gender
        self.type = _type
        self.major = major
        self.minor = minor
        self.startA = start
        self.limit = limit
        self.dump = False
        self.json = None

    def start(self):
        self.__exit = False
        super(DumpThread, self).start()

    def stop(self):
        self.__exit = True
        self.wait()

    def run(self):
        self.__emit_signal_log("[%s] [%s] [%s] [%s] [%s] [%d] [%d]", self.token, self.gender,
                               self.type, self.major, self.minor, self.startA, self.limit)

        if self.dump:
            if self.json is None:
                self.__auto_dump()
            else:
                self.__dump_by_books(self.token, self.path, self.json)
        else:
            self.__request_book_by_categories(
                self.gender, self.type, self.major, self.minor, self.startA, self.limit)

        self.__emit_signal_log('exit')

    def __auto_dump(self):
        while self.__exit is False:
            while self.__exit is False:
                try:
                    if self.__dump_by_categories(
                            self.token, self.path, self.gender, self.type, self.major, self.minor, self.startA, self.limit):
                        break
                except Exception, e:
                    logging.error(str(e))
                    self.__emit_signal_log(str(e))
                    for x in xrange(1, 3):
                        if self.__exit:
                            break
                        time.sleep(1)
            if self.__exit is False:
                self.startA += self.limit
                self.__emit_signal_start(self.startA)

    def __emit_signal_list(self, json):
        self.signal_list.emit(json)

    def __emit_signal_start(self, start):
        self.signal_start.emit(start)

    def __emit_signal_title(self, msg, *args):
        if args:
            msg = msg % args
        self.signal_title.emit(msg)

    def __emit_signal_log(self, msg, *args):
        if args:
            msg = msg % args
        self.signal_log.emit(msg)

    def __save_book_conf(self, path, json):
        conf = ConfigFile(path)
        conf.book_title = json['title']
        conf.book_author = json['author']
        conf.book_shortIntro = json['shortIntro']
        conf.book_majorCate = json['majorCate']
        conf.book_minorCate = json['minorCate']

    def __save_book_done(self, path):
        conf = ConfigFile(path)
        conf.dump_done = True

    def __is_book_done(self, path):
        conf = ConfigFile(path)
        if conf.dump_done is None:
            return False
        return True

    def __dump_by_books(self, token, path, json):

        for item in json:

            if self.__exit:
                break

            path1 = os.path.join(path, 'dump', item['majorCate'], item[
                                 'minorCate'], '%s-%s' % (item['title'], item['author']))
            if not os.path.exists(path1):
                os.makedirs(path1)

            self.__emit_signal_title("%s-%s", item['title'], item['author'])

            config_path = os.path.join(path1, 'config.ini')
            if self.__is_book_done(config_path):
                continue

            self.__save_book_conf(config_path, item)

            json5 = zsapi.request_chapters_bought(item['_id'], token)
            if json5 is None:
                self.__emit_signal_log('request_chapters_bought failed')
                return False

            json2 = zsapi.request_btoc('summary', item['_id'])
            if json2 is None:
                self.__emit_signal_log('request_btoc failed')
                return False

            for item2 in json2:

                if self.__exit:
                    break

                json3 = zsapi.request_btoc_book(item2['_id'], 'chapters')
                if json3 is None:
                    self.__emit_signal_log('request_btoc_book failed')
                    return False

                json7 = zsapi.request_purchase_batchBuy(
                    json3['book'], json3['_id'], False, False, 1, len(json3['chapters']), token)
                if json7 is None:
                    self.__emit_signal_log('request_purchase_batchBuy failed')
                    return False

                for item3 in json3['chapters']:

                    if self.__exit:
                        break

                    self.__emit_signal_log(item3['title'])

                    path2 = os.path.join(path1, '%d.txt' % item3['order'])
                    if not os.path.exists(path2):

                        json4 = zsapi.request_chapter_link(item3['link'])
                        if json4 is None and json4['ok'] is False:
                            self.__emit_signal_log(
                                'request_chapter_link failed')
                            return False

                        cpContent = ''

                        if json4['chapter']['isVip'] is False:
                            cpContent = json4['chapter']['cpContent']
                        else:
                            order = item3['order']
                            key = zsapi.find_key2(json7, order)
                            if key is None:
                                key = zsapi.find_key(json5, order)
                                if key is None:
                                    while True:

                                        if self.__exit:
                                            break

                                        json6 = zsapi.request_purchase_buy(
                                            'txt', order, 'false', item['_id'], 'auto', token)
                                        if json6 is None:
                                            self.__emit_signal_log(
                                                'request_purchase_buy failed')
                                            return False

                                        if json6['ok'] is True:
                                            key = json6['key']
                                            break
                                        else:
                                            self.__emit_signal_log(
                                                'key is None')
                                            for x in xrange(1, 20):
                                                if self.__exit:
                                                    break
                                                time.sleep(1)

                            if self.__exit:
                                break

                            if key is not None:
                                cpContent = zsapi.decrypt(
                                    key, json4['chapter']['cpContent'])
                            else:
                                self.__emit_signal_log('key is None')
                                return False

                        if cpContent == '':
                            self.__emit_signal_log('content is empty')
                            return False

                        try:
                            with open(path2, 'w') as f:
                                f.write(item3['title'] + "\n\n")
                                f.write(cpContent)
                        except Exception, e:
                            logging.error(str(e))
                            self.__emit_signal_log('write file failed.')
                            self.__emit_signal_log(str(e))
                            return False

            if self.__exit is False:
                self.__save_book_done(config_path)

        return True

    def __dump_by_categories(self, token, path, gender, _type, major, minor, start, limit):
        json1 = zsapi.request_book_by_categories(
            gender, _type, major, minor, start, limit)
        if json1 is None:
            self.__emit_signal_log('request_book_by_categories failed')
            return False

        if json1['ok'] is False:
            self.__emit_signal_log('ok is false')
            return False

        if json1['total'] == 0:
            self.__exit = True
            self.__emit_signal_log('exit')
            return True

        return self.__dump_by_books(token, path, json1['books'])

    def __request_book_by_categories(self, gender, _type, major, minor, start, limit):
        json1 = zsapi.request_book_by_categories(
            gender, _type, major, minor, start, limit)
        if json1 is None:
            self.__emit_signal_log('request_book_by_categories failed')
            return False

        if json1['ok'] is False:
            self.__emit_signal_log('ok is false')
            return False

        if json1['total'] == 0:
            self.__exit = True
            self.__emit_signal_log('exit')
            return True

        self.__emit_signal_list(json1['books'])
        return True
