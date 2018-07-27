#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64


def encrypt(key, data, length=100):
    data = data.encode(encoding="utf-8")
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    res = []
    for i in range(0, len(data), length):
        res.append(cipher.encrypt(data[i:i+length]))
    return base64.b64encode("".join(res))


def decrypt(key, data, length=128):
    data = base64.b64decode(data)
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    res = []
    for i in range(0, len(data), length):
        res.append(cipher.decrypt(data[i:i+length], "ERROR"))
    return "".join(res)


def generator(bits=1024):
    rsa = RSA.generate(bits, Random.new().read)
    return (rsa.exportKey(), rsa.publickey().exportKey())


def main():
    key = generator()
    print key
    d = encrypt(key[1], 'qintangtasdfadsfasdfasdao' * 100)
    print d
    print decrypt(key[0], d)


if __name__ == "__main__":
    main()
