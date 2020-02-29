import RPi.GPIO as GPIO
import time
import threading

class LEDplus():
    def __init__(self,pin):
        self.__loop = True

        self.__led_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__led_pin, GPIO.OUT)
        self.__state = 0
       

    def on(self):
        self.__loop = False
        self.maybejoin()
        self.__turnledon()

    def off(self ):
        self.__loop = False
        self.maybejoin()
        self.__turnledoff()

    def maybejoin(self):
        if self.__threading.isAlive():
            self.__threading.join()

    def blink(self, pitch):
        self.__threading = threading.Thread(target=self.__blink)
        self.__threading.start()
    
    def changeblink(self, pitch):
        self.__pitch = pitch

    def __turnledon(self):
        GPIO.output(self.__led_pin, GPIO.LOW)

    def __turnledoff(self):
        GPIO.output(self.__led_pin, GPIO.HIGH)

    def __blink(self):
        self.__loop = True
        while self.__loop:
            if(not self.__state):
                self.__turnledon()
                self.__state = 1
            else:
                self.__turnledoff()
                self.__state = 0
            time.sleep(self.__pitch/2)
        self.__turnledoff()

green = LEDplus(18)
green.blink(1)