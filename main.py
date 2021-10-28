#import camara
#import sensores as sens
import control
#import actuadores
#import asyncio
from threading import Thread
import time
#import RPi.GPIO as GPIO
from cam_thread import Camera
from sen_thread import Sensors


class Main(object):
    def __init__(self, tipoCam='grn'):    
        self.tipoCam = tipoCam
        self.constCam, self.varCam = control.defineVariablesControlCam(tipoCam)
        self.thread = Thread(target=self.update_cam, args=())
        self.thread.daemon=True
        self.thread.start()
        self.thread = Thread(target=self.update_sen, args=())
        self.thread.daemon=True
        self.thread.start()

    def update_cam(self):
        self.camera = Camera()
        if self.tipoCam == 'grn':
            while True:
                try:
                    self.camInfo = self.camera.foto_grn()
                except AttributeError:
                    self.camInfo = (240, 0)
                time.sleep(0.01)
        elif self.tipoCam == 'qr':
            while True:
                try:
                    self.camInfo = self.camera.foto()
                except AttributeError:
                    self.camInfo = (240, 0)
                time.sleep(0.01)

    def update_sen(self):
        self.sensors = Sensors()
        if self.tipoCam == 'grn':
            while True:
                try:
                    self.camInfo = self.camara.foto_grn()
                except AttributeError:
                    self.camInfo = (240, 0)
                time.sleep(0.01)
    def run(self):
        while True:
            try:
                print(self.camInfo)
                if self.camInfo != False:
                    vrCam, vlCam, varCam = control.controlCamara(qrInfo, constCam, varCam)
                else:
                    vrCam = 0
                    vlCam = 0
                #rawDist =  sens.distSensores()
                #dist, senMax = sens.adaData(rawDist)
                vrSen, vlSen, varSen = control.controlSensores(self.distSen)
            except AttributeError:
                pass


async def maintemp():
    # qr o grn
    tipoCam = "grn"
    if not camara.cam.read()[0]:
        print("fallo al detectar camara")
        return False
    constCam, varCam = control.defineVariablesControlCam(tipoCam)
    i=0
    while(True):
        ti = time.time()
        i += 1
        if tipoCam == "qr":
            infoto = asyncio.create_task(camara.foto())
        elif tipoCam == "grn":
            infoto = asyncio.create_task(camara.foto_grn())
        rawDist = await sens.distSensores()
        dist, senMax = sens.adaData(rawDist)
        #print(dist)
        #control de sensores
        vrSen, vlSen, varSen = control.controlSensores(dist)
        qrInfo = await infoto
        #print(qrInfo)
        if qrInfo != False:
            vrCam, vlCam, varCam = control.controlCamara(qrInfo, constCam, varCam)
        else:
            vrCam = 0
            vlCam = 0
        if senMax > 0.1 or qrInfo != False or vrCam > 9 or vlCam > 9:
            actuadores.enable_motors(GPIO.HIGH)
        else:
            actuadores.enable_motors(GPIO.LOW)
        vr = vrCam*varSen + vrSen
        vl = vlCam*varSen + vlSen
        #print(vlSen, vrSen)
        #print(vl, vr)
        #print(vlCam, vrCam, vlSen, vrSen, vl, vr)
        actuadores.actua(vr, vl)
        print(time.time()-ti)


if __name__ == '__main__':
    #asyncio.run(main())
    main = Main()
    main.run()
