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
    i=0
    while(i < 5000):
        ti = time.time()
        i += 1
        infoto = asyncio.create_task(camara.foto())
        rawDist = await sens.distSensores()
        dist = sens.adaData(rawDist)
        infoto = await infoto
        print(time.time()-ti)
        if infoto:
            print("QR: ", infoto)
            #sensores
            #tomar decisiones con los datos (control)
            #actuadores

if __name__ == '__main__':
    asyncio.run(main())
