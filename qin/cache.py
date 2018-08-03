#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import logging
import aes
import utils


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
        except Exception, e:
            logging.error(str(e))
        return False

    def read(self):
        try:
            if os.path.exists(self._path):
                data = utils.read_file_r(self._path)
                if data is not None:
                    return self._decode(data)
        except Exception, e:
            logging.error(str(e))
        return None


class PrpcryptCache(JsonCache):

    def __init__(self, path, key, iv):
        super(PrpcryptCache, self).__init__(path)
        self._prpcrypt = aes.aes(key, iv)

    def _encode(self, dict):
        return self._prpcrypt.encrypt(super(PrpcryptCache, self)._encode(dict))

    def _decode(self, text):
        return super(PrpcryptCache, self)._decode(self._prpcrypt.decrypt(text))


class MemoryCache(JsonCache):

    def __init__(self, path):
        super(MemoryCache, self).__init__(path)
        data = super(MemoryCache, self).read()
        self.__dict__['__data__'] = {} if data is None else data

    def __del__(self):
        self.write(self.__dict__['__data__'])

    def __setattr__(self, name, value):
        if '__data__' in self.__dict__:
            self.__dict__['__data__'][name] = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if '__data__' in self.__dict__ and name in self.__dict__['__data__']:
            return self.__dict__['__data__'][name]
        return self.__dict__[name]


class MemoryPrpcryptCache(JsonCache):

    def __init__(self, path, key, iv):
        super(MemoryPrpcryptCache, self).__init__(path)
        self._prpcrypt = aes.aes(key, iv)
        data = super(MemoryPrpcryptCache, self).read()
        self.__dict__['__data__'] = {} if data is None else data

    def __del__(self):
        self.write(self.__dict__['__data__'])

    def __setattr__(self, name, value):
        if '__data__' in self.__dict__:
            self.__dict__['__data__'][name] = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if '__data__' in self.__dict__ and name in self.__dict__['__data__']:
            return self.__dict__['__data__'][name]
        return self.__dict__[name]

    def _encode(self, dict):
        return self._prpcrypt.encrypt(super(MemoryPrpcryptCache, self)._encode(dict))

    def _decode(self, text):
        return super(MemoryPrpcryptCache, self)._decode(self._prpcrypt.decrypt(text))

if __name__ == "__main__":
    c = MemoryCache(os.path.join(os.getcwd(), 'MemoryCache.json'))
    c.abc = 123
    print c.abc
    # print c.aaa
    print c.__dict__
