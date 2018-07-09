#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import requests
import logging
import scapi
import shutil
import json
from PyQt4 import QtCore


class DumpThread(QtCore.QThread):

    signal_progress = QtCore.pyqtSignal(int, int, int)
    signal_log = QtCore.pyqtSignal(int, str)
    signal_finished = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(DumpThread, self).__init__(parent)
        self.__exit = False

    def start(self, index, path, bid, uid):
        self.__index = index
        self.__path = path
        self.__bid = bid
        self.__uid = uid
        self.__exit = False
        super(DumpThread, self).start()

    def stop(self):
        self.__exit = True
        #self.wait()

    def run(self):
        code = 1
        json = scapi.request_WapBookIntro(self.__bid, self.__uid)
        if json is not None:
            if json['errno'] == '0':
                path = os.path.join(self.__path, json['data']['book'][
                                    'clazz'], "%s-%s" % (json['data']['book']['name'], json['data']['book']['author']))
                if not os.path.exists(path):
                    os.makedirs(path)

                book = json['data']['book']
                data = {'cover': book['cover'], 'clazz': book['clazz'], 'name': book[
                    'name'], 'author': book['author'], 'desc': book['desc']}

                if 'sources' in json:
                    if self.__dump_chapter_by_sources(path, json['sources'], data):
                        code = 0
                else:
                    json2 = scapi.request_ChangeSource(self.__bid, self.__uid)
                    if json2 is not None:
                        if json2['errno'] == 0 and 'sources' in json2:
                            if self.__dump_chapter_by_sources(path, json2['sources'], data):
                                code = 0
                        else:
                            logging.error(
                                'request_ChangeSource: %s', json2['errno'])
                    else:
                        logging.error('request_ChangeSource failed')
            else:
                logging.error('request_WapBookIntro: %s', json['errno'])
        else:
            logging.error('request_WapBookIntro failed')
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

    def __get_book_info(self, path):
        filepath = os.path.join(path, 'book.json')
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.loads(f.read())
        return None

    def __get_book_site(self, path):
        old_site = ''
        old_data = self.__get_book_info(path)
        if old_data is not None:
            if 'site' in old_data and old_data['site'] != '':
                old_site = old_data['site']
        return old_site

    def __save_chapter_info(self, path, data):
        filepath = os.path.join(path, 'chapter.json')
        self.__save_json(filepath, data)

    def __dump_chapter_by_sources(self, path, sources, data):
        old_site = self.__get_book_site(path)
        for item in sources:
            if self.__exit:
                break

            if old_site != '':
                if old_site != item['site']:
                    continue
                else:
                    old_site = ''

            data['site'] = item['site']
            data['site_name'] = item['site_name']

            chapterpath = os.path.join(path, 'chapters')
            if not os.path.exists(chapterpath):
                os.makedirs(chapterpath)
            if self.__dump_chapter_html(chapterpath, self.__bid, self.__uid, item['site']):
                self.__save_book_info(path, data)
                return True
            else:
                if self.__exit is False:
                    shutil.rmtree(chapterpath)

        if self.__exit:
            self.__save_book_info(path, data)
        return False

    def __dump_chapter_html(self, path, bid, uid, site):
        json = scapi.request_WapChapterList(bid, uid, site)
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
