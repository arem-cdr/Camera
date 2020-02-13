import cv2
import numpy as np
import imutils
from imutils import contours

def imgbox(img):
   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7,7), 0)
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours individually
    for c in cnts:
        
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box) 
        box = np.array(box, dtype="int")
        cv2.drawContours(img, [box.astype("int")],-1, (0, 0, 255), 2) 
        k = doubleminBox(box)
        fmin= k[0]
        smin = k[1]
        cv2.circle(img,(int(fmin[0]),int(fmin[1])),3,(255,255,0),1)
        cv2.circle(img,(int(smin[0]),int(smin[1])),3,(255,255,0),1)
  
        teta = np.arctan2(smin[1]-fmin[1],smin[0]-fmin[0])
        print(teta)
        xmid = (fmin[0]+smin[0])/2 
        ymid = (fmin[1]+smin[1])/2
        proportion = 0.1
        k = getHW(box)
        h = k[0]
        w = k[1]
        
        xdelta = -np.sin(teta)*proportion*h
        ydelta = np.cos(teta)*proportion*h
        if(teta<np.pi/2):
            xdelta = -xdelta
            ydelta = -ydelta
     
        centerx =  xmid+xdelta
        centery = ymid + ydelta
        cv2.circle(img,(int(centerx),int(centery)),3,(255,0,0),2)
    return img

def dist(p1,p2):
    return np.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)

def getHW(box):
    l = []
    plast = box[0]
    for p in box:
        l.append(dist(plast,p))
        plast = p
    l.pop()
    u= [np.max(l),np.min(l)]
    return u

        

def doubleminBox(box):

    b1 = box[0]
    b1y = box[0][1]
    b2 = box[1]
    b2y = box[1][1]
   
    for i in range(2,4):
        p = box[i]
     
        if(p[1]>b1y & p[1]>b2y):
            if(p[1]>b1y):
                b1y = p[1]
                b1 = p
            else:
                b2y = p[1]
                b2 = p

        if(p[1]>b2y):
            b2y = p[1]
            b2 = p
        if(p[1]>b1y):
            b1y = p[1]
            b1 = p
        i+=1
    if(b1y>b2y):
        b1,b2 = b2,b1
    # second min, first min
    
    k = [b1,b2]
    return k

img = cv2.imread('raw/calib_fish/11.jpg')
img = imgbox(img)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()