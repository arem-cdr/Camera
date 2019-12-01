
import cv2
from cv2 import aruco
import numpy as np





class Tracker(object):
    def  __init__(self):
       pass

    def draw(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        img = aruco.drawDetectedMarkers(img, corners, ids)
        return img
    
    def get(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        


