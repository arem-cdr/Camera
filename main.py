from scipy.spatial import distance as dist
import numpy as np
import cv2

from cv2 import aruco
import math  
import yaml 
from calibrator import *
from track import *
from gextractor import *

# Here we build the code that calls other scripts to do all the work

def main():
    # Opening data stream
    cap = cv2.VideoCapture("raw/v12.MOV")
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
    track = Tracker() 
    gex = GExtractors() 
    gex.debug_init("test","test1")
    i = 0
    while(cap.isOpened()):
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
            gex.debug(warped,"test","test1")
            aruco = track.draw(warped)
            cv2.imshow('aruco', aruco)
            #####################################################################################
        i += 1
        cv2.imshow('real', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()