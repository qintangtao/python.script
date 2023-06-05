#!/usr/bin/python
# -*- coding: UTF-8 -*-
from binascii import b2a_hex, a2b_hex
from utils import b

PADDING_ZERO	=	0
PADDING_PKCS7	=	1
PADDING_ISO		=	2

class es(object):

    def __init__(self, block_size, padding):
        self._block_size = block_size
        self._padding = padding

    def _pad_ZERO(self, plaintext):
        padding_length = (self._block_size - len(plaintext) % self._block_size) % self._block_size
        if padding_length==0:
            return plaintext
        padded = plaintext + bytes(padding_length)
        return padded

    def _pad_PKCS7(self, plaintext):
        padding_length = (self._block_size - len(plaintext) % self._block_size) % self._block_size
        if padding_length==0:
            padding_length = self._block_size
        padded = plaintext + b(chr(padding_length))*padding_length
        return padded

    def _pad_ISO(self, plaintext):
        padding_length = (self._block_size - len(plaintext) % self._block_size) % self._block_size
        if padding_length==0:
            return plaintext
        padded = plaintext + b('\x80') + bytes(padding_length-1)
        return padded

    def _pad(self, plaintext):
        if self._padding == PADDING_ISO:
        	return self._pad_ISO(plaintext)
        elif self._padding == PADDING_PKCS7:
        	return self._pad_PKCS7(plaintext)
        else:
            return self._pad_ZERO(plaintext)

    def _unpad_ZERO(self, ciphertext):
    	length=len(ciphertext)
    	for i in reversed(range(length)):
    		if ciphertext[i] != 0:
    			break
    		length -= 1
    	return ciphertext[0:length]

    def _unpad_PKCS7(self, ciphertext):
    	return ciphertext[0:-ciphertext[-1]]

    def _unpad_ISO(self, ciphertext):
    	length=len(ciphertext)-1
    	for i in reversed(range(length+1)):
    		if ciphertext[i] != 0:
    			break
    		length -= 1
    	if ciphertext[length] == 128:
    		return ciphertext[0:length]
    	return ciphertext

    def _unpad(self, ciphertext):
    	if self._padding == PADDING_ISO:
    		return self._unpad_ISO(ciphertext)
    	elif self._padding == PADDING_PKCS7:
    		return self._unpad_PKCS7(ciphertext)
    	else:
            return self._unpad_ZERO(ciphertext)

    def _encode(self, ciphertext):
        return b2a_hex(ciphertext)

    def _decode(self, ciphertext):
        return a2b_hex(ciphertext)

    def _encrypt(self, plaintext):
        raise NotImplementedError('_encrypt: not implemented!')

    def _decrypt(self, ciphertext):
        raise NotImplementedError('_decrypt: not implemented!')

    def encrypt(self, plaintext):
        return self._encode(self._encrypt(self._pad(plaintext)))

    def decrypt(self, ciphertext):
        return self._unpad(self._decrypt(self._decode(ciphertext)))



if __name__ == "__main__":
    pass