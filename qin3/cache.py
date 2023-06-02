#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import logging
import aes
import utils
from atexit import register
from Crypto import Random
from Crypto.Cipher import AES

class JsonCache(object):

    def __init__(self, path):
        self._path = path

    def _encode(self, dict):
        return json.dumps(dict)

    def _decode(self, text):
        return json.loads(text)

    def write(self, dict):
        try:
            data = self._encode(dict)
            return utils.save_file_w(self._path, data)
        except Exception as e:
            logging.error(str(e))
        return False

    def read(self):
        try:
            if os.path.exists(self._path):
                data = utils.read_file_r(self._path)
                if data is not None:
                    return self._decode(data)
        except Exception as e:
            logging.error(str(e))
        return None


class AESCache(JsonCache):

    def __init__(self, path, key, iv):
        super(AESCache, self).__init__(path)
        self._aes = aes.aes(key, iv)

    def _encode(self, dict):
        return self._aes.encrypt(super(AESCache, self)._encode(dict).encode("utf-8"))

    def _decode(self, text):
        return super(AESCache, self)._decode(self._aes.decrypt(text)).decode("utf-8")


class ConfCache(JsonCache):

    def __init__(self, path):
        super(ConfCache, self).__init__(path)
        data = super(ConfCache, self).read()
        self.__dict__['__data__'] = {} if data is None else data
        register(self._del)

    def __del__(self):
        pass

    def __setattr__(self, name, value):
        if '__data__' in self.__dict__:
            self.__dict__['__data__'][name] = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if '__data__' in self.__dict__ and name in self.__dict__['__data__']:
            return self.__dict__['__data__'][name]
        return self.__dict__[name]

    def _del(self):
        self.write(self.__dict__['__data__'])

    def getattr(self, name, default=None):
        try:
            return getattr(self, name)
        except Exception:
            return default


class ConfAESCache(JsonCache):

    def __init__(self, path, key, iv):
        super(ConfAESCache, self).__init__(path)
        self._aes = aes.aes(key, iv)
        data = super(ConfAESCache, self).read()
        self.__dict__['__data__'] = {} if data is None else data
        register(self._del)

    def __del__(self):
        pass

    def __setattr__(self, name, value):
        if '__data__' in self.__dict__:
            self.__dict__['__data__'][name] = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if '__data__' in self.__dict__ and name in self.__dict__['__data__']:
            return self.__dict__['__data__'][name]
        return self.__dict__[name]

    def _del(self):
        self.write(self.__dict__['__data__'])

    def _encode(self, dict):
        return self._aes.encrypt(super(ConfAESCache, self)._encode(dict).encode("utf-8")).decode("utf-8")

    def _decode(self, text):
        return super(ConfAESCache, self)._decode(self._aes.decrypt(text)).decode("utf-8")

    def getattr(self, name, default=None):
        try:
            return getattr(self, name)
        except Exception:
            return default

def testConfCache():
    path=os.path.join(os.getcwd(), 'ConfCache.json')
    c = ConfCache(path)
    c.abc = 123
    c.aa= 'aaaaaaaaaaa'
    c.bb = True
    print (c.abc)
    print (c.__dict__)

def testConfAESCache():
    path=os.path.join(os.getcwd(), 'ConfAESCache.json')
    key = b'Jsdfiahdjfieqtao'
    iv = Random.new().read(AES.block_size)
    c = ConfAESCache(path, key, iv)
    c.abc = 123
    c.aa= 'aaaaaaaaaaa'
    c.bb = True
    print (c.abc)
    print (c.__dict__)

if __name__ == "__main__":
    testConfCache()
    testConfAESCache()
