#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
from qin.prpcrypt import prpcrypt
from qin import utils


class SourcesCache():

    def __init__(self, path):
        self.__path = path
        self.__pc = prpcrypt('Jsdfiahdjfieqtao', '1237635217384736')

    def __encrypt(self, dict):
        return self.__pc.encrypt(json.dumps(dict))

    def __decrypt(self, text):
        return json.loads(self.__pc.decrypt(text))

    def write(self, dict):
        data = self.__encrypt(dict)
        return utils.save_file_w(self.__path, data)

    def read(self):
        data = utils.read_file_r(self.__path)
        if data is None:
            return None
        return self.__decrypt(data)

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'cache')
    c = SourcesCache(path)
