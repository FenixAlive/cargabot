import camara
import sensores as sens
import control
import actuadores
import asyncio
import time
import RPi.GPIO as GPIO

async def main():
    if not camara.cam.read()[0]:
        print("fallo al detectar camara")
        return False
    constCam, varCam = control.defineVariablesControlCam()
    i=0
    while(True):
        i += 1
        infoto = asyncio.create_task(camara.foto())
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
        if senMax > 0.1 or qrInfo != False:
            actuadores.enable_motors(GPIO.HIGH)
        else:
            actuadores.enable_motors(GPIO.LOW)
        vr = vrCam*varSen + vrSen
        vl = vlCam*varSen + vlSen
        #print(vlSen, vrSen)
        #print(vl, vr)
        print(vlCam, vrCam, vlSen, vrSen, vl, vr)
        actuadores.actua(vr, vl)


if __name__ == '__main__':
    asyncio.run(main())
