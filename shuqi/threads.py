#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import logging
import scapi
import time
from PyQt4 import QtCore
from cache import SourcesCache, ChaptersCache, SettingsCache
from qin import utils
from qin.cache import MemoryCache


def set_selected_site(path, bid, value):
    path = os.path.join(path, 'settings')
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, bid)
    cache = SettingsCache(path)
    cache.site = value


def get_selected_site(path, bid):
    try:
        path = os.path.join(path, 'settings', bid)
        if os.path.exists(path):
            cache = SettingsCache(path)
            return cache.site
    except Exception, e:
        logging.error(str(e))
    return None


def get_sources(path, bid):
    root_path = path
    path = os.path.join(root_path, 'sources', bid)
    if not os.path.exists(path):
        return None

    cache = SourcesCache(path)
    json = cache.read()
    if json is None:
        return None

    if json['errno'] != 0:
        return None

    selected_site = get_selected_site(root_path, bid)
    sources = []
    for item in json['sources']:
        selected = 0
        if selected_site is not None and selected_site == item['site']:
            selected = 1
        sources.append({'site_name': item['site_name'], 'site': item[
                       'site'], 'selected': selected})
    return sources


def get_progress(path, name, author, site_name):
    path = os.path.join(path, "%s-%s" %
                        (name.replace(':', '_'), author), site_name, 'chapter.json')
    if not os.path.exists(path):
        return (0, 0)
    cache = MemoryCache(path)
    total = 0
    index = 0
    try:
        total = cache.total
        index = cache.index
    except Exception:
        pass
    return (total, index)


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


class SearchByThread(QtCore.QThread):

    signal_search = QtCore.pyqtSignal(int, list)
    signal_finished = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(SearchByThread, self).__init__(parent)
        self.__exit = False

    def start(self, uid, by, text, start, limit):
        self.__uid = uid
        self.__by = by
        self.__text = text
        self.__start = start
        self.__limit = limit
        self.__exit = False
        super(SearchByThread, self).start()

    def stop(self):
        self.__exit = True
        # self.wait()

    def run(self):
        code = 1
        json = None
        if self.__by == 'name':
            json = scapi.request_SearchByName(
                self.__uid, self.__text, self.__start, self.__limit)
        elif self.__by == 'author':
            json = scapi.request_SearchByAuthor(
                self.__uid, self.__text, self.__start, self.__limit)
        elif self.__by == 'tags':
            json = scapi.request_SearchByTags(
                self.__uid, self.__text, self.__start, self.__limit)
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


class SearchCacheThread(QtCore.QThread):

    signal_search = QtCore.pyqtSignal(int, list)
    signal_finished = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(SearchCacheThread, self).__init__(parent)
        self.__exit = False

    def start(self, path_cache, path_dump, db, status, start, limit):
        self.__path_cache = path_cache
        self.__path_dump = path_dump
        self.__db = db
        self.__status = status
        self.__start = start
        self.__limit = limit
        self.__exit = False
        super(SearchCacheThread, self).start()

    def stop(self):
        self.__exit = True
        # self.wait()

    def run(self):
        code = 1
        total = self.__db.count(self.__status)
        cursor = self.__db.query(self.__status, self.__start, self.__limit)
        if cursor is not None:
            listdata = []
            for row in cursor:
                sources = get_sources(self.__path_cache, row[0])
                site_name = ''
                if sources is not None:
                    for item in sources:
                        if site_name == '':
                            site_name = item['site_name']
                        if item['selected'] == 1:
                            site_name = item['site_name']
                (progress_total, progress_index) = get_progress(
                    self.__path_dump, row[1], row[2], site_name)
                listdata.append({'id': row[0],
                                 'title': row[1],
                                 'author': row[2],
                                 'status': scapi.get_status(str(row[3])),
                                 'sources': sources,
                                 'site': site_name,
                                 'status_number': row[3],
                                 'progress_total': progress_total,
                                 'progress_index': progress_index})
            self.__emit_signal_search(total, listdata)
            code = 0
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
                selected_site = get_selected_site(self.__path, self.__bid)
                sources = []
                for item in json['sources']:
                    selected = 0
                    if selected_site is not None and selected_site == item['site']:
                        selected = 1
                    sources.append(
                        {'site_name': item['site_name'], 'site': item['site'], 'selected': selected})
                self.__emit_signal_sources(sources)
                code = 0
            else:
                logging.error('errno: %s', json['errno'])
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
        set_selected_site(self.__path_cache, self.__bid, self.__site)
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

        path_book = os.path.join(
            path, "%s-%s" % (book['name'].replace(':', '_'), book['author']))
        if not os.path.exists(path_book):
            try:
                os.makedirs(path_book)
            except Exception, e:
                logging.error(str(e))
                return False

        self.__emit_signal_log('download cover.')
        utils.download_file(path_book, book['cover'])

        cache_book = MemoryCache(os.path.join(path_book, 'book.json'))
        cache_book.bid = bid
        cache_book.cover = book['cover']
        cache_book.clazz = book['clazz']
        cache_book.name = book['name']
        cache_book.author = book['author']
        cache_book.desc = book['desc']
        cache_book.status = book['status']
        cache_book.site = site
        cache_book.site_name = site_name

        try:
            cache_book.sources
        except Exception:
            cache_book.sources = [{'site': site, 'site_name': site_name}]

        try:
            findSite = False
            for item in cache_book.sources:
                if site == item['site']:
                    findSite = True
                else:
                    if not os.path.exists(os.path.join(path_book, item['site_name'])):
                        print 'remove', item['site_name']
                        cache_book.sources.remove(item)
            if findSite is False:
                cache_book.sources.append(
                    {'site': site, 'site_name': site_name})
        except Exception, e:
            logging.error(str(e))

        self.__emit_signal_log('start dump chapter')
        total = len(json['data']['chapters'])
        if total > 0:

            logging.info(str(json))
            if newjson:
                cache.write(json)

            path_chapter = os.path.join(path_book, site_name)
            if not os.path.exists(path_chapter):
                try:
                    os.makedirs(path_chapter)
                except Exception, e:
                    logging.error(str(e))
                    return False

            cache_chapter = MemoryCache(
                os.path.join(path_chapter, 'chapter.json'))
            cache_chapter.site = site
            cache_chapter.site_name = site_name
            cache_chapter.total = total
            cache_chapter.index = 0
            cache_chapter.chapters = []

            self.__emit_signal_progress(
                cache_chapter.total, cache_chapter.index)
            for item in json['data']['chapters']:
                if self.__exit:
                    break

                self.__emit_signal_log(item['title'])
                index = item['cidx']
                filename = os.path.join(path_chapter, "%s.html" % index)
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

                cache_chapter.index = index
                cache_chapter.chapters.append(
                    {'cidx': index, 'title': item['title']})
                self.__emit_signal_progress(total, index)
        else:
            logging.error('chapters is empty')
            logging.debug('%s(%s)' % (site_name, site))
            return False
        if self.__exit:
            return False
        else:
            if book['status'] != 1:
                if os.path.exists(path_cache):
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
