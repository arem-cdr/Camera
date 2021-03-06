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

        # General
        self.debug = raw['enable_debug']
        self.fps = raw['enable_fps']

        # Calib error check values
        self.calib_check_time_in_sec = int(raw['calib_check_time_in_sec'])
        self.loc_aruco_x = float(raw['loc_aruco_x'])
        self.loc_aruco_y = float(raw['loc_aruco_y'])
        self.loc_aruco_acceptable_diff = float(raw['loc_aruco_acceptable_diff'])

        # Zones to retake and exclude
        self.zones_to_retake = raw['zones_to_retake']
        self.zones_to_exclude = raw['zones_to_exclude']

        # Calib data
        self.matrix = raw['enable_perpective_correction']
        self.sizeXmm = raw['sizeXmm']
        self.sizeYmm = raw['sizeYmm']
        self.zeroxloc = raw['zeroxloc']
        self.zeroyloc = raw['zeroyloc']
        self.reduction = int(raw['reduction'])
        self.calibfile = raw['matrix_file']
        if(self.matrix):
            self.M = np.load(raw['matrix_file'])

        # Fish
        self.fish = raw['enable_fisheye']
        if(self.fish):
            self.K = np.load(raw['matrix_K'])
            self.D = np.load(raw['matrix_D'])
            self.DIM = np.load(raw['array_DIM'])
        
        # Object extraction
        self.back = raw['enable_background_diff_from_file']
        self.threshold = raw['threshold']
        self.background = raw['sub_file']
        self.size_min = raw['noise_size']
        self.size_min_robot = raw['min_robot_size']
        self.obj_center_ratio = float(raw['obj_center_ratio'])
        self.robot_center_ratio = float(raw['robot_center_ratio'])

        # Points
        self.points = raw['points']

        # Workflow
        self.img_resize_default = float(raw['img_resize_default'])
        self.img_resize_after_fish = float(raw['img_resize_after_fish'])
        self.img_resize_after_perpective = float(raw['img_resize_after_perpective'])
        self.img_resize_display = float(raw['img_resize_display'])

class BaseConfig(object):
    def  __init__(self):
        pass
    def load(self,path):
        raw = ""
        with open(path, 'r') as ymlfile:
            raw = yaml.load(ymlfile,Loader=yaml.FullLoader)
        self.confYellow = raw['conf_Yellow']
        self.confBlue = raw['conf_Blue']