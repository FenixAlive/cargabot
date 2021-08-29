import camara
import sensores as sens
import control
import actuadores
import asyncio
import time

async def main():
    if not camara.cam.read()[0]:
        print("fallo al detectar camara")
        return False
    constCam, varCam = control.defineVariablesControlCam()
    i=0
    while(i < 1000):
        i += 1
        infoto = asyncio.create_task(camara.foto())
        rawDist = await sens.distSensores()
        dist = sens.adaData(rawDist)
        #control de sensores
        vrSen, vlSen, varSen = control.controlSensores(dist)
        qrInfo = await infoto
        if qrInfo != False:
            vrCam, vlCam, varCam = control.controlCamara(qrInfo, constCam, varCam)
        else:
            vrCam = 0
            vlCam = 0

        vr = vrCam*varSen + vrSen
        vl = vlCam*varSen + vlSen
        #por ahora que nos falta un sensor
        vr = vrCam
        vl = vlCam
        actuadores.actua(vr, vl, dist, qrInfo)


if __name__ == '__main__':
    asyncio.run(main())
