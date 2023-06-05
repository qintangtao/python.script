#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import AES
from Crypto import Random
import base64
import es

PADDING_ZERO	=	0
PADDING_PKCS7	=	1
PADDING_ISO		=	2

class aes(es.es):

    def __init__(self, key, iv, mode=AES.MODE_CBC, padding=PADDING_ISO):    	
        self.__key = key
        self.__iv = iv
        self.__mode = mode
        super(aes, self).__init__(AES.block_size, padding)

    def _encrypt(self, plaintext):
        cryptor=AES.new(self.__key, self.__mode, self.__iv)
        return cryptor.encrypt(plaintext)

    def _decrypt(self, ciphertext):
        cryptor=AES.new(self.__key, self.__mode, self.__iv)
        return cryptor.decrypt(ciphertext)

class aesReader(aes):

    def _encode(self, ciphertext):
    	return base64.b64encode(ciphertext)

    def _decode(self, ciphertext):
        return base64.b64decode(ciphertext)


if __name__ == "__main__":
    key = b'Jsdfiahdjfieqtao'
    iv = Random.new().read(AES.block_size)
    ar = aesReader(key, iv, padding=PADDING_ISO)
    e = ar.encrypt('{"type":"玄幻","page":"2","gender":"male"}'.encode("utf-8"))
    print (e)
    d = ar.decrypt(e).decode("utf-8")
    print (d)

'''
    data = "中文测试用例"
    data = data.encode("utf-8")
    print(type(data), data)
    data = b2a_hex(data)
    print(type(data), data)
    data = data.decode(encoding='utf-8')
    print(type(data), data)
    
    data = data.encode("utf-8")
    #text = a2b_hex('e4b8ade69687e6b58be8af95e794a8e4be8b')
    text = a2b_hex(data)
    print(type(text), text)
    text = text.decode(encoding='utf-8')
    print(type(text), text)



    
    >>> hex(10) # 10进制转16进制
    '0xa'
    >>> oct(10) # 10进制转8进制
    '0o12'
    >>> chr(48) # ASCII转字符
    '0'
    >>> ord('a') # 字符转ASCII
    97
 

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