
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
from modules.track import *
from modules.gpiomanager import *
from modules.checkInterest import *
from modules.backgroundup import *

# Here we build the code that calls other scripts to do all the work
def main():
    

    # Initializing GPIO
    gpioM = GpioManager()

    # Base config load
    bc = BaseConfig()
    bc.load("config.yml")
    if(gpioM.led):
        conf_file = bc.confBlue
    else:
        conf_file = bc.confYellow
    print("Loaded: " + conf_file)

    # Loading data from specific config.yml
    conf = Config()
    conf.load(conf_file)

    # Initializing Communication Object
    com = Com()

    # Generating data object (to stock collected data)
    data = DataExtractor(1)
    

    # Loading perspective correction matrix from file if exits
    if(conf.matrix == 1):
        calibobj = Calib(conf.sizeXmm//conf.reduction, conf.sizeYmm//conf.reduction, conf.matrix, conf.calibfile)
        calibobj.M = conf.M

    # Tracker object to calibrate with central aruco
    track = Tracker()
    
    # Interest track
    # interests = CInterest(conf.points)

    # Auto regen background
    # backupdate = BackgroundUp(conf)

    # Some counters
    i = 0
    changedConf = 0
    j = 1
    fps_t = time.time()
    start_t = time.time()
    # Opening data stream
    cap = cv2.VideoCapture(0)

    while(cap.isOpened()):
        ret, img = cap.read()
        if(img is None):
            break
        img = cv2.resize(img, (0, 0), fx=conf.img_resize_default, fy=conf.img_resize_default)
        # cv2.imshow('real', resized)

        # Removing fisheye
        if(conf.fish == 1):
            if(i == 0):
                # Generating FishEye remover object
                fishremover = FRemover(img, 1, conf.K, conf.D, conf.DIM)
            img = fishremover.removefish(img)
            img = cv2.resize(img, (0, 0), fx=conf.img_resize_after_fish, fy=conf.img_resize_after_fish)
        
        # Check camera position 
        if(time.time() - start_t < conf.calib_check_time_in_sec):
            aruco_pos = track.getPos(img, 42)
        else:
            aruco_pos = [1]
            
        # Applying perspective correction matrix to frame
        if(conf.matrix):
            img = calibobj.applyCalibration(img)
            img = cv2.resize(img, (0, 0), fx=conf.img_resize_after_perpective, fy=conf.img_resize_after_perpective)
        
        # Interest 
        # img = interests.display(img)
        # cv2.imshow('interest', img)
        # l = interests.extract(img)
        # com.send_Interest_list(l)
        # print(l)

        # Loading or Saving background
        if(i == 0):
            gex = NGExtractors(conf, img) 

        # Clearing buffer
        data.clear()
        # Get Data
        img_result = gex.extract(img, data, conf)
        com.send_Point_list(data.green_gobelet, 1, conf)
        com.send_Point_list(data.red_gobelet, 2, conf)
        com.send_Point_list(data.robot, 3, conf)
        
        # Background update
        # backupdate.update(img, start_t, gex)

        # Debug
        if(conf.debug):
            data.showTrails(img, 3)
            data.showPos(img, conf)
            img_result = cv2.resize(img, (0, 0), fx=conf.img_resize_display,fy=conf.img_resize_display)
            cv2.imshow('mask + track', img_result)

        # FPS
        if(conf.fps):
            if(time.time() - fps_t > 1): 
                fps_t = time.time()
                print("[INFO] {} FPS".format(j))
                j = 1
        
        
        # Led & Switch
        changedConf = gpioM.update(aruco_pos,conf)
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
