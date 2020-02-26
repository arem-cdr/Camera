import serial,sys
import time
from datetime import datetime

class Com(object):
    def  __init__(self):
        SERIALPORT = '/dev/ttyUSB0'
        self.ser = serial.Serial(SERIALPORT)
    def send(self,msg):
        self.ser.write(str.encode(msg))
    def send_Point_list(self,l,obj_type,conf):
        k = "-101 "
        for i in l:
            k += str(obj_type)+" "+self.formatPoint(i,conf)
        k += "-1 \n"
        self.send(k)
    def formatPoint(self,p,conf):
        p.toReal(conf)
        return str(int(p.rx))+" "+str(int(p.ry)) +" "
