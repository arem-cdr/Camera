
import numpy as np
import cv2
import time
from cv2 import aruco
import math  


# Imports from our project
from modules.calibrator import *
from modules.track import *
from modules.gextractor import *
from modules.gextractorNG import *
from modules.dextractor import *
from modules.fisheye import *
from modules.settings import *


# Here we build the code that calls other scripts to do all the work
def main():
    # Opening data stream
    cap = cv2.VideoCapture(0)
    sizex = 1
    sizey = 1
    # Loading data from config.yml
    conf = Config()
    conf.load("config.yml")

    if(conf.fish == 1):
        # Generating FishEye remover object
        fishremover = FRemover(1, conf.K, conf.D, conf.DIM)
       
    # Loading perspective correction matrix from file if exits
    if(conf.matrix == 1):
        calibobj = Calib(conf.tl,conf.tr,conf.dr,conf.dl,conf.sizeXmm,conf.sizeYmm,conf.matrix,conf.calibfile)
        calibobj.M = conf.M
    # Generating data object (to stock collected data)
    data = DataExtractor()
   
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
        #cv2.imshow('bird eye', warped)
        if(i == 0):
            gex = NGExtractors(warped) 
        res =gex.draw(warped,data)
     
        for j in range(len(data.fallen_goblet)):
            
            if( (time.time() - data.fallen_goblet[j].t)>3):
                data.fallen_goblet.pop(j)
            else:
                center = (int(data.fallen_goblet[j].x), int(data.fallen_goblet[j].y))
                cv2.circle(res, center, 2, (0, 0, 255),2)
        cv2.imshow('mask + track', res)
       
        i += 1
        #cv2.imshow('real + fish', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()
