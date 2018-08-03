#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex
import base64
import utils
import os
import urllib


class des(object):

    def __init__(self, key, iv, mode=DES.MODE_CBC):
        self.__key = key
        self.__iv = iv
        self.__mode = mode

    def _pad(self, str):
        return str + (DES.block_size - len(str) % DES.block_size) * chr(DES.block_size - len(str) % DES.block_size)

    def _unpad(self, str):
        return str[0:-ord(str[-1])]

    def _encode(self, str):
        return b2a_hex(str)

    def _decode(self, str):
        return a2b_hex(str)

    def encrypt(self, str):
        cryptor = DES.new(self.__key, self.__mode, self.__iv)
        return self._encode(cryptor.encrypt(self._pad(str)))

    def decrypt(self, str):
        cryptor = DES.new(self.__key, self.__mode, self.__iv)
        return self._unpad(cryptor.decrypt(self._decode(str)).rstrip('\0'))


class desReader(des):

    def _pad(self, str):
        return str + (DES.block_size - len(str) % DES.block_size) * chr(0)

    def _unpad(self, str):
        return str

    def _encode(self, str):
        return base64.b64encode(str)

    def _decode(self, str):
        return base64.b64decode(str)


if __name__ == "__main__":
    pc = desReader('readBook', 'readBook', DES.MODE_ECB)
    e = pc.encrypt('{"type":"玄幻","page":"2","gender":"male"}')
    print e
    e = urllib.quote(e)
    print e
    e = urllib.unquote(e)
    print e
    d = pc.decrypt(e)
    print d
    utils.save_file_w(os.path.join(os.getcwd(), 'a.json'), d)
