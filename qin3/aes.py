#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex
import base64
import urllib.parse
from utils import b

class aes(object):

    def __init__(self, key, iv, mode=AES.MODE_CBC):
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
        cryptor = AES.new(self.__key, self.__mode, self.__iv)
        return self._encode(cryptor.encrypt(self._pad(cryptor, plaintext)))

    def decrypt(self, ciphertext):
        cryptor = AES.new(self.__key, self.__mode, self.__iv)
        return self._unpad(cryptor.decrypt(self._decode(ciphertext)))


class aesReader(aes):

    def _encode(self, str):
        return base64.b64encode(str)

    def _decode(self, str):
        return base64.b64decode(str)


if __name__ == "__main__":
    key = b'Jsdfiahdjfieqtao'
    iv = Random.new().read(AES.block_size)
    ar = aesReader(key, iv)

    e = ar.encrypt('{"type":"玄幻","page":"2","gender":"male"}'.encode("utf-8"))
    print (e)

    e = urllib.parse.quote(e)
    print (e)
    
    e = urllib.parse.unquote(e)
    print (e)
    
    d = ar.decrypt(e).decode("utf-8")
    print (d)
    
    
    '''
    >>> hex(10) # 10进制转16进制
    '0xa'
    >>> oct(10) # 10进制转8进制
    '0o12'
    >>> chr(48) # ASCII转字符
    '0'
    >>> ord('a') # 字符转ASCII
    97
    '''

    '''
    # 限制为 0 <= x < 256
    bytes(10) # 指定长度的以零值填充的 bytes 对象
    # b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    bytes(range(20)) # 通过由整数组成的可迭代对象
    # b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b...'

    obj = (1, 2)
    bytes(obj) # 通过缓冲区协议复制现有的二进制数据
    # b'\x01\x02'

    bytes('hello', 'utf-8')
    # b'hello'
    '''