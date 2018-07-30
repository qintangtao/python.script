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
            if os.path.exists(self._path):
                data = utils.read_file_r(self._path)
                if data is not None:
                    return self._decrypt(data)
        except Exception, e:
            logging.error(str(e))
        return None


if __name__ == "__main__":
    pass
