
import time
import cv2

class DataExtractor(object):
    def  __init__(self, debug):
        self.red_gobelet = []
        self.green_gobelet = []
        self.to_trail = []
        self.robot = []
        self.debug = debug

    def log(self, dpoint, color, robot):
        """
            dpoint: Point objet corresponding to detected object.
            color: 0 == RED ; 1 == GREEN
            robot: 0 == NO ;  1 == YES
        """
        if(self.debug):
            self.to_trail.append(dpoint)
        if(robot):
            self.robot.append(dpoint)
        else:
            if(color):
                self.green_gobelet.append(dpoint)
            else:
                self.red_gobelet.append(dpoint)

    def clear(self):
        """
            Call before starting new frame !

        """
        self.red_gobelet = []
        self.green_gobelet = []
        self.robot = []

    def showTrails(self,img,decay_time):
        h = []
        for j in range(len(self.to_trail)):
            if( (time.time() - self.to_trail[j].t)<decay_time):
                cx = int(self.to_trail[j].x)
                cy = int(self.to_trail[j].y)
                center = (cx,cy)
                cv2.circle(img, center, 2, (0, 255, 255),2)
                h.append(self.to_trail[j])
        self.to_trail = h

    def showPos(self,img,conf):
        for j in range(len(self.red_gobelet)):
                px = int(self.red_gobelet[j].x)
                py = int(self.red_gobelet[j].y)
                pos= (px,py)
                cv2.circle(img, pos, 2, (0, 0, 255),2)
                h, w, channels = img.shape 
                x= int(px/w * conf.sizeXmm)
                y= int(py/h * conf.sizeYmm)
                cv2.putText(img, "x:{}, y:{}".format(x,y), (px,py-20),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 0, 159), 2)

        for j in range(len(self.green_gobelet)):
                px = int(self.green_gobelet[j].x)
                py = int(self.green_gobelet[j].y)
                pos= (px,py)
                cv2.circle(img, pos, 2, (0, 255, 0),2)
                h, w, channels = img.shape 
                x= int(px/w * conf.sizeXmm)
                y= int(py/h * conf.sizeYmm)
                cv2.putText(img, "x:{}, y:{}".format(x,y), (px,py-20),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 0, 159), 2)
        
        for j in range(len(self.robot)):
                px = int(self.robot[j].x)
                py = int(self.robot[j].y)
                pos= (px,py)
                cv2.circle(img, pos, 2, (255, 0, 255),2)
                h, w, channels = img.shape 
                x= int(px/w * conf.sizeXmm)
                y= int(py/h * conf.sizeYmm)
                cv2.putText(img, "x:{}, y:{}".format(x,y), (px,py-20),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 0, 159), 2)


class Point(object):
    def  __init__(self,x,y,t =None ):
        self.x = x
        self.y = y 
        if(t==None):
            self.t = time.time()
        else:
            self.t = t