import serial,sys
import time
from datetime import datetime
from modules.cdrserial import *

class Com(object):
    def  __init__(self):
        SERIALPORT = '/dev/ttyUSB0'
        self.cdrser = CDRSerial(SERIALPORT, 115200)
    def send(self,msg):
        self.cdrser.send(msg)
    def send_Point_list(self,l,obj_type,conf):
        k = []
        k.append(-101)
        for i in l:
            k.append(obj_type)
            i.toReal(conf)
            k.append(int(i.rx))
            k.append(int(i.ry))
    
        k.append(-1)
        self.send(k)

    def send_Interest_list(self,l):
        k = []
        k.append(-150)
        for i in l:
            k.append(int(l))
        k.append(-1)
        self.send(k)