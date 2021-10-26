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

qrDecoder = cv2.QRCodeDetector()

async def foto():
    await asyncio.sleep(0)
    ok, img = cam.read()
    if not ok:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    zero = np.zeros((alto_img, ancho_img))
    norm = cv2.normalize(gray, zero, 0, 255, cv2.NORM_MINMAX)
    #blur = cv2.GaussianBlur(norm,(3,3),0)
    #cv2.waitKey(1)
    return decodificarQr(norm)


def decodificarQr(img):
    decoded = decode(img)
    if decoded:
        for decoded_i in decoded:
            if decoded_i.data.decode('utf-8') == "git@github.com:FenixAlive/cargabot.git":
                return (decoded_i.rect.left+decoded_i.rect.width/2, decoded_i.rect.height)
    return False

def decodificarQrCV(img):
    ti = time.time()
    global qrDecoder
    data, bbox, rectImg = qrDecoder.detectAndDecode(img) 
    print(time.time()-ti)


async def foto_grn():
    t = time.time()
    ok, img = cam.read()
    if not ok:
        return False
    #img = cv2.imread("round.jpg")
    zero = np.zeros((alto_img, ancho_img))
    img = cv2.normalize(img, zero, 0, 255, cv2.NORM_MINMAX)
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    #cv2.imshow("lab", img_lab[:,:,2])
    #tam = img.shape
    #Rc = 30*np.ones((tam[0],tam[1]), dtype='float64')
    #Gc = 150*np.ones((tam[0],tam[1]), dtype='float64')
    #Bc = 30*np.ones((tam[0],tam[1]), dtype='float64')
    #r = 70
    #img_bn = (Rc-img[:,:,0])**2 + (Gc-img[:,:,1])**2 + (Bc-img[:,:,2])**2
    #img_bn = np.power(Rc-img[:,:,0],2) + np.power(Gc-img[:,:,1],2) + np.power(Bc-img[:,:,2],2)
    #img_bn = np.uint8(255*(img_bn<=(r^2)))
    #img_bn = (Rc-(img[:,:,0].astype(np.float64)))**2+(Gc-(img[:,:,1].astype(np.float64)))**2+(Bc-(img[:,:,2].astype(np.float64)))**2
    #img_bn = 255*(img_bn <= r**2)
    #img_bn = img_bn.astype(np.uint8)
    img_bn = ((img_lab[:,:,1] < 107) & (img_lab[:,:,2] > 50) & (img_lab[:,:,2] < 170) )*255
    img_bn = img_bn.astype(np.uint8)
    img_bn = cv2.erode(img_bn, None, iterations=3)
    img_bn = cv2.dilate(img_bn, None, iterations=3)
    #l_green = (144,200,144)
    #d_green = (10,238,10)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    #img_bn = cv2.inRange(hsv_img,l_green,d_green)
    #_ = cv2.bitwise_and(img, img,mask=img_bn)
    xc,yc, area = foto_data(img_bn)
    if xc == False or area < 200:
        return False
    #cv2.imshow("orig", img)
    #img_cir = cv2.circle(img, (xc, yc), int((area/3.139)**0.5), (200,0,200),5)
    #cv2.imshow("bin", img_cir)
    #cv2.waitKey(0)
    await asyncio.sleep(0)
    return (xc,2*(area/3.139)**0.5)

def foto_data(img_bn):
    M = cv2.moments(img_bn)
    if M["m00"] != 0:
        xc = int(M["m10"]/M["m00"])
        yc = int(M["m01"]/M["m00"])
    else:
        return False, False, False
    area = sum(sum(img_bn/255))
    return (xc, yc, area)


if __name__ == '__main__':
    if cam.read()[0]:
        i = 0
        #asyncio.run(foto())
        while(i < 100):
            i+=1
            #ti=time.time()
            #asyncio.run(foto())
            #asyncio.run(foto_grn())
            #print(asyncio.run(foto()))
            #print(time.time()-ti)

