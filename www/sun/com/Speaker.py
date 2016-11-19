'''
Created on 2016年4月26日

@author: bestv
'''

class Speaker():
    topic = ""
    name = ""

    def __init__(self, n, t):
        self.name = n
        self.topic = t
    
    def speak(self):
        print("I am %s, I am a speaker! My topic is %s"%(self.name, self.topic))
