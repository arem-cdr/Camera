
import RPi.GPIO as GPIO


class GpioManager(object):
    def  __init__(self):
        self.led = 0
        self.blink = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(23,GPIO.OUT)
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(14,GPIO.OUT)
        #self.led20 = Led(20)
        #self.led21 = Led(21)
        
        self.led = GPIO.input(15)
        if(self.led):
                GPIO.output(14,GPIO.LOW)
                GPIO.output(18,GPIO.HIGH)
        else:
            GPIO.output(18,GPIO.LOW)
            GPIO.output(14,GPIO.HIGH)

    def update(self, aruco_pos, conf):
        #self.calib_blink(aruco_pos, conf)
        if(GPIO.input(15) != self.led):
            if(self.led):
                GPIO.output(14,GPIO.LOW)
                GPIO.output(18,GPIO.HIGH)
            else:
                GPIO.output(18,GPIO.LOW)
                GPIO.output(14,GPIO.HIGH)
            self.led = GPIO.input(15)
            return 1
        if(self.blink):
            GPIO.output(23,GPIO.LOW)
            self.blink = 0
        else:
            GPIO.output(23,GPIO.HIGH)
            self.blink = 1
        return 0
    
    """ def calib_blink(self,aruco_pos, conf):
        if(len(aruco_pos)!=2):
            if(len(aruco_pos)==1):
                self.led20.on()
            return 
        
        x = aruco_pos[0]
        y = aruco_pos[1]
        diffx = abs(conf.loc_aruco_x-x)
        diffy = abs(conf.loc_aruco_y-y)
        diffx = 10
        diffy = 20

        min_t = 0.1
        max_t = 1
        min_diff = 5
        max_diff = 100
        a = (max_t-min_t)/(max_diff-min_diff)
        b = min_diff - a*min_t
        if(diffx< 5):
            self.led20.on()
        else:
            self.led20.blink(0.05, (diffx-b)/a)
        if(diffy< 5):
            self.led21.on()
        else:
            self.led21.blink(0.05, (diffy-b)/a) """
        