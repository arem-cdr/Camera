from scipy.spatial import distance as dist
import numpy as np
import cv2
import imutils
from imutils import perspective
from imutils import contours
from cv2 import aruco
import math  

def first():
    # Select video source/file.
    cap = cv2.VideoCapture("v3.mov")
    sizex = 1/2
    sizey = 1/2
    #backSub = cv2.createBackgroundSubtractorMOG2()

    while(cap.isOpened()):
        ret, frame = cap.read()
        try:
            #fgMask = backSub.apply(frame)
            resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey) 
            
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7,7), 0)
            edged = cv2.Canny(gray, 50, 100)
            edged = cv2.dilate(edged, None, iterations=1)
            edged = cv2.erode(edged, None, iterations=1)
            # find contours in the edge map
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            # loop over the contours individually
            i = 0
            for c in cnts:
                if(i>50):
                    continue
                if(cv2.contourArea(c) < 150):
                    continue
                
                i+=1
            
            
                # compute the rotated bounding box of the contour
                box = cv2.minAreaRect(c)
                box = cv2.boxPoints(box) 
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)
            
                # compute the center of the bounding box
                (tl, tr, br, bl) = box
                tx,ty = tl
                cX = np.average(box[:, 0])
                cY = np.average(box[:, 1])
                cv2.putText(resized, "{},{}".format(int(cX), int(cY)), (int(tx)-10, int(ty)-10),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 0, 159), 2)
                cv2.drawContours(resized, [box.astype("int")], -1, (0, 255, 0), 2)
            cv2.imshow('mask_blur', resized)
            #cv2.imshow('mask_blur', fgMask)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            pass
    cap.release()
    cv2.destroyAllWindows()

def dis(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

def laruco():
    # Select video source/file.
    cap = cv2.VideoCapture("v7.mov")
    sizex = 1/2
    sizey = 1/2
    #backSub = cv2.createBackgroundSubtractorMOG2()

    while(cap.isOpened()):
        ret, frame = cap.read()
        
        try:
            #fgMask = backSub.apply(frame)
            resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey) 
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
            parameters =  aruco.DetectorParameters_create()
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
            ox,oy =0,0
            rx,ry = 0,0
            for i in range(len(corners)):
                obj = corners[i][0]
                cx,cy = obj[:, 0].mean(),obj[:, 1].mean()
                if ids[i] ==14:
                    cv2.circle(resized, (cx,cy), 10, (0, 255, 0))
                    rx,ry =cx,cy
                else:
                    cv2.circle(resized, (cx,cy), 10, (0, 0, 0))  
                    ox,oy =cx,cy   
            if(len(corners)==2):    
                d = round(dis(rx,ry,ox,oy),2)
                cv2.line(resized, (rx,ry), (ox,oy), (240, 0, 159))
                cv2.putText(resized, "{}".format(d), (int((rx+ox)/2.0), int((ry+oy)/2.0)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 0, 159), 2)
            
            
            resized = aruco.drawDetectedMarkers(resized, corners, ids)
            cv2.imshow('mask_blur', resized)
            #cv2.imshow('mask_blur', fgMask)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            pass
    cap.release()
    cv2.destroyAllWindows()

def order_points(corners,ids):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = []
    for i in range(3):
        if(ids[i]==14):
            rect[0]= corners[i][0][0]

        if(ids[i]==12):
            rect[1]= corners[i][0][1]

        if(ids[i]==13):
            rect[2]= corners[i][0][2]

        if(ids[i]==15):
            rect[3]= corners[i][0][3]
    return rect
    # return the ordered coordinates
   

def four_point_transform(cornes,ids):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(cornes,ids)
    (tl, tr, br, bl) = rect
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

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    return M,maxHeight,maxWidth

def loc():
    calculated = False
    M= None
    # Select video source/file.
    cap = cv2.VideoCapture("v9.mov")
    sizex = 1/2
    sizey = 1/2
    #backSub = cv2.createBackgroundSubtractorMOG2()
    while(cap.isOpened()):
        ret, frame = cap.read()
        
        
         
        #fgMask = backSub.apply(frame)
        resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey) 
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if(not(calculated) and len(corners)==4):
            return corners
            rect = order_points(corners,ids)
            for j in range(3):
                x,y = rect[j]
                cv2.circle(resized, (x,y), 10, (0, 255, 0))
            M,maxWidth, maxHeight = four_point_transform(corners,ids)
            frame = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))
            calculated = True
        resized = aruco.drawDetectedMarkers(resized, corners, ids)
        cv2.imshow('mask_blur', resized)

        #cv2.imshow('mask_blur', fgMask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()

laruco()