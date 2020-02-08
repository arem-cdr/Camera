import serial,sys
import time
from datetime import datetime


SERIALPORT = '/dev/ttyUSB0'

ser = serial.Serial(SERIALPORT)
i=0
while 1:
	#d = str(int(round(time.time()*1000)))
	ser.write(str.encode(str(i)))
	print(i)
	time.sleep(1/2)
	i+=1

