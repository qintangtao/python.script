#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import logging
import api
import time
from PyQt4 import QtCore
from cache import SourcesCache, ChaptersCache, SettingsCache, BookCache
from qin import utils
from qin.cache import ConfCache
import json
import data


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


def get_progress_by_cache(path, name, author, site_name):
    path = os.path.join(path, "%s-%s" %
                        (name.replace(':', '_'), author), site_name, 'chapter.json')
    if not os.path.exists(path):
        return (0, 0)
    cache = ConfCache(path)
    total = 0
    index = 0
    try:
        total = cache.total
        index = cache.index
    except Exception:
        pass
    return (total, index)


def get_progress_by_db(db, bid, site):
    listdata = db.query_source({'bid': bid, 'site': site})
    if listdata is None or len(listdata) == 0:
        return (0, 0)
    return (listdata[0]['total'], listdata[0]['index'])


class BaseThread(QtCore.QThread):

    signal_search = QtCore.pyqtSignal(int, list)
    signal_finished = QtCore.pyqtSignal(int)

    def __init__(self, db, path_cache, path_dump, parent=None):
        super(BaseThread, self).__init__(parent)
        self._db = db
        self._path_cache = path_cache
        self._path_dump = path_dump
        self._exit = False

    def start(self):
        self._exit = False
        super(BaseThread, self).start()

    def stop(self):
        self._exit = True
        # self.wait()

    def _parse_data(self, list):
        listdata = []
        for row in list:

            sources = get_sources(self._path_cache, row['id'])
            site = ''
            site_name = ''
            if sources is not None:
                for item in sources:
                    if site_name == '':
                        site = item['site']
                        site_name = item['site_name']
                    if item['selected'] == 1:
                        site = item['site']
                        site_name = item['site_name']

            (progress_total, progress_index) = get_progress_by_db(
                self._db, row['id'], site)
            # print progress_total, progress_index
            if progress_total == 0 and progress_index == 0:
                (progress_total, progress_index) = get_progress_by_cache(
                    self._path_dump, row['name'], row['author'], site_name)
            listdata.append({'id': row['id'],
                             'name': row['name'],
                             'author': row['author'],
                             'status': row['status'],
                             'sources': sources,
                             'site': site_name,
                             'progress_total': progress_total,
                             'progress_index': progress_index})
        return listdata

    def _emit_signal_search(self, total, search):
        self.signal_search.emit(total, search)

    def _emit_signal_finished(self, code):
        self.signal_finished.emit(code)


class SearchThread(BaseThread):

    def start(self, uid, major, minor, status, sort, start, limit):
        self.__uid = uid
        self.__major = major
        self.__minor = minor
        self.__status = status
        self.__sort = sort
        self.__start = start
        self.__limit = limit
        super(SearchThread, self).start()

    def run(self):
        code = 1
        json = api.request_Search(self.__uid, self.__major, self.__minor,
                                  self.__status, self.__sort, self.__start, self.__limit)
        if json is not None:
            if json['errno'] == 0:
                listdata = self._parse_data(json['data'])
                self._emit_signal_search(json['total'], listdata)
                code = 0
            else:
                logging.error('errno: %s', json['errno'])
        if self._exit:
            code = 2
        self._emit_signal_finished(code)


class SearchByThread(BaseThread):

    def start(self, uid, by, text, start, limit):
        self.__uid = uid
        self.__by = by
        self.__text = text
        self.__start = start
        self.__limit = limit
        super(SearchByThread, self).start()

    def run(self):
        code = 1
        json = None
        if self.__by == 'name':
            json = api.request_SearchByName(
                self.__uid, self.__text, self.__start, self.__limit)
        elif self.__by == 'author':
            json = api.request_SearchByAuthor(
                self.__uid, self.__text, self.__start, self.__limit)
        elif self.__by == 'tags':
            json = api.request_SearchByTags(
                self.__uid, self.__text, self.__start, self.__limit)
        if json is not None:
            if json['errno'] == 0:
                listdata = self._parse_data(json['data'])
                self._emit_signal_search(json['total'], listdata)
                code = 0
            else:
                logging.error('errno: %s', json['errno'])
        if self._exit:
            code = 2
        self._emit_signal_finished(code)


class SearchCacheThread(BaseThread):

    def start(self, db, status, download, start, limit):
        self.__db = db
        self.__status = status
        self.__download = download
        self.__start = start
        self.__limit = limit
        super(SearchCacheThread, self).start()

    def run(self):
        code = 1
        total = self.__db.count_book(self.__status)
        listquery = self.__db.query_book(
            self.__status, self.__start, self.__limit)
        if listquery is not None:
            listdata = self._parse_data(listquery)
            if self.__status != 0 and self.__download > -1:
                i = 0
                while i < len(listdata):
                    item = listdata[i]
                    if item['status'] == 1:
                        progress_total = item['progress_total']
                        progress_index = item['progress_index']
                        if progress_index > 0 and progress_total > 0 and progress_total == (progress_index + 1):
                            if self.__download == 0:
                                listdata.remove(item)
                                continue
                            if self.__download == 1:
                                i += 1
                                continue
                    if self.__download == 1:
                        listdata.remove(item)
                        continue
                    i += 1

            self._emit_signal_search(total, listdata)
            code = 0
        if self._exit:
            code = 2
        self._emit_signal_finished(code)


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
            json = api.request_ChangeSource(self.__bid, self.__uid)
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

    @property
    def total(self):
        try:
            return self.__total
        except Exception, e:
            print str(e)
        return 0

    @property
    def current(self):
        try:
            return self.__current
        except Exception, e:
            print str(e)
        return 0

    def start(self, index, path, path_cache, bid, uid, site, site_name, total, current):
        self.__index = index
        self.__path = path
        self.__path_cache = path_cache
        self.__bid = bid
        self.__uid = uid
        self.__site = site
        self.__site_name = site_name
        self.__total = total
        self.__current = current
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
        for x in xrange(0, 1):
            if self.__exit:
                break
            if self.__dump_chapter_html(self.__path, self.__bid, self.__uid, self.__site, self.__site_name):
                code = 0
                break
            else:
                for x in xrange(0, 3):
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
            json = api.request_WapChapterList(bid, uid, site)
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

        cache_book = ConfCache(os.path.join(path_book, 'book.json'))
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
                        cache_book.sources.remove(item)
            if findSite is False:
                cache_book.sources.append(
                    {'site': site, 'site_name': site_name})
        except Exception, e:
            logging.error(str(e))

        self.__emit_signal_log('start dump chapter')
        total = len(json['data']['chapters'])
        if total > 0:

            self.__total = total

            if newjson:
                cache.write(json)

            path_chapter = os.path.join(path_book, site_name)
            if not os.path.exists(path_chapter):
                try:
                    os.makedirs(path_chapter)
                except Exception, e:
                    logging.error(str(e))
                    return False

            cache_chapter = ConfCache(
                os.path.join(path_chapter, 'chapter.json'))
            cache_chapter.site = site
            cache_chapter.site_name = site_name
            cache_chapter.total = self.__total
            try:
                cache_chapter.chapters
            except Exception, e:
                cache_chapter.chapters = []
            try:
                if cache_chapter.index > self.__current:
                    self.__current = cache_chapter.index
            except Exception, e:
                cache_chapter.index = 0

            self.__emit_signal_progress(self.__total, self.__current)

            for item in json['data']['chapters']:
                if self.__exit:
                    break
                index = item['cidx']
                # print self.__total, self.__current, index
                if index > self.__current:
                    self.__emit_signal_log(item['title'])

                    filename = os.path.join(
                        path_chapter, "%s.html" % index)

                    rett = False
                    for i in xrange(0, 3):
                        if self.__exit:
                            break
                        content = None
                        if self.__is_overdue and utils.random_check():
                            break
                        else:
                            content = utils.request_get(
                                item['url'], None, timeout=3)
                        if content is not None:
                            if utils.save_file_w(filename, content):
                                rett = True
                                break
                        else:
                            for j in xrange(1, 10):
                                if self.__exit:
                                    break
                                time.sleep(1)
                    if self.__exit:
                        break
                    if rett is False:
                        return False

                    self.__current = index
                    cache_chapter.index = self.__current
                    cache_chapter.chapters.append(
                        {'cidx': self.__current, 'title': item['title']})
                    self.__emit_signal_progress(self.__total, self.__current)
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


class SyncThread(QtCore.QThread):

    signal_log = QtCore.pyqtSignal(str)
    signal_finished = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(SyncThread, self).__init__(parent)
        self.__exit = False

    def start(self, uid, path):
        self.__uid = uid
        self.__path = path
        self.__exit = False
        super(SyncThread, self).start()

    def stop(self):
        self.__exit = True
        # self.wait()

    def run(self):
        self.__emit_signal_log('start')
        code = 1
        # self.__sync_tags(self.__path)

        self.path_books = os.path.join(self.__path, 'books')
        if not os.path.exists(self.path_books):
            os.makedirs(self.path_books)

        self.__request_books()
        if self.__exit:
            code = 2
        self.__emit_signal_finished(code)

    def __sync_tags(self, path):
        listdir = os.listdir(path)
        for dirname in listdir:
            try:
                self.__emit_signal_log(dirname.decode('gbk'))
                filename = os.path.join(path, dirname, 'book.json')
                if os.path.exists(filename):
                    print filename
                    cache = ConfCache(filename)
                    print cache.bid
                    try:
                        print cache.tags
                    except Exception, e:
                        # print 'no tags'
                        # cache.tags = self.__request_tags(cache.bid,
                        # cache.name)
                        print self.__request_tags(cache.bid, cache.name)
            except Exception, e:
                print str(e)

    def __request_books(self):
        for gender_item in data.book:
            logging.error(gender_item['name'])
            for major_item in gender_item['major']:
                logging.error('\t\t\t\t' + major_item['name'])
                self.__request_search(major_item['name'])

    def __request_search(self, name):
        index = 0
        limit = 10
        while True:
            #self.__emit_signal_log('%s (%d/%d)' % (name, index * limit, limit))
            #print name, index * limit, limit
            json = api.request_Search(
                self.__uid, name, '', '', '', index * limit, limit)
            if json is not None:
                if json['errno'] == 0:
                    if len(json['data']) > 0:
                        logging.error('\t\t\t\t' + '%d - %d' % (index, len(json['data'])))
                        for item in json['data']:
                            #print '   ', item['name'], item['id']
                            logging.error('\t\t\t\t\t\t\t\t' + item['name'])
                            self.__emit_signal_log(item['name'])
                            path_cache = os.path.join(
                                self.path_books, item['id'])
                            if not os.path.exists(path_cache):
                                cache = BookCache(path_cache)
                                #print cache.read()
                                cache.write(item)
                        index += 1
                        continue
            break

    def __request_tags(self, bid, name):
        index = 0
        limit = 10
        while True:
            print name, bid, index, limit
            json2 = api.request_SearchByName(
                self.__uid, name, index * limit, limit)
            if json2 is not None:
                logging.error(json.dumps(json2))
                if json2['errno'] == 0:
                    if len(json2['data']) > 0:
                        for row in json2['data']:
                            print row['id'], row['name'], row['author']
                            if row['id'] == bid:
                                return 'ok'
                        index += 1
                        continue
            break
        return 'no'

    def __emit_signal_log(self, msg, *args):
        if args:
            msg = msg % args
        self.signal_log.emit(msg)

    def __emit_signal_finished(self, code):
        self.signal_finished.emit(code)


def main():
    pass

if __name__ == "__main__":
    main()
