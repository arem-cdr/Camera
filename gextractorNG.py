
import cv2
from cv2 import aruco
import numpy as np
import imutils

from imutils import contours




class NGExtractors(object):
    def  __init__(self,background):
        background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (21, 21), 0)
        self.back = background
    

    def draw(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # In each iteration, calculate absolute difference between current frame and reference frame
        difference = cv2.absdiff(gray, self.back)

        # Apply thresholding to eliminate noise
        thresh = cv2.threshold(difference, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        res = cv2.bitwise_and(img,img, mask= thresh)
        cv2.imshow('mask', res)
        cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
   