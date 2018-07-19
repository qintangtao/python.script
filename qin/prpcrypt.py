#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class prpcrypt():

    def __init__(self, key, iv):
        self.__key = key
        self.__iv = iv
        self.__mode = AES.MODE_CBC
        self.__pad = lambda s: s + \
            (AES.block_size - len(s) % AES.block_size) * \
            chr(AES.block_size - len(s) % AES.block_size)
        self.__unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        cryptor = AES.new(self.__key, self.__mode, self.__iv)
        return b2a_hex(cryptor.encrypt(self.__pad(text)))

    def decrypt(self, text):
        cryptor = AES.new(self.__key, self.__mode, self.__iv)
        return self.__unpad(cryptor.decrypt(a2b_hex(text)).rstrip('\0'))

if __name__ == "__main__":
    pc = prpcrypt('Jsdfiahdjfieqtao', '1237635217384736')
    e = pc.encrypt('qintangadsfadsfasdftao')
    d = pc.decrypt(e)
    print 'e:', e, 'd:', d
