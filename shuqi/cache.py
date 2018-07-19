#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import logging
from qin.prpcrypt import prpcrypt
from qin import utils


class BaseCache(object):

    def __init__(self, path, key, iv):
        self._path = path
        self._prpcrypt = prpcrypt(key, iv)

    def _encrypt(self, dict):
        return self._prpcrypt.encrypt(json.dumps(dict))

    def _decrypt(self, text):
        return json.loads(self._prpcrypt.decrypt(text))

    def write(self, dict):
        try:
            data = self._encrypt(dict)
            return utils.save_file_w(self._path, data)
        except Exception, e:
            logging.error(str(e))
        return False

    def read(self):
        try:
            data = utils.read_file_r(self._path)
            if data is not None:
                return self._decrypt(data)
        except Exception, e:
            logging.error(str(e))
        return None


class SourcesCache(BaseCache):

    def __init__(self, path):
        super(SourcesCache, self).__init__(
            path, 'Jsdfiahdjfieqtao', '1237635217384736')


class ChaptersCache(BaseCache):

    def __init__(self, path):
        super(ChaptersCache, self).__init__(
            path, 'Abdkiahdjfieqtao', '9856335217384736')


class SettingsCache(BaseCache):

    def __init__(self, path):
        super(SettingsCache, self).__init__(
            path, 'Abdkiahdjqinqtao', '9856335217386589')
        data = super(SettingsCache, self).read()
        self._data = {} if data is None else data

    def __del__(self):
        self.write(self._data)

    def __setattr__(self, name, value):
        if '_data' in self.__dict__ and '_data' != name:
            self._data[name] = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self._data:
            return self._data[name]
        return None

if __name__ == "__main__":
    #path = os.path.join(os.getcwd(), 'cache')
    #c = SourcesCache(path)
    path = os.path.join(os.getcwd(), 'cache', 'settings')
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, '123456')
    cache = SettingsCache(path)
    print cache.__dict__
    print cache.asdf
    cache.asdf = 'asdfaaa'
    cache.abc = '123'
    print cache.abc
    print cache.__dict__
