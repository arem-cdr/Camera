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
            raw = yaml.load(ymlfile)
        self.sizeXmm = raw['sizeXmm']
        self.sizeYmm = raw['sizeYmm']
        self.matrix = raw['matrix']
        self.tl = raw['idtl']
        self.tr = raw['idtr']
        self.dr = raw['iddr']
        self.dl = raw['iddl']
        self.fish = raw['fisheye']
        self.K = np.load(raw['matrix_K'])
        self.D = np.load(raw['matrix_D'])
        self.DIM = np.load(raw['array_DIM'])
        self.M = np.load(raw['matrix_file'])
