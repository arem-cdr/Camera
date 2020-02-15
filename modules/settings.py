import cv2
import numpy as np
import os
import yaml 

class Config(object):
    def  __init__(self):
        pass
    def load(self,path):
        raw = ""
        with open(path, 'r') as ymlfile:
            raw = yaml.load(ymlfile,Loader=yaml.FullLoader)
        self.debug = raw['enable_debug']
        self.sizeXmm = raw['sizeXmm']
        self.sizeYmm = raw['sizeYmm']
        self.matrix = raw['enable_perpective_correction']
        self.calibfile = raw['matrix_file']
        self.fish = raw['enable_fisheye']
        if(self.fish):
            self.K = np.load(raw['matrix_K'])
            self.D = np.load(raw['matrix_D'])
            self.DIM = np.load(raw['array_DIM'])
        if(self.matrix):
            self.M = np.load(raw['matrix_file'])
        self.back = raw['enable_background_diff_from_file']
        self.background = raw['sub_file']
        self.size_min = raw['noise_size']
        self.size_min_robot = raw['min_robot_size']
        self.img_resize_default = raw['img_resize_default']
        self.img_resize_after_fish = raw['resize_after_fish']
        self.img_resize_after_perpective = raw['img_resize_after_perpective']
        self.img_resize_display = raw['img_resize_display']
