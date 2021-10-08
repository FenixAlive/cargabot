import cv2
import numpy as np
from pyzbar.pyzbar import decode
import asyncio
import time

# se guarda en variable el tamano total de la imagen
alto_img = 480
ancho_img = 640
cam = cv2.VideoCapture(0)

cam.set(3,ancho_img)
cam.set(4,alto_img)


async def foto():
    await asyncio.sleep(0)
    ok, img = cam.read()
    if not ok:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    zero = np.zeros((alto_img, ancho_img))
    norm = cv2.normalize(gray, zero, 0, 255, cv2.NORM_MINMAX)
    #blur = cv2.GaussianBlur(norm,(3,3),0)
    cv2.waitKey(1)
    return decodificarQr(norm)


def decodificarQr(img):
    decoded = decode(img)
    if decoded:
        for decoded_i in decoded:
            if decoded_i.data.decode('utf-8') == "git@github.com:FenixAlive/cargabot.git":
                return decoded_i.rect
    return False


if __name__ == '__main__':
    if cam.read()[0]:
        i = 0
        while(i < 1000):
            i+=1
            ti=time.time()
            asyncio.run(foto())
            print(time.time()-ti)
            #print(asyncio.run(foto()))

