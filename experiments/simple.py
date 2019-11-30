from scipy.spatial import distance as dist
import numpy as np
import cv2
import imutils
from imutils import perspective
from imutils import contours
from cv2 import aruco
import math  


def simple():
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

simple()