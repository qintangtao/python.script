#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
import urllib


class aes(object):

    def __init__(self, key, iv, mode=AES.MODE_CBC):
        self.__key = key
        self.__iv = iv
        self.__mode = mode

    def _pad(self, str):
        return str + (AES.block_size - len(str) % AES.block_size) * chr(AES.block_size - len(str) % AES.block_size)

    def _unpad(self, str):
        return str[0:-ord(str[-1])]

    def _encode(self, str):
        return b2a_hex(str)

    def _decode(self, str):
        return a2b_hex(str)

    def encrypt(self, str):
        cryptor = AES.new(self.__key, self.__mode, self.__iv)
        return self._encode(cryptor.encrypt(self._pad(str)))

    def decrypt(self, str):
        cryptor = AES.new(self.__key, self.__mode, self.__iv)
        return self._unpad(cryptor.decrypt(self._decode(str)).rstrip('\0'))


class aesReader(aes):

    def _pad(self, str):
        return str + (AES.block_size - len(str) % AES.block_size) * chr(0)

    def _unpad(self, str):
        return str

    def _encode(self, str):
        return base64.b64encode(str)

    def _decode(self, str):
        return base64.b64decode(str)


if __name__ == "__main__":
    ar = aesReader('Jsdfiahdjfieqtao', '1237635217384736')
    e = ar.encrypt('{"type":"玄幻","page":"2","gender":"male"}')
    print e
    e = urllib.quote(e)
    print e
    e = urllib.unquote(e)
    print e
    d = ar.decrypt(e)
    print d
