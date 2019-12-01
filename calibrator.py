
import cv2
from cv2 import aruco
import numpy as np





class Calib(object):
    def  __init__(self,toplid,toprid,lowrid,lowlid,sizeXmm,sizeYmm):
        self.rect = [[0,0],[0,0],[0,0],[0,0]]
        self.toplid = toplid
        self.toprid = toprid
        self.lowrid = lowrid
        self.lowlid = lowlid
        self.maxWidth = sizeXmm
        self.maxHeight = sizeYmm

    def genCalibration(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if(len(corners)==4):
            self.rect = getRect(corners,ids,self.toplid,self.toprid,self.lowrid,self.lowlid)
            self.M,self.maxHeight,self.maxWidth = four_point_transform(self.rect,self.maxHeight,self.maxWidth)
            return True
        else:
            return False
    def applyCalibration(self,img):
        corrected = cv2.warpPerspective(img, self.M, (self.maxWidth,self.maxHeight))
        return corrected
    def saveMat(self):
        np.save('calib_matrix.npy',self.M)


def four_point_transform(rect,maxHeight,maxWidth):
    # obtain a consistent order of the points and unpack them
    # individually
    rect1 = np.zeros((4, 2), dtype = "float32")
    rect1[0] = rect[0]
    rect1[1] = rect[1]
    rect1[2] = rect[2]
    rect1[3] = rect[3]
    (tl, tr, br, bl) = rect1

 
    dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(rect1, dst)
    return M,maxHeight,maxWidth

def maxX(l):
    return max([l[i][0] for i in range(len(l))])
def maxY(l):
    return max([l[i][1] for i in range(len(l))])
def minX(l):
    return min([l[j][0] for j in range(len(l))])
def minY(l):
    return min([l[i][1] for i in range(len(l))])
def distance(v1,v2):
    return ((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)**(0.5)

def getRect(corners,ids,topl,topr,lowr,lowl):
    rect = [[0,0],[0,0],[0,0],[0,0]]
    for i in range(4):
        if(ids[i]==topl):
            rect[0]= [0,0]
            rect14 = corners[i][0]
            point = [minX(rect14),minY(rect14)]
            mindis = distance(point,rect14[0])
            minpoint = rect14[0]
            for el in rect14:
                if(distance(point,el)<mindis):
                    minpoint = el
                    mindis =  distance(point,el)
            rect[0] = minpoint
        if(ids[i]==topr):
            rect[1]= [0,0]
            rect14 = corners[i][0]
            point = [maxX(rect14),minY(rect14)]
            mindis = distance(point,rect14[0])
            minpoint = rect14[0]
            for el in rect14:
                if(distance(point,el)<mindis):
                    minpoint = el
                    mindis =  distance(point,el)
            rect[1] = minpoint
        if(ids[i]==lowr):
            rect[2]= [0,0]
            rect14 = corners[i][0]
            point = [maxX(rect14),maxY(rect14)]
            mindis = distance(point,rect14[0])
            minpoint = rect14[0]
            for el in rect14:
                if(distance(point,el)<mindis):
                    minpoint = el
                    mindis =  distance(point,el)
            rect[2] = minpoint
        if(ids[i]==lowl):
            rect[3]= [0,0]
            rect14 = corners[i][0]
            point = [minX(rect14),maxY(rect14)]
            mindis = distance(point,rect14[0])
            minpoint = rect14[0]
            for el in rect14:
                if(distance(point,el)<mindis):
                    minpoint = el
                    mindis =  distance(point,el)
            rect[3] = minpoint
    return rect