'''
Created on 2016年5月17日

@author: bestv
'''
#coding=utf-8
import aiml
import os

def run():
    os.chdir('./alice')
    alice = aiml.Kernel()
    alice.learn('startup.xml')
    alice.respond('LOAD ALICE')


if __name__ == '__main__':
    run()