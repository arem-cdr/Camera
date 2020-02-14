
import numpy as np
import cv2
import time
from cv2 import aruco
import math  
import cProfile

# Imports from our project
from modules.calibrator import *
from modules.track import *
from modules.gextractor import *
from modules.gextractorNG import *
from modules.dextractor import *
from modules.fisheye import *
from modules.settings import *
from modules.network import *


# Here we build the code that calls other scripts to do all the work
def main():
    # Opening data stream
    cap = cv2.VideoCapture(0)
    sizex = 1
    sizey = 1
    # Loading data from config.yml
    conf = Config()
    conf.load("config.yml")

    com = Com()

    if(conf.fish == 1):
        # Generating FishEye remover object
        fishremover = FRemover(1, conf.K, conf.D, conf.DIM)
       
    # Loading perspective correction matrix from file if exits
    if(conf.matrix == 1):
        calibobj = Calib(conf.sizeXmm,conf.sizeYmm,conf.matrix,conf.calibfile)
        calibobj.M = conf.M
    # Generating data object (to stock collected data)
    data = DataExtractor(1)
   
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if(frame is None):
            break
        resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey)
        #cv2.imshow('real', resized)

         # Removing fisheye
        if(conf.fish == 1):
            resized = fishremover.removefish(resized)
            # Applying perspective correction matrix to frame
      
        warped = calibobj.applyCalibration(resized)
        warped = cv2.resize(warped, (0, 0), fx=1/4,fy=1/4)
        
        if(i == 0):
            gex = NGExtractors(conf,warped) 

        data.clear()
        # Get Data
        res = gex.extract(warped,data,conf)
        data.showTrails(res,3)
        data.showPos(res,conf)
        com.send_Point_list(data.red_gobelet)
        
        res = cv2.resize(res, (0, 0), fx=1,fy=1)
        cv2.imshow('mask + track', res)
       
        i += 1
        #cv2.imshow('real + fish', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()
