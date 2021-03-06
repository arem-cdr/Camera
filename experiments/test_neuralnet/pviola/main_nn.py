
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
from modules.classifier import *

# Here we build the code that calls other scripts to do all the work
def main(conf_file):
    # Opening data stream
    cap = cv2.VideoCapture(0)
    
    # Loading data from config.yml
    conf = Config()
    conf.load(conf_file)


    # Generating FishEye remover object
    if(conf.fish == 1):
        fishremover = FRemover(1, conf.K, conf.D, conf.DIM)
       
    # Loading perspective correction matrix from file if exits
    if(conf.matrix == 1):
        calibobj = Calib(conf.sizeXmm//conf.reduction,conf.sizeYmm//conf.reduction,conf.matrix,conf.calibfile)
        calibobj.M = conf.M

    # Generating data object (to stock collected data)
    
    # Initializing GPIO
    gpioM = GpioManager()

    # Classifier
    cl = Classifier("classifier/trained/cascade.xml")

    i = 0
    changedConf = 0
    j = 1
    t = time.time()
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
          
        cl.detectAndDisplay(img)
       
        # FPS
        if(conf.fps):
            if(time.time()-t>1): 
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
        bc = BaseConfig()
        bc.load("config.yml")
        if(bc.confYellow == conf_file):
            main(bc.confBlue)
        else:
            main(bc.confYellow)


bc = BaseConfig()
bc.load("config.yml")
main(bc.confYellow)
