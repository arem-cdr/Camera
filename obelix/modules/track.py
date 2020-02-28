
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
        imgg = aruco.drawDetectedMarkers(img, corners, ids)
        return imgg
    
    def get(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        
    def getPos(self, img, tagid):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        l = []
        for i in range():
            if(ids[i]==tagid):
                rect = corners[i][0]
                cX = np.average(rect[:, 0])
                cY = np.average(rect[:, 1]) 
                l = [cX,cY] 
        return l

def maxX(l):
    return max([l[i][0] for i in range(len(l))])
def maxY(l):
    return max([l[i][1] for i in range(len(l))])
def minX(l):
    return min([l[j][0] for j in range(len(l))])
def minY(l):
    return min([l[i][1] for i in range(len(l))])