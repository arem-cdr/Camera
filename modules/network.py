import serial,sys
import time
from datetime import datetime

class Com(object):
    def  __init__(self):
        SERIALPORT = '/dev/ttyUSB0'
        self.ser = serial.Serial(SERIALPORT)
    def send(self,msg):
        self.ser.write(str.encode(msg))
    def send_Point_list(self,l):
        for i in l:
            self.send(self.formatPoint(i))
    def formatPoint(self,p):
        return str(int(p.x))+" ,"+str(int(p.y)) +" |"
