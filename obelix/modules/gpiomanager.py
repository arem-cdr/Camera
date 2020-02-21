
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
    def update(self):
        if(GPIO.input(15) != self.led):
            if(self.led):
                GPIO.output(14,GPIO.LOW)
                GPIO.output(18,GPIO.HIGH)
            else:
                GPIO.output(18,GPIO.LOW)
                GPIO.output(14,GPIO.HIGH)
            self.led = GPIO.input(15)
        if(self.blink):
            GPIO.output(23,GPIO.LOW)
            self.blink = 0
        else:
            GPIO.output(23,GPIO.HIGH)
            self.blink = 1
