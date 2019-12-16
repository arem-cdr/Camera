import matplotlib.pyplot as plt
import datetime

class DataExtractor(object):
    def  __init__(self):
       self.red_goblet = []
       self.green_goblet = []
       self.fallen_goblet = []
       self.allies = []
       self.enemies = []
       self.records = {}

    def visualize(self):
        pass
    def genVelocity(self,arucoid):
        p = self.records[str(arucoid)]
        v = [0]
        for i in range(1,len(p)-1):
            pass   

        return v

    def plotvelocity(self,arucoid):
        v = self.genVelocity(arucoid)
        plt.plot(v)
        plt.show()
        

    def recordposition(self,arucoid):
        self.records[str(arucoid)] = []
        

    def plotpositions(self,arucoid):
        p = self.records["p"+str(arucoid)]    
       


class Point(object):
    def  __init__(self,x,y):
        self.x = x
        self.y = y 
        self.t = datetime.datetime.now()