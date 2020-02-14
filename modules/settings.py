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
        self.sizeXmm = raw['sizeXmm']
        self.sizeYmm = raw['sizeYmm']
        self.matrix = raw['matrix']
        self.calibfile = raw['matrix_file']
        self.fish = raw['fisheye']
        if(self.fish):
            self.K = np.load(raw['matrix_K'])
            self.D = np.load(raw['matrix_D'])
            self.DIM = np.load(raw['array_DIM'])
        if(self.matrix):
            self.M = np.load(raw['matrix_file'])
        self.back = raw['background_file']
        self.background = raw['sub_file']
        self.size_min = raw['size_min']
        self.size_min_robot = raw['size_min_robot']
