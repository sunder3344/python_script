'''
Created on 2016年4月26日

@author: bestv
'''
from www.sun.com.People import People

class Student(People):
    grade = ""

    def __init__(self, n, a, w, g):
        People.__init__(self, n, a, w)
        self.grade = g
    
    def speak(self):
        print("%s is speaking: I am %d years old,and I am in grade %d"%(self.name,self.age,self.grade))
        
# s = Student('ken', 20, 60, 3)
# s.speak()