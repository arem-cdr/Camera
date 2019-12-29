
import numpy as np
import cv2
import time
from cv2 import aruco
import math  
import yaml 

# Imports from our project
from calibrator import *
from track import *
from gextractor import *
from gextractorNG import *
from dextractor import *
from fisheye import *

# Here we build the code that calls other scripts to do all the work

def main():
    # Opening data stream
    cap = cv2.VideoCapture("raw/video9.h254")
    sizex =1
    sizey =1
    # Loading data from config.yml
    raw = ""
    with open("config.yml", 'r') as ymlfile:
        raw = yaml.load(ymlfile)
    calculated = False
    sizeXmm = raw['sizeXmm']
    sizeYmm = raw['sizeYmm']
    matrix = raw['matrix']
    tl = raw['idtl']
    tr = raw['idtr']
    dr = raw['iddr']
    dl = raw['iddl']
    
    
    # Loading correction matrix from files
    if(fish == 1):
        # Generating FishEye remover object
        Dp= raw['matrix_D']
        Kp = raw['matrix_K']
        Ap = raw['array_DIM']
        K = np.load(raw[Kp])
        D = np.load(raw[Dp])
        DIM = np.load(raw[Ap])
        fishremover = FRemover(0, K, D, DIM, dim2=None, dim3=None)
       
    # Generating Calibration object
    calibobj = Calib(tl,tr,dr,dl,sizeXmm,sizeYmm)
    # Loading perspective correction matrix from file if exits
    if(matrix ==1):
        calibobj.M = np.load(raw['matrix_file'])
        i = 40
        calculated = True
    # Generating data object (to stock collected data)
    data = DataExtractor()
    # Generating tracker object (for aruco detection)
    track = Tracker() 
    # Generating Gextractor object (for 'gobelet' detection)
    #gex.debug_init("test","test1")
    i = 0
    while(cap.isOpened()):

        #####################################################################
        # Reading frame from video stream
        ret, frame = cap.read()
        if(frame is None):
            break

        # Resizing image
        resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey)

         # Removing fisheye
        if(fish == 1):
            resized = fishremover.removefish(resized)
        #####################################################################
        # TEMP ZONE
        #___________________________________________________________________#

        #aruco = track.draw(resized)
        #gex.debug(resized,"test","test1")
        # Initializing gextractor
        if(i==0):
            gex = NGExtractors(resized) 
        gex.draw(resized)
        #####################################################################
        # Checking if we have calculate perspective correction matrix

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
            #####################################################################
            # TEMP ZONE
            #___________________________________________________________________#
            #gex.debug(warped,"test","test1")
            
            #cv2.imshow('aruco', aruco)
            #####################################################################
        i += 1
      
        cv2.imshow('real', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()