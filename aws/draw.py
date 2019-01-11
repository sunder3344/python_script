'''
Created on 2016年5月17日

@author: sunder3344
'''
#coding=utf-8
import time
import os
import re
import json
import urllib.request
import urllib.parse
import http.cookiejar
    
def fakeLogin():
    a = "我们去朱家角玩一天"
    res = re.findall(u'朱-角', a)
    print(len(res))
    print(res is None)

if __name__ == '__main__':
    fakeLogin()