import RPi.GPIO as GPIO
import time
import numpy as np
import asyncio

# Inicializamos gpio para tomar data de sensores
GPIO.setmode(GPIO.BCM)
#GPIO numbers
trig = [4,27,10,11,6,21]
echo = [17,22,9,5,26,20]
for i in range(len(trig)):
    GPIO.setup(trig[i], GPIO.OUT)
    GPIO.setup(echo[i], GPIO.IN)

disMax = 0.3
disMin = 0.05
nSen = len(trig)
nFiltro = 9
w = 0.1*np.random.random_sample((nFiltro+1,nSen))
eta = 0.009
data = np.zeros((nFiltro+1, nSen))


#toma la distancia de un sensor en especifico
async def readSen(utrig, uecho):
    #tiempo para descansar
    GPIO.output(utrig, False)
    await asyncio.sleep(0.0001)
    GPIO.output(utrig, True)
    await asyncio.sleep(0.00001)
    GPIO.output(utrig, False)
    ti = time.time()
    while GPIO.input(uecho) == 0:
        await asyncio.sleep(0)
        if(time.time()-ti > 0.01): 
            return disMax
    t_start = time.time()
    while GPIO.input(uecho) == 1:
        await asyncio.sleep(0)
        if(time.time()-t_start > 0.01): 
            return disMax
    return (343/2)*(time.time()-t_start)


async def distSensores():
    tdata = []
    for i in range(nSen):
        tdata.append(asyncio.create_task(readSen(trig[i], echo[i])))
    tdata = await asyncio.gather(*tdata)
    for i in range(nSen):
        if tdata[i] < disMax and tdata[i] > disMin:
            tdata[i] = 1-(tdata[i]-disMin)/(disMax-disMin)
        elif tdata[i] < disMin:
            tdata[i] = 1
        else:
            tdata[i] = 0
    return tdata


def adaData(dist):
    global data
    data = np.roll(data,shift=1,axis=0) 
    data[0] = dist
    data[-1] = np.ones(nSen)
    y = np.zeros(nSen)
    #print("---Pesos----")
    #print(w)
    senMax = 0
    for n in range(nSen):
        #print("sensor: {}".format(n))
        x = data[:,n]
        #print(x)
        wt = w[:,n]
        #print(wt)
        y[n] = np.dot(wt,x)
        #print(y[n])
        e = data[0,n]-y[n]
        #print(e)
        w[:,n] = w[:,n] + eta*e*x
        if y[n] > senMax:
            senMax = y[n]
    return [y, senMax]


if __name__ == '__main__':
    for i in range(3000):
        #ti = time.time()
        dist = asyncio.run(distSensores())
        y,senMax = adaData(dist)
        #print(time.time()-ti)
        print(np.round_(y,decimals=2))
        #print("{:.6f}, {:.6f}".format(data[0,1],y[1]))
    GPIO.cleanup()
    
