#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import DES3
from Crypto import Random
import es
import base64

PADDING_ZERO	=	0
PADDING_PKCS7	=	1
PADDING_ISO		=	2

class des(es.es):

    def __init__(self, key, iv, mode=DES3.MODE_CBC, padding=PADDING_ISO):    	
        self.__key = key
        self.__iv = iv
        self.__mode = mode
        super(des, self).__init__(DES3.block_size, padding)

    def _encrypt(self, plaintext):
        cryptor = DES3.new(self.__key, self.__mode, self.__iv)
        return cryptor.encrypt(plaintext)

    def _decrypt(self, plaintext):
        cryptor = DES3.new(self.__key, self.__mode, self.__iv)
        return cryptor.decrypt(plaintext)

class desReader(des):

    def _encode(self, ciphertext):
        return base64.b64encode(ciphertext)

    def _decode(self, ciphertext):
        return base64.b64decode(ciphertext)


if __name__ == "__main__":
    key = b'Sixteen byte key'
    iv = Random.new().read(DES3.block_size)
    dr = desReader(key, iv, DES3.MODE_ECB)
    e = dr.encrypt('{"type":"玄幻","page":"2","gender":"male"}'.encode("utf-8"))
    print (e)
    d = dr.decrypt(e).decode("utf-8")
    print (d)
