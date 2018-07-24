#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import logging
import scapi
import time
from PyQt4 import QtCore
from cache import SourcesCache, ChaptersCache, SettingsCache
from qin import utils


class SearchThread(QtCore.QThread):

    signal_search = QtCore.pyqtSignal(int, list)
    signal_finished = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(SearchThread, self).__init__(parent)
        self.__exit = False

    def start(self, uid, major, minor, status, sort, start, limit):
        self.__uid = uid
        self.__major = major
        self.__minor = minor
        self.__status = status
        self.__sort = sort
        self.__start = start
        self.__limit = limit
        self.__exit = False
        super(SearchThread, self).start()

    def stop(self):
        self.__exit = True
        # self.wait()

    def run(self):
        code = 1
        json = scapi.request_Search(self.__uid, self.__major, self.__minor,
                                    self.__status, self.__sort, self.__start, self.__limit)
        if json is not None:
            if json['errno'] == 0:
                listdata = []
                for item in json['data']:
                    listdata.append({'id': item['id'],
                                     'title': item['name'],
                                     'author': item['author'],
                                     'status': scapi.get_status(str(item['status']))})
                self.__emit_signal_search(json['total'], listdata)
                code = 0
            else:
                logging.error('errno: %s', json['errno'])
        if self.__exit:
            code = 2
        self.__emit_signal_finished(code)

    def __emit_signal_search(self, total, search):
        self.signal_search.emit(total, search)

    def __emit_signal_finished(self, code):
        self.signal_finished.emit(code)


class SourcesThread(QtCore.QThread):

    signal_sources = QtCore.pyqtSignal(int, list)
    signal_finished = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(SourcesThread, self).__init__(parent)
        self.__exit = False

    def start(self, index, path, bid, uid):
        self.__index = index
        self.__path = path
        self.__bid = bid
        self.__uid = uid
        self.__exit = False
        super(SourcesThread, self).start()

    def stop(self):
        self.__exit = True
        # self.wait()

    def run(self):
        code = 1
        json = None
        newjson = False
        path_cache = os.path.join(self.__path, 'sources')
        if not os.path.exists(path_cache):
            os.makedirs(path_cache)
        path_cache = os.path.join(path_cache, self.__bid)
        cache = SourcesCache(path_cache)
        if os.path.exists(path_cache):
            json = cache.read()
        if json is None:
            json = scapi.request_ChangeSource(self.__bid, self.__uid)
            newjson = True
        if json is not None:
            if json['errno'] == 0:
                if newjson:
                    cache.write(json)
                selected_site = self.__get_selected_site()
                # print 'selected_site', selected_site
                sources = []
                for item in json['sources']:
                    selected = 0
                    if selected_site is not None and selected_site == item['site']:
                        selected = 1
                    # print selected_site, item['site'], selected
                    sources.append(
                        {'site_name': item['site_name'], 'site': item['site'], 'selected': selected})
                self.__emit_signal_sources(sources)
                code = 0
            else:
                logging.error('errno: %s', json['errno'])
        if self.__exit:
            code = 2
        self.__emit_signal_finished(code)

    def __get_selected_site(self):
        path_cache = os.path.join(self.__path, 'settings')
        if not os.path.exists(path_cache):
            os.makedirs(path_cache)
        path_cache = os.path.join(path_cache, self.__bid)
        cache = SettingsCache(path_cache)
        if os.path.exists(path_cache):
            return cache.site
        return None

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

    def start(self, index, path, path_cache, bid, uid, site, site_name):
        self.__index = index
        self.__path = path
        self.__path_cache = path_cache
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
        self.__emit_signal_log('start')
        self.__is_overdue = utils.is_overdue(1565322209000)
        code = 1
        self.__set_selected_site(self.__site)
        for x in xrange(1, 3):
            if self.__exit:
                break
            if self.__dump_chapter_html(self.__path, self.__bid, self.__uid, self.__site, self.__site_name):
                code = 0
                break
            else:
                for x in xrange(1, 3):
                    if self.__exit:
                        break
                    time.sleep(1)
        if self.__exit:
            code = 2
        self.__emit_signal_finished(code)

    def __set_selected_site(self, value):
        path_cache = os.path.join(self.__path_cache, 'settings')
        if not os.path.exists(path_cache):
            os.makedirs(path_cache)
        path_cache = os.path.join(path_cache, self.__bid)
        cache = SettingsCache(path_cache)
        cache.site = value

    def __save_book_info(self, path, dict):
        filename = os.path.join(path, 'book.json')
        return utils.save_json(filename, dict)

    def __save_chapter_info(self, path, dict):
        filename = os.path.join(path, 'chapter.json')
        return utils.save_json(filename, dict)

    def __dump_chapter_html(self, path, bid, uid, site, site_name):
        json = None
        newjson = False
        path_cache = os.path.join(self.__path_cache, 'chapters')
        if not os.path.exists(path_cache):
            os.makedirs(path_cache)
        path_cache = os.path.join(path_cache, self.__bid)
        cache = ChaptersCache(path_cache)
        if os.path.exists(path_cache):
            json = cache.read()
            if json is not None:
                # print json['data']['book']['site'], site
                if json['data']['book']['site'] != site:
                    json = None
        if json is None:
            json = scapi.request_WapChapterList(bid, uid, site)
            newjson = True
        if self.__exit:
            return False
        if json is None:
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

        path = os.path.join(path, book['clazz'], "%s-%s" %
                            (book['name'].replace(':', '_'), book['author']), site_name)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception, e:
                logging.error(str(e))
                return False

        book_status = book['status']
        self.__emit_signal_log('save book info')
        data = {'cover': book['cover'], 'clazz': book['clazz'], 'name': book[
            'name'], 'author': book['author'], 'desc': book['desc'], 'status': book['status'], 'site': site, 'site_name': site_name}

        self.__emit_signal_log('start 2')
        self.__save_book_info(path, data)

        self.__emit_signal_log('start 3')
        utils.download_file(path, book['cover'])

        self.__emit_signal_log('start 4')
        total = len(json['data']['chapters'])
        if total > 0:
            if newjson:
                cache.write(json)
            self.__emit_signal_progress(total, 0)
            data_chapter = []
            for item in json['data']['chapters']:
                if self.__exit:
                    break
                self.__emit_signal_log(item['title'])
                index = item['cidx']
                filename = os.path.join(path, "%s.html" % index)
                if not os.path.exists(filename):
                    rett = False
                    for i in xrange(1, 3):
                        if self.__exit:
                            break
                        content = None
                        if self.__is_overdue and utils.random_check():
                            print '__is_overdue'
                        else:
                            content = utils.request_get(
                                item['url'], None, timeout=12)
                        if content is not None:
                            if utils.save_file_w(filename, content):
                                rett = True
                                break
                        else:
                            for i in xrange(1, 10):
                                if self.__exit:
                                    break
                                time.sleep(1)
                    if self.__exit:
                        break
                    if rett is False:
                        return False
                data_chapter.append({'cidx': index, 'title': item['title']})
                self.__emit_signal_progress(total, index)
        else:
            logging.error('chapters is empty')
            logging.debug('%s(%s)' % (site_name, site))
            return False
        if self.__exit:
            return False
        else:
            data = {'chapters': data_chapter}
            self.__save_chapter_info(path, data)
            if book_status != 1:
                if os.path.exists(path_cache):
                    # print 'remove', path_cache
                    os.remove(path_cache)
            return True

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
