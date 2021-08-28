import cv2
import numpy as np
from pyzbar.pyzbar import decode

# se guarda en variable el tamano total de la imagen
alto_img = 480
ancho_img = 640
cam = cv2.VideoCapture(0)

cam.set(3,ancho_img)
cam.set(4,alto_img)


def foto():
    ok, img = cam.read()
    if not ok:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    zero = np.zeros((alto_img, ancho_img))
    norm = cv2.normalize(gray, zero, 0, 255, cv2.NORM_MINMAX)
    blur = cv2.GaussianBlur(norm,(3,3),0)
    qrInfo = decodificarQr(blur)
    if qrInfo != False:
        return qrInfo
    return False
 #   cv2.imshow('blur', blur)
 #   cv2.waitKey(1)


def decodificarQr(img):
    decoded = decode(img)
    if decoded:
        for decoded_i in decoded:
            if decoded_i.data.decode('utf-8') == "https://github.com/FenixAlive/cargabot":
                return decoded_i.rect
    return False


if __name__ == '__main__':
    if cam.read()[0]:
        while(1):
            print(foto())
