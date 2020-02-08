import cv2
import numpy as np
from modules.calibrator import *
from modules.fisheye import *
from modules.settings import *

refPt = []
conf = Config()
conf.load("config.yml")

def click_and_crop(event, x, y, flags, param):
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        cv2.rectangle(image, (x-10,y-10),(x+10,y+10), (0, 0, 255), 2)

# Opening data stream
cap = cv2.VideoCapture(0)
ret, image = cap.read()
fishremover = FRemover(1, conf.K, conf.D, conf.DIM)
image = fishremover.removefish(image)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("r"):
        image = clone.copy()
        refPt = []
    elif key == ord("c"):
        break

if len(refPt) == 4 :
    M,maxHeight,maxWidth = four_point_transform(refPt,conf.sizeYmm ,conf.sizeXmm )
    np.save("calib_data/calib_matrix.npy",M)
    print("Saved to calib_data/calib_matrix.npy")

cv2.destroyAllWindows()
