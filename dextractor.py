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
            vx = (p[i+1].x-p[i].x)/(p[i+1].t-p[i].t)
            vy = (p[i+1].y-p[i].y)/(p[i+1].t-p[i].t)
            vp = Point(vx,vy,p[i+1].t)
            v.append(vp)
            pass   
        v.append(0)
        return v

    def plotvelocity(self,arucoid):
        v = self.genVelocity(arucoid)
        t =  [x.t for x in v]
        plt.plot(t,v)
        plt.show()
        

    def recordposition(self,arucoid):
        self.records[str(arucoid)] = []
        

    def plotpositions(self,arucoid):
        p = self.records["p"+str(arucoid)]    
       


class Point(object):
    def  __init__(self,x,y,t =None ):
        self.x = x
        self.y = y 
        if(t==None):
            self.t = datetime.datetime.now()
        else:
            self.t = t