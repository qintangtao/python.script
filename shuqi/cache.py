#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from qin.cache import BaseCache


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
