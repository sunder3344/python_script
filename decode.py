#coding=utf-8

import base64
import binascii
from Crypto.Cipher import AES

def getKey(key):
    length = len(key)
    tmp = '0'
    data = ''
    if length < 32:
        surplus = 32 - length
        blank = tmp * surplus
        data = key + blank
    elif length > 32:
        data = key[0:32]
    else:
        data = key
    return data

def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]
        
def decrypt(enc, key):
#     enc = base64.b64decode(enc)
    enc = binascii.a2b_hex(enc)
    print(enc)
    iv = b'0000000000000000'
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return _unpad(cipher.decrypt(enc))



s = 'D6EQND4r26pvT6NXHJfB11DT2pC6Phj8q1mAfl9nwndPfXPf66SNqEQU+wMuRpQHZEbZ0URCdsBdKnfgltWk1FvBeAVkI2d7UiSbESlVF1prsQ7j2QqRzW3LdWOqpHC1YX5anO4wM6/rXB5J8oKNJ61i5H8LuF3hiW8ZKDaT7tc='
t = base64.b64decode(s)
oriKey = 'abcdef123456'
key = getKey(oriKey)
print(key)
res = decrypt(s, key)
print(res)
