
import numpy as np
import cv2
import time
import math  
import cProfile

# Imports from our project
from modules.calibrator import *
from modules.gextractorNG import *
from modules.dextractor import *
from modules.fisheye import *
from modules.settings import *
from modules.network import *


# Here we build the code that calls other scripts to do all the work
def main():
    # Opening data stream
    cap = cv2.VideoCapture(0)

    # Loading data from config.yml
    conf = Config()
    conf.load("config.yml")

    com = Com()

    # Generating FishEye remover object
    if(conf.fish == 1):
        fishremover = FRemover(1, conf.K, conf.D, conf.DIM)
       
    # Loading perspective correction matrix from file if exits
    if(conf.matrix == 1):
        calibobj = Calib(conf.sizeXmm,conf.sizeYmm,conf.matrix,conf.calibfile)
        calibobj.M = conf.M

    # Generating data object (to stock collected data)
    data = DataExtractor(1)
   
    i = 0
    while(cap.isOpened()):
        ret, img = cap.read()
        if(img is None):
            break
        img = cv2.resize(img, (0, 0), fx=conf.img_resize_default,fy=conf.img_resize_default)
        #cv2.imshow('real', resized)

        # Removing fisheye
        if(conf.fish == 1):
            img = fishremover.removefish(img)
            img = cv2.resize(img, (0, 0), fx=conf.img_resize_after_fish,fy=conf.img_resize_after_fish)
        
        # Applying perspective correction matrix to frame
        if(conf.matrix):
            img = calibobj.applyCalibration(img)
            img = cv2.resize(img, (0, 0), fx=conf.img_resize_after_perpective,fy=conf.img_resize_after_perpective)
          
        # Saving background
        if(i == 0):
            gex = NGExtractors(conf,img) 

        # Clearing buffer
        data.clear()
        # Get Data
        img_result = gex.extract(img,data,conf)
        com.send_Point_list(data.red_gobelet)
        
        # Debug
        if(conf.debug):
            data.showTrails(img,3)
            data.showPos(img,conf)
            img_result = cv2.resize(img, (0, 0), fx=conf.img_resize_display,fy=conf.img_resize_display)
            cv2.imshow('mask + track', img_result)
       
        i += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()
