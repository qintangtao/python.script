#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
import logging
import scapi
import json
from PyQt4 import QtCore


class SourcesThread(QtCore.QThread):

    signal_sources = QtCore.pyqtSignal(int, list)
    signal_finished = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(SourcesThread, self).__init__(parent)
        self.__exit = False

    def start(self, index, bid, uid):
        self.__index = index
        self.__bid = bid
        self.__uid = uid
        self.__exit = False
        super(SourcesThread, self).start()

    def stop(self):
        self.__exit = True
        # self.wait()

    def run(self):
        code = 1
        json = scapi.request_ChangeSource(self.__bid, self.__uid)
        if json is not None:
            if json['errno'] == 0:
                sources = []
                for item in json['sources']:
                    sources.append(
                        {'site_name': item['site_name'], 'site': item['site']})
                self.__emit_signal_sources(sources)
                code = 0
            else:
                logging.error('request_ChangeSource: %s', json['errno'])
        else:
            logging.error('request_ChangeSource failed')
        if self.__exit:
            code = 2
        self.__emit_signal_finished(code)

    def __emit_signal_sources(self, sources):
        self.signal_sources.emit(self.__index, sources)

    def __emit_signal_finished(self, code):
        self.signal_finished.emit(self.__index, code)


class DumpThread(QtCore.QThread):

    signal_progress = QtCore.pyqtSignal(int, int, int)
    signal_log = QtCore.pyqtSignal(int, str)
    signal_finished = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(DumpThread, self).__init__(parent)
        self.__exit = False

    def start(self, index, path, bid, uid, site, site_name):
        self.__index = index
        self.__path = path
        self.__bid = bid
        self.__uid = uid
        self.__site = site
        self.__site_name = site_name
        self.__exit = False
        super(DumpThread, self).start()

    def stop(self):
        self.__exit = True
        # self.wait()

    def run(self):
        self.__emit_signal_log('get book info')
        code = 1
        for i in xrange(0, 3):
            if self.__exit:
                break
            if self.__dump_chapter_html(self.__path, self.__bid, self.__uid, self.__site, self.__site_name):
                code = 0
                break
        if self.__exit:
            code = 2
        self.__emit_signal_finished(code)

    def __save_json(self, filepath, data):
        with open(filepath, 'w') as f:
            content = json.dumps(data)
            logging.debug(content)
            f.write(content)

    def __save_book_info(self, path, data):
        filepath = os.path.join(path, 'book.json')
        self.__save_json(filepath, data)

    def __save_chapter_info(self, path, data):
        filepath = os.path.join(path, 'chapter.json')
        self.__save_json(filepath, data)

    def __dump_chapter_html(self, path, bid, uid, site, site_name):
        self.__emit_signal_log('get chapter list')
        json = scapi.request_WapChapterList(bid, uid, site)
        if self.__exit:
            return False
        if json is None:
            logging.error('request_WapChapterList failed')
            return False
        if json['errno'] != '0':
            logging.error('errno: %d', json['errno'])
            return False
        if 'data' not in json:
            logging.error('data is none')
            return False
        if 'chapters' not in json['data']:
            logging.error('chapters is none')
            return False
        if 'book' not in json['data']:
            logging.error('book is none')
            return False
        book = json['data']['book']

        path = os.path.join(path, book['clazz'], "%s-%s" % (book['name'], book['author']), site_name)
        if not os.path.exists(path):
            os.makedirs(path)

        self.__emit_signal_log('save book info')
        data = {'cover': book['cover'], 'clazz': book['clazz'], 'name': book[
            'name'], 'author': book['author'], 'desc': book['desc'], 'status': book['status'], 'site': site, 'site_name': site_name}

        self.__save_book_info(path, data)

        total = len(json['data']['chapters'])
        if total > 0:
            self.__emit_signal_progress(total, 0)
            data_chapter = []
            for item in json['data']['chapters']:
                if self.__exit:
                    break
                index = item['cidx']
                filepath = os.path.join(path, "%s.html" % index)
                self.__emit_signal_log(item['title'])
                data_chapter.append({'cidx': index, 'title': item['title']})
                if not os.path.exists(filepath):
                    rett = False
                    for i in xrange(1, 3):
                        if self.__exit:
                            break
                        content = self.__request_get(item['url'])
                        if content is not None:
                            try:
                                with open(filepath, 'w') as f:
                                    f.write(item['title'] + '\n\n')
                                    f.write(content)
                                rett = True
                                break
                            except Exception, e:
                                logging.error(str(e))
                                logging.error(item['url'])
                        else:
                            logging.error(item['url'])
                    if self.__exit:
                        break
                    if rett is False:
                        return False
                self.__emit_signal_progress(total, index)
        else:
            logging.error('%s chapters is empty' % site)
            return False
        if self.__exit:
            return False
        else:
            data = {'chapters': data_chapter}
            self.__save_chapter_info(path, data)
            return True

    def __request_get(self, url, params=None):
        try:
            r = requests.get(url, params)
            logging.debug(r.url)
            if r.status_code == 200:
                logging.debug(r.content)
                return r.content
        except Exception, e:
            logging.error(str(e))
        return None

    def __emit_signal_log(self, msg, *args):
        if args:
            msg = msg % args
        self.signal_log.emit(self.__index, msg)

    def __emit_signal_progress(self, total, current):
        self.signal_progress.emit(self.__index, total, current)

    def __emit_signal_finished(self, code):
        self.signal_finished.emit(self.__index, code)


def main():
    pass

if __name__ == "__main__":
    main()
