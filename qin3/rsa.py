#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.Util.number import ceil_div
import Crypto.Util.number
import base64

def __get_max_length(key, encrypt=True):
    modBits = Crypto.Util.number.size(key.n)
    k = ceil_div(modBits,8) # Convert from bits to bytes
    if encrypt:
        k = k-11
    return k
    
def encrypt(externKey, message):
    h = SHA.new(message)
    key = RSA.importKey(externKey)
    length = __get_max_length(key)
    cipher = Cipher_pkcs1_v1_5.new(key)
    ciphertext = bytes()
    for i in range(0, len(message), length):
        ciphertext += cipher.encrypt(message[i:i+length])
    return base64.b64encode(ciphertext)


def decrypt(externKey, ciphertext):
    ciphertext = base64.b64decode(ciphertext)
    key = RSA.importKey(externKey)
    length = __get_max_length(key, False)
    cipher = Cipher_pkcs1_v1_5.new(key)
    message = bytes()
    for i in range(0, len(ciphertext), length):
        message += cipher.decrypt(ciphertext[i:i+length], "ERROR")
    return message
    

def generator(bits=1024):
    rsa = RSA.generate(bits, Random.new().read)
    return (rsa.exportKey(), rsa.publickey().exportKey())


def main():
    key = generator()
    print(key)
    message = 'qintangtasd中国fadsfasdfasdaaa123123o' * 2
    e = encrypt(key[1], message.encode("utf-8"))
    print(e)
    d = decrypt(key[0], e).decode("utf-8")
    print(d)


if __name__ == "__main__":
    main()
