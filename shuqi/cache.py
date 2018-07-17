#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import utils
from prpcrypt import prpcrypt


def SourcesCache():

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
