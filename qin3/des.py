#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import DES3
from Crypto import Random
from binascii import b2a_hex, a2b_hex
from utils import b
import base64
import urllib.parse


class des(object):

    def __init__(self, key, iv, mode=DES3.MODE_CBC):
        self.__key = key
        self.__iv = iv
        self.__mode = mode

    def _pad(self, cryptor, plaintext):
        padding_length = (cryptor.block_size - len(plaintext) % cryptor.block_size) % cryptor.block_size
        if padding_length==0:
            padding_length = cryptor.block_size
        padded = plaintext + b(chr(padding_length))*padding_length
        return padded

    def _unpad(self, ciphertext):
        return ciphertext[0:-ciphertext[-1]]

    def _encode(self, ciphertext):
        return b2a_hex(ciphertext)

    def _decode(self, ciphertext):
        return a2b_hex(ciphertext)

    def encrypt(self, plaintext):
        cryptor = DES3.new(self.__key, self.__mode, self.__iv)
        return self._encode(cryptor.encrypt(self._pad(cryptor, plaintext)))

    def decrypt(self, ciphertext):
        cryptor = DES3.new(self.__key, self.__mode, self.__iv)
        return self._unpad(cryptor.decrypt(self._decode(ciphertext)))


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
    e = urllib.parse.quote(e)
    print (e)
    e = urllib.parse.unquote(e)
    print (e)
    d = dr.decrypt(e).decode("utf-8")
    print (e)
