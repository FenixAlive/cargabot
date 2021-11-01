try:
    import RPi.GPIO as GPIO
except:
    print("error en gpio al importar")
import time
import numpy as np
import asyncio
from threading import Thread


class Sensors(object):
    def __init__(self):
        self.disMax = 0.3
        self.disMin = 0.05
        self.nSen = 6
        self.nFilter = 9
        self.w = 0.1*np.random.random_sample((self.nFilter+1,self.nSen))
        self.eta = 0.009
        self.data = np.zeros((self.nFilter+1, self.nSen))
        #GPIO numbers
        self.trig = [4,27,10,11,6,21]
        self.echo = [17,22,9,5,26,20]
        try:
            GPIO.setmode(GPIO.BCM)
            for i in range(self.nSen):
                GPIO.setup(self.trig[i], GPIO.OUT)
                GPIO.setup(self.echo[i], GPIO.IN)
            #start thread to read frames from video stream
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon=True
            self.thread.start()
        except Exception as e:
            print(e)
            self.dist = [0,0,0,0,0,0]


    def update(self):
        #read the next frame from the stream in other thread
        while True:
            self.dist = asyncio.run(self.distSensors())
            #print(self.dist)

    #take data from especific sensor
    async def readSen(self, utrig, uecho):
        #little time to rest
        GPIO.output(utrig, False)
        await asyncio.sleep(0.0001)
        GPIO.output(utrig, True)
        await asyncio.sleep(0.00001)
        GPIO.output(utrig, False)
        ti = time.time()
        while GPIO.input(uecho) == 0:
            await asyncio.sleep(0)
            if(time.time()-ti > 0.01): 
                return self.disMax
        t_start = time.time()
        while GPIO.input(uecho) == 1:
            await asyncio.sleep(0)
            if(time.time()-t_start > 0.01): 
                return self.disMax
        return (343/2)*(time.time()-t_start)


    async def distSensors(self):
        tdata = []
        for i in range(self.nSen):
            tdata.append(asyncio.create_task(self.readSen(self.trig[i], self.echo[i])))
        tdata = await asyncio.gather(*tdata)
        for i in range(self.nSen):
            if tdata[i] < self.disMax and tdata[i] > self.disMin:
                tdata[i] = 1-(tdata[i]-self.disMin)/(self.disMax-self.disMin)
            elif tdata[i] < self.disMin:
                tdata[i] = 1
            else:
                tdata[i] = 0
        return tdata


    def adaData(self):
        self.data = np.roll(self.data,shift=1,axis=0) 
        self.data[0] = self.dist
        self.data[-1] = np.ones(self.nSen)
        y = np.zeros(self.nSen)
        senMax = 0
        for n in range(self.nSen):
            x = self.data[:,n]
            wt = self.w[:,n]
            y[n] = np.dot(wt,x)
            e = self.data[0,n]-y[n]
            self.w[:,n] = self.w[:,n] + self.eta*e*x
            if y[n] > senMax:
                senMax = y[n]
        return (y, senMax)



if __name__ == '__main__':
    sensors = Sensors()
    while True:
        try:
            print(sensors.adaData())
        except AttributeError:
            pass
