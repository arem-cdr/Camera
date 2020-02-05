
import datetime

class DataExtractor(object):
    def  __init__(self):
       self.red_goblet = []
       self.green_goblet = []
       self.fallen_goblet = []
       self.allies = []
       self.enemies = []
       self.records = {}

class Point(object):
    def  __init__(self,x,y,t =None ):
        self.x = x
        self.y = y 
        if(t==None):
            self.t = datetime.datetime.now()
        else:
            self.t = t