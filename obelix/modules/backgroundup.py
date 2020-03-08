import time
import cv2

class BackgroundUp(object):
    def  __init__(self,conf):
       self.zones_to_exclude = conf.zones_to_exclude
       self.zones_to_retake = conf.zones_to_retake
       self.done_list = []
    def update(self, img, start_time, gextractorng, conf):
        for key in self.zones_to_retake.keys():
            if(key in self.done_list):
                continue
            zone = self.zones_to_retake[key]
            time_to_retake = float(zone['retake_time'])
            if(time.time() - start_time > time_to_retake):
                self.done_list.append(key)
                x1 = int(zone['x1'])
                y1 = int(zone['y1'])
                x2 = int(zone['x2'])
                y2 = int(zone['y2'])
                zone = img[y1:y2,x1:x2]
                if(conf.debug):
                    cv2.imshow('zone_'+str(key),zone)
                zone = cv2.cvtColor(zone, cv2.COLOR_BGR2GRAY)
                zone = cv2.GaussianBlur(zone, (21, 21), 0)
                gextractorng.back[y1:y2,x1:x2] = zone