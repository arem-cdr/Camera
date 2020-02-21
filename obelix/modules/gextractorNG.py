
import cv2
import numpy as np
import imutils
from modules.dextractor import *
from imutils import contours





class NGExtractors(object):
    def  __init__(self,conf,background):
        if(not(conf.back)):
            background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
            background = cv2.GaussianBlur(background, (21, 21), 0)
            cv2.imwrite(conf.background, background) 
        else:
            background = cv2.imread(conf.background) 
        self.back = background
    

    def extract(self,img,data,conf):
        """
            Input BGR img
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # In each iteration, calculate absolute difference between current frame and reference frame
        difference = cv2.absdiff(gray, self.back)

        # Apply thresholding to eliminate noise
        thresh = cv2.threshold(difference, conf.threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        res = cv2.bitwise_and(img,img, mask= thresh)



        ###############################################################
        ## FIND OBJECTS 
        cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours individually
        for c in cnts:
            if(cv2.contourArea(c) <conf.size_min):
                continue
            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box) 
            box = np.array(box, dtype="int")
            cv2.drawContours(res, [box.astype("int")], -1, (0, 255, 0), 2)

            # Color ?
            cX = np.average(box[:, 0])
            cY = np.average(box[:, 1]) 
            colors = (img[int(cY),int(cX)])
            color = colors[1]>colors[2]

            # Exact center calcul ?
            k = doubleminBox(box)
            fmin= k[0]
            smin = k[1]
            teta = np.arctan2(smin[1]-fmin[1],smin[0]-fmin[0])
            xmid = (fmin[0]+smin[0])/2 
            ymid = (fmin[1]+smin[1])/2
            proportion = conf.obj_center_ratio
            k = getHW(box)
            h = k[0]
            w = k[1]
            
            xdelta = -np.sin(teta)*proportion*h
            ydelta = np.cos(teta)*proportion*h
            if(teta<np.pi/2):
                xdelta = -xdelta
                ydelta = -ydelta
            centerx =  xmid+xdelta
            centery = ymid + ydelta

            # Is robot ?
            robot = 0
            robot_area = conf.size_min_robot
            if(cv2.contourArea(c)>robot_area):
                robot = 1

            # Exporting info
            data.log(Point(centerx,centery),color,robot)
      
        return res


def dist(p1,p2):
    return np.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)

def getHW(box):
    l = []
    plast = box[0]
    for p in box:
        l.append(dist(plast,p))
        plast = p
    l.pop()
    u= [np.max(l),np.min(l)]
    return u

        

def doubleminBox(box):
    b1 = box[0]
    b1y = box[0][1]
    b2 = box[1]
    b2y = box[1][1]
    for i in range(2,4):
        p = box[i]
        if(p[1]>b1y & p[1]>b2y):
            if(p[1]>b1y):
                b1y = p[1]
                b1 = p
            else:
                b2y = p[1]
                b2 = p
        if(p[1]>b2y):
            b2y = p[1]
            b2 = p
        if(p[1]>b1y):
            b1y = p[1]
            b1 = p
        i+=1
    if(b1y>b2y):
        b1,b2 = b2,b1
    k = [b1,b2]
    return k