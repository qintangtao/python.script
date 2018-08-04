#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from qin.cache import AESCache, ConfAESCache


class SourcesCache(AESCache):

    def __init__(self, path):
        super(SourcesCache, self).__init__(
            path, 'Jsdfiahdjfieqtao', '1237635217384736')


class ChaptersCache(AESCache):

    def __init__(self, path):
        super(ChaptersCache, self).__init__(
            path, 'Abdkiahdjfieqtao', '9856335217384736')


class SettingsCache(ConfAESCache):

    def __init__(self, path):
        super(SettingsCache, self).__init__(
            path, 'Abdkiahdjqinqtao', '9856335217386589')

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
