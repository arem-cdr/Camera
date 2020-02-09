import cv2


class CPixel_Interest(object):
    def  __init__(self):
        self.interest = {}
        
    def add(self, letter, ipoint):
        self.interest[letter] = ipoint
    
    def check(self,letter):
        pass


    
class IPoint(object):
    def  __init__(self,x,y):
        self.x = x
        self.y = y 
        