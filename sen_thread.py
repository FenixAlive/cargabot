import RPi.GPIO as GPIO
import time
import numpy as np


class Sensors(object):
    def __init__(self):
        self.disMax = 0.3
        self.disMin = 0.05
        self.nSen = 6
        self.nFilter = 9
        self.w = 0.1*np.random.random_sample((self.nFilter+1,self.nSen))
        self.eta = 0.009
        self.data = np.zeros((self.nFilter+1, self.nSen))
        GPIO.setmode(GPIO.BCM)
        #GPIO numbers
        self.trig = [4,27,10,11,6,21]
        self.echo = [17,22,9,5,26,20]
        for i in range(len(trig)):
            GPIO.setup(self.trig[i], GPIO.OUT)
            GPIO.setup(self.echo[i], GPIO.IN)
        #start thread to read frames from video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon=True
        self.thread.start()


    def update(self):
        #read the next frame from the stream in other thread
        while True:
