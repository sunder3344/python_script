#coding=utf-8

import time
import threading
from time import sleep
import time

def task1():
    print('Task 1 executed')
    sleep(1)
    
def task2():
    print('Task 2 executed')
    sleep(5)
    
if __name__ == '__main__':
    print('多线程')
    starttime = time.time()
    threads = []
    t1 = threading.Thread(target = task1)
    threads.append(t1)
    t2 = threading.Thread(target = task2)
    threads.append(t2)
    
    for t in threads:
        t.setDaemon(True)
        t.start()
    endtime = time.time()
    totaltime = endtime - starttime
    print('耗时：{0:.5f}秒' .format(totaltime))
    print('----------------------------------')
    
    print('单线程：')
    starttime = time.time()
    task1()
    task2()
    endtime = time.time()
    totaltime = endtime - starttime
    print('耗时：{0:.5f}秒' .format(totaltime))