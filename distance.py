from scipy.spatial import distance as dist
import numpy as np
import cv2
import imutils
from imutils import perspective
from imutils import contours
from cv2 import aruco
import math  


def dis(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

def main():
    # source (direct ou video enregistre).
    cap = cv2.VideoCapture("v7.mov")
    sizex = 1/2
    sizey = 1/2

    while(cap.isOpened()):
        ret, frame = cap.read()
        try:
            resized = cv2.resize(frame, (0, 0), fx=sizex,fy=sizey) 
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
            parameters =  aruco.DetectorParameters_create()
            # boom, fonction qui retrouve les coins des qrcode aruco.
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

            # ici on affiche les rectangles + le calcul de distance
            ox,oy =0,0
            rx,ry = 0,0
            for i in range(len(corners)):
                obj = corners[i][0]
                cx,cy = obj[:, 0].mean(),obj[:, 1].mean() # on retrouve le centre de chaque carre
                if ids[i] ==14:
                    cv2.circle(resized, (cx,cy), 10, (0, 255, 0))
                    rx,ry =cx,cy
                else:
                    cv2.circle(resized, (cx,cy), 10, (0, 0, 0))  
                    ox,oy =cx,cy   
            if(len(corners)==2):    
                # affichage de la distance séparant les deux aruco
                d = round(dis(rx,ry,ox,oy),2)
                cv2.line(resized, (rx,ry), (ox,oy), (240, 0, 159))
                cv2.putText(resized, "{}".format(d), (int((rx+ox)/2.0), int((ry+oy)/2.0)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 0, 159), 2)

            resized = aruco.drawDetectedMarkers(resized, corners, ids)
            cv2.imshow('mask_blur', resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            pass
    cap.release()
    cv2.destroyAllWindows()

main()