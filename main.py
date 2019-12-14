from scipy.spatial import distance as dist
import numpy as np
import cv2
import imutils
from imutils import perspective
from imutils import contours
from cv2 import aruco
import math  
import yaml 
from calibrator import *
from track import *

# Here we build the code that calls other scripts to do all the work



b = 4
lowthreshold = 10
diter = 5
eiter = 1
cv2.namedWindow("real")
def on_b(val):
    pass

cv2.createTrackbar("h1", "real" , 0, 255, on_b)
cv2.createTrackbar("s1", "real" , 80, 255, on_b)
cv2.createTrackbar("v1", "real" , 40, 255, on_b)

cv2.createTrackbar("h2", "real" , 255,255, on_b)
cv2.createTrackbar("s2", "real" , 255, 255, on_b)
cv2.createTrackbar("v2", "real" , 255, 255, on_b)

cv2.createTrackbar("blur", "real" , 4, 10, on_b)
cv2.createTrackbar("diter", "real" , 5, 10, on_b)
cv2.createTrackbar("eiter", "real" , 1, 10, on_b)
cv2.createTrackbar("lowth", "real" , 10, 100, on_b)

def main():
    # Opening data stream
    cap = cv2.VideoCapture("raw/v14.MOV")
    sizex =1/2
    sizey =1/2

    # Loading data from config.yml
    raw = ""
    with open("config.yml", 'r') as ymlfile:
        raw = yaml.load(ymlfile)
    
    calculated = False
    sizeXmm = raw['sizeXmm']
    sizeYmm = raw['sizeYmm']
    matrix = raw['matrix']

    # Generating Calibration object
    calibobj = Calib(13,11,15,14,sizeXmm*10,sizeYmm*10) 

    # Loading perspective correction matrix from file if exits
    if(matrix ==1):
        calibobj.M = np.load(raw['matrix_file'])
        i = 40
        calculated = True

    # Generating tracker object
    trak = Tracker() 

    i = 0
    while(cap.isOpened()):
        b = cv2.getTrackbarPos("blur", "real" )
        diter = cv2.getTrackbarPos("diter", "real")
        eiter = cv2.getTrackbarPos("eiter", "real" )
        lowthreshold = cv2.getTrackbarPos("lowth", "real" )

        h1 = cv2.getTrackbarPos("h1", "real")
        s1 = cv2.getTrackbarPos("s1", "real" )
        v1 = cv2.getTrackbarPos("v1", "real" )

        h2 = cv2.getTrackbarPos("h2", "real")
        s2 = cv2.getTrackbarPos("s2", "real" )
        v2 = cv2.getTrackbarPos("v2", "real" )
        # Reading frame from stream
        ret, frame = cap.read()
        if(not(frame.any())):
            continue
        # Resizing image
        resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey) 

        # Checking if we have calculate perspective correction matrxix
        if(not(calculated) | (i<40)):

            # Calculating perspective correction matrix and saving it
            result = calibobj.genCalibration(resized)
            calculated = result
            if(calculated):
                calibobj.saveMat()

        if calculated:

            # Applying perspective correction matrix to frame
            warped = calibobj.applyCalibration(resized)
            cv2.imshow('fixed', warped)


            #####################################################################################
            # TEMP ZONE
            #####################################################################################
            hsv = cv2.cvtColor(warped,cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv,(h1,s1,v1),(h2,s2,v2))
            res = cv2.bitwise_and(warped,warped, mask= mask)
            cv2.imshow('ress', res)
            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (15,15), b)
            cv2.imshow('resss', gray)
            ratio = 3
            edged = cv2.Canny(gray, lowthreshold, lowthreshold*ratio)
            cv2.imshow('edged 1', edged)
            edged = cv2.dilate(edged, None, iterations=diter)
            edged = cv2.erode(edged, None, iterations=eiter)
            cv2.imshow('edged 2', edged)
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
            cv2.imshow('filtered red2', res)
            
            #####################################################################################
        i += 1
        cv2.imshow('real', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()