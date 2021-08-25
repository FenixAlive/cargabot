import RPi.GPIO as GPIO
import time
import numpy as np

# Inicializamos gpio para tomar data de sensores
GPIO.setmode(GPIO.BCM)
trig = [5, 10, 27, 4, 7, 9, 20] #26
echo = [6, 11, 22, 17, 25, 8, 16] #21
for i in range(len(trig)):
    GPIO.setup(trig[i], GPIO.OUT)
    GPIO.setup(echo[i], GPIO.IN)

disMax = 120
nSen = len(trig)
nFiltro = 7
nVeces = 3
w = 0.1*np.random.random_sample((nFiltro+1,nSen))
eta = 0.000007
data = np.zeros((nFiltro+1, nSen))
#toma la distancia de un sensor en especifico
def dis(utrig, uecho):
    #tiempo para descansar
    GPIO.output(utrig, False)
    time.sleep(0.00005)
    GPIO.output(utrig, True)
    time.sleep(0.00001) 
    GPIO.output(utrig, False)
    t_start = time.time()
    t_end = time.time()
    while GPIO.input(uecho) == 0:
        t_start = time.time()
    while GPIO.input(uecho) == 1:
        t_end = time.time()
    distancia = (34300/2)*(t_end-t_start)
    if distancia < disMax:
        return distancia
    else:
        return disMax
    return              # cm/s * s


def senData():
    tdata = np.zeros(nSen)
    for i in range(nVeces):
        for i in range(nSen):
            tdata[i] += dis(trig[i], echo[i])
    return np.divide(tdata,nVeces)


def senOne():
    tdata = np.zeros(nSen)
    for i in range(nSen):
        tdata[i] = dis(trig[i], echo[i])
    return tdata

def adaData():
    global data
    data = np.roll(data,shift=1,axis=0) 
    data[0] = senOne()
    data[-1] = np.ones(nSen)
    y = np.zeros(nSen)
    #print("---Pesos----")
    #print(w)
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
    return y


if __name__ == '__main__':
    try:
        for i in range(500):
            #print("-----Data-----")
            #print(data)
            y = adaData()
            print(np.round_(y,decimals=2))
            #print("{:.2f}, {:.2f}".format(data[0,6],y[6]))
        GPIO.cleanup()
    except:
        print("error en algo")
        GPIO.cleanup()
    
