from scipy.spatial import distance as dist
import numpy as np
import cv2
import imutils
from imutils import perspective
from imutils import contours
from cv2 import aruco
import math  
from calibrator import *

# Here we build the code that calls other scripts to do all the work

def main():
    cap = cv2.VideoCapture("v14.mov")
    sizex = 1/2
    sizey = 1/2
    calculated = False
    sizeXmm = 49
    sizeYmm = 58
    calibobj = Calib(13,11,15,14,sizeXmm*10,sizeYmm*10)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey) 
        if(not(calculated) or (i<40)):
            result = calibobj.genCalibration(resized)
            calculated = result
        if calculated:
            warped = calibobj.applyCalibration(resized)
            cv2.imshow('corrected', warped)
        i += 1
        cv2.imshow('real', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()