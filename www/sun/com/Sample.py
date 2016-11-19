'''
Created on 2016年4月26日

@author: bestv
'''
from www.sun.com.Speaker import Speaker
from www.sun.com.Student import Student

class Sample(Speaker, Student):
    a = ""

    def __init__(self, n, a, w, g, t):
        Student.__init__(self, n, a, w, g)
        Speaker.__init__(self, n, t)