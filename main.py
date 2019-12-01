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

def main():
    # Opening data stream
    cap = cv2.VideoCapture("raw/v14.mov")
    sizex = 1/2
    sizey = 1/2

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

        # Reading frame from stream
        ret, frame = cap.read()

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
            hsv = cv2.cvtColor(warped,cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv,(0,80,40),(255,255,255))
            res = cv2.bitwise_and(warped,warped, mask= mask)
            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7,7), 0)
            edged = cv2.Canny(gray, 50, 100)
            edged = cv2.dilate(edged, None, iterations=1)
            edged = cv2.erode(edged, None, iterations=2)
            # find contours in the edge map
            cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE  )
            cnts = imutils.grab_contours(cnts)
            # loop over the contours individually
            cv2.drawContours(res, cnts, -1, (0,255,0), 3)
            cv2.imshow('filtered red2', res)
            # Goblet vert
            green = warped.copy()
            green[green[:,:,1] <=80] = 0
            green[(green[:,:,1] >=200)]  = 0
            cv2.imshow('filtered green', green)

            # Goblet rouge
            red = warped
            red[red[:,:,2] <=70] = 0
            red[(red[:,:,2] >=220)]  = 0
            cv2.imshow('filtered red', red)

        i += 1
        cv2.imshow('real', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()