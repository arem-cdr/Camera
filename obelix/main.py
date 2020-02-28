
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
from modules.gpiomanager import *

# Here we build the code that calls other scripts to do all the work
def main():
    # Opening data stream
    cap = cv2.VideoCapture(0)

    # Initializing GPIO
    gpioM = GpioManager()

    # Base config load
    bc = BaseConfig()
    bc.load("config.yml")
    if(not gpioM.led):
        conf_file = bc.confBlue
    else:
        conf_file = bc.confYellow
    print("Loaded: "+conf_file)

    # Loading data from specific config.yml
    conf = Config()
    conf.load(conf_file)

    # Initializing Communication Object
    com = Com()
       
    # Loading perspective correction matrix from file if exits
    if(conf.matrix == 1):
        calibobj = Calib(conf.sizeXmm//conf.reduction, conf.sizeYmm//conf.reduction, conf.matrix, conf.calibfile)
        calibobj.M = conf.M

    # Generating data object (to stock collected data)
    data = DataExtractor(1)
    
    i = 0
    changedConf = 0
    j = 1
    t = time.time()

    while(cap.isOpened()):
        ret, img = cap.read()
        if(img is None):
            break
        img = cv2.resize(img, (0, 0), fx=conf.img_resize_default, fy=conf.img_resize_default)
        #cv2.imshow('real', resized)

        # Removing fisheye
        if(conf.fish == 1):
            if(i == 0):
                # Generating FishEye remover object
                fishremover = FRemover(img,1, conf.K, conf.D, conf.DIM)
            img = fishremover.removefish(img)
            img = cv2.resize(img, (0, 0), fx=conf.img_resize_after_fish, fy=conf.img_resize_after_fish)
        
        # Applying perspective correction matrix to frame
        if(conf.matrix):
            img = calibobj.applyCalibration(img)
            img = cv2.resize(img, (0, 0), fx=conf.img_resize_after_perpective, fy=conf.img_resize_after_perpective)
          
        # Saving background
        if(i == 0):
            gex = NGExtractors(conf, img) 

        # Clearing buffer
        data.clear()
        # Get Data
        img_result = gex.extract(img, data, conf)
        com.send_Point_list(data.green_gobelet, 1, conf)
        com.send_Point_list(data.red_gobelet, 2, conf)
        com.send_Point_list(data.robot, 3, conf)
        
        # Debug
        if(conf.debug):
            data.showTrails(img, 3)
            data.showPos(img, conf)
            img_result = cv2.resize(img, (0, 0), fx=conf.img_resize_display,fy=conf.img_resize_display)
            cv2.imshow('mask + track', img_result)

        # FPS
        if(conf.fps):
            if(time.time() - t > 1): 
                t = time.time()
                print("[INFO] {} FPS".format(j))
                j = 1
        
        # Led & Switch
        changedConf = gpioM.update()
        if(changedConf):
            break
        
        i += 1
        j += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

    # Switching procedure
    if(changedConf):
        main()


main()
