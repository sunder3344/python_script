'''
Created on 2016年4月26日

@author: sunder3344
'''

class People(object):
    name = ""
    age = 0
    __weight = 0

    def __init__(self, n, a, w):
        self.name = n
        self.age = a
        self.__weight = w
        
    def speak(self):
        print("%s is speeking: I am %d years old"%(self.name, self.age))
        

# p = People('tom', 10, 30)
# p.speak()