import cv2
import numpy as np
import os



class FRemover(object):
    def  __init__(self,img, balance, K, D, DIM, dim2=None, dim3=None):
        self.balance = balance
        self.K = K
        self.D = D
        self.DIM = DIM
        self.dim2 = dim2
        self.dim3 = dim3
        # By Kenneth Jiang
        dim1 = img.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort
        assert dim1[0]/dim1[1] == self.DIM[0]/self.DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
        if not self.dim2:
            self.dim2 = dim1
        if not self.dim3:
            self.dim3 = dim1
        scaled_K = self.K * dim1[0] / self.DIM[0]  # The values of K is to scale with image dimension.
        scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
        # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
        new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, self.D, self.dim2, np.eye(3), balance=self.balance)
        self.map1, self.map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, self.D, np.eye(3), new_K, self.dim3, cv2.CV_16SC2)
    def removefish(self,img):
        
        undistorted_img = cv2.remap(img, self.map1, self.map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted_img