import camara
import sensores as sens
import control
import actuadores
import asyncio
import time
import RPi.GPIO as GPIO


async def main():
    tipoCam = "qr"
    if not camara.cam.read()[0]:
        print("fallo al detectar camara")
        return False
    constCam, varCam = control.defineVariablesControlCam(tipoCam)
    i=0
    while(True):
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


if __name__ == '__main__':
    asyncio.run(main())
