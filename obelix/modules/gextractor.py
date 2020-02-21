
import cv2
from cv2 import aruco
import numpy as np
import imutils
from imutils import contours




class GExtractors(object):
    def  __init__(self):
       pass

    def draw(self,img):
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
        
            if(cv2.contourArea(c) <3000):
                continue
            if(cv2.contourArea(c) >8000):
                continue
            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box) 
            box = np.array(box, dtype="int")
            cv2.drawContours(res, [box.astype("int")], -1, (0, 255, 0), 2)
        #cv2.drawContours(res, cnts, -1, (255,0,0), 3)
        cv2.imshow('filtered + track', res)
       
    
    def get(self,img):
        pass
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