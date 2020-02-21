import cv2


class CArea_Interest(object):
    def  __init__(self):
        self.interest = {}
        
    def add(self, letter, ipoint):
        self.interest[letter] = ipoint
    
    def check(self,letter):
        return self.interest[letter].hasChanged()


    
class IPoint(object):
    def  __init__(self,x,y,w,h):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
    def save(self,img):
        self.zone = img[int(self.y-self.h/2):int(self.y+self.h/2),int(self.x-self.w/2):int(self.x+self.w/2)]
    def hasChanged(self):
        pass
        