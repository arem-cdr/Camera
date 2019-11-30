from scipy.spatial import distance as dist
import numpy as np
import cv2
import imutils
from imutils import perspective
from imutils import contours
from cv2 import aruco
import math  

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
def order_points(corners,ids):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = [[0,0],[0,0],[0,0],[0,0]]
    for i in range(4):
        if(ids[i]==13):
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

        if(ids[i]==11):
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
        if(ids[i]==15):
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
        if(ids[i]==14):
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
    # return the ordered coordinates
   

def four_point_transform(rect):
    # obtain a consistent order of the points and unpack them
    # individually
    rect1 = np.zeros((4, 2), dtype = "float32")
    rect1[0] = rect[0]
    rect1[1] = rect[1]
    rect1[2] = rect[2]
    rect1[3] = rect[3]
    (tl, tr, br, bl) = rect1
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    maxHeight = 580
    maxWidth = 490
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect1, dst)
    return M,maxHeight,maxWidth
def getcxcy(wcorners,wids):
    (cx,cy) = 0,0
    try:
        for j in range(4):
            if(wids[j]==12):
                obj = wcorners[j][0]
                cx,cy = obj[:, 0].mean(),obj[:, 1].mean()
    except:
        pass
    return (cx,cy)

def main():
    calculated = False
    M = None
    # Select video source/file.
    cap = cv2.VideoCapture("v13.mov")
    sizex = 1/2
    sizey = 1/2
    #backSub = cv2.createBackgroundSubtractorMOG2()
    rect = None
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        i += 1
         #fgMask = backSub.apply(frame)
        resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey) 
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
   
        if((not(calculated) or (i<40)) and len(corners)==5):
            rect = order_points(corners,ids)
            M,maxWidth, maxHeight = four_point_transform(rect)
            warped = cv2.warpPerspective(resized, M, (maxHeight,maxWidth))
            calculated = True
        if calculated and rect != None:
            warped = cv2.warpPerspective(resized, M, (maxHeight,maxWidth))
            for j in range(4):
                x,y = rect[j]
                cv2.circle(resized, (x,y), 20, (0, 255, 0))
             
        resized = aruco.drawDetectedMarkers(resized, corners, ids)
        
        cv2.imshow('mask_blur', resized)
        try:
            wcorners, wids, wrejectedImgPoints = aruco.detectMarkers(warped, aruco_dict, parameters=parameters)
            warped = aruco.drawDetectedMarkers(warped, wcorners, wids)
            (cx,cy) = getcxcy(wcorners,wids)
            cv2.circle(warped, (cx,cy), 10, (0, 0, 255))
            v = round(distance([0,0], [cx,cy]),2)
            cv2.putText(warped, "{}".format((cx,cy)), (int(cx), int(cy-40)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 0, 159), 2)
            cv2.imshow('warped', warped)
        except:
            pass
        #cv2.imshow('mask_blur', fgMask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


main()