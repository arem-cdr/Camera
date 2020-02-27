
import cv2
import numpy as np
import imutils
from imutils import contours


class GExtractors(object):
    def  __init__(self):
       pass

    def extract(self,img,data,conf):
        b = 4
        diter = 5
        eiter = 1
        lowthreshold = 10

        h1 = 0
        s1 = 80
        v1 = 40

        h2 = 255
        s2 = 255
        v2 = 255
        
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,(h1,s1,v1),(h2,s2,v2))
        res = cv2.bitwise_and(img,img, mask= mask)
        cv2.imshow('mask', res)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (15,15), b)
        cv2.imshow('gaussianblur', gray)
        ratio = 3
        edged = cv2.Canny(gray, lowthreshold, lowthreshold*ratio)
        cv2.imshow('edged 1', edged)
        edged = cv2.dilate(edged, None, iterations=diter)
        edged = cv2.erode(edged, None, iterations=eiter)
        cv2.imshow('dilated + erode', edged)
        # find contours in the edge map
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE )
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
            h, w, channels = img.shape 
            data.log(Point(centerx,centery,h,w),color,robot)
        
        cv2.imshow('filtered + track', res)
       
    
    def debug_init(self,framename,framename1):
        cv2.namedWindow(framename)
        
        def on_b(val):
            pass

        cv2.createTrackbar("h1", framename , 0, 255, on_b)
        cv2.createTrackbar("s1", framename , 183, 255, on_b)
        cv2.createTrackbar("v1", framename , 0, 255, on_b)

        cv2.createTrackbar("h2", framename , 255,255, on_b)
        cv2.createTrackbar("s2", framename, 255, 255, on_b)
        cv2.createTrackbar("v2", framename, 182, 255, on_b)

        cv2.createTrackbar("blur", framename, 4, 10, on_b)
        cv2.namedWindow(framename1)
        cv2.createTrackbar("diter", framename1 , 5, 10, on_b)
        cv2.createTrackbar("eiter",framename1, 1, 10, on_b)
        cv2.createTrackbar("lowth", framename1 , 10, 100, on_b)

        cv2.createTrackbar("areamax", framename1, 8000, 10000, on_b)
        cv2.createTrackbar("areamin", framename1 , 3000, 10000, on_b)

    def debug(self,img,framename,framename1):
        b = cv2.getTrackbarPos("blur", framename)
        diter = cv2.getTrackbarPos("diter", framename1)
        eiter = cv2.getTrackbarPos("eiter", framename1)
        lowthreshold = cv2.getTrackbarPos("lowth", framename1)

        h1 = cv2.getTrackbarPos("h1", framename)
        s1 = cv2.getTrackbarPos("s1", framename)
        v1 = cv2.getTrackbarPos("v1", framename)

        h2 = cv2.getTrackbarPos("h2", framename)
        s2 = cv2.getTrackbarPos("s2", framename)
        v2 = cv2.getTrackbarPos("v2", framename)

        amax = cv2.getTrackbarPos("areamax", framename1)
        amin = cv2.getTrackbarPos("areamin", framename1)

        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,(h1,s1,v1),(h2,s2,v2))
        res = cv2.bitwise_and(img,img, mask= mask)
        cv2.imshow('mask', res)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (15,15), b)
        cv2.imshow('gaussianblur', gray)
        ratio = 3
        edged = cv2.Canny(gray, lowthreshold, lowthreshold*ratio)
        cv2.imshow('edged 1', edged)
        edged = cv2.dilate(edged, None, iterations=diter)
        edged = cv2.erode(edged, None, iterations=eiter)
        cv2.imshow('dilated + erode', edged)
        # find contours in the edge map
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE )
        cnts = imutils.grab_contours(cnts)
        # loop over the contours individually
        for c in cnts:
        
            if(cv2.contourArea(c) <amin):
                continue
            if(cv2.contourArea(c) >amax):
                continue
            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box) 
            box = np.array(box, dtype="int")
            cv2.drawContours(res, [box.astype("int")], -1, (0, 255, 0), 2)
        #cv2.drawContours(res, cnts, -1, (255,0,0), 3)
        cv2.imshow('filtered + track', res)


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