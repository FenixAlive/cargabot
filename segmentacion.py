import cv2
import numpy as np
from time import time

alto_img = 480
ancho_img = 640
cam = cv2.VideoCapture(0)

cam.set(3,ancho_img)
cam.set(4,alto_img)

def fotoverde():
    t = time()
    ok, img = cam.read()
    if not ok:
        return False
    #img = cv2.imread("round.jpg")

    tam = img.shape
    Rc = 10*np.ones((tam[0],tam[1]), dtype='float64')
    Gc = 120*np.ones((tam[0],tam[1]), dtype='float64')
    Bc = 10*np.ones((tam[0],tam[1]), dtype='float64')
    r = 70

    #img_bn = (Rc-img[:,:,0])**2 + (Gc-img[:,:,1])**2 + (Bc-img[:,:,2])**2
    #img_bn = np.power(Rc-img[:,:,0],2) + np.power(Gc-img[:,:,1],2) + np.power(Bc-img[:,:,2],2)
    #img_bn = np.uint8(255*(img_bn<=(r^2)))
    img_bn = (Rc-(img[:,:,0].astype(np.float64)))**2+(Gc-(img[:,:,1].astype(np.float64)))**2+(Bc-(img[:,:,2].astype(np.float64)))**2
    img_bn = 255*(img_bn <= r**2)
    img_bn = img_bn.astype(np.uint8)
    img_bn = cv2.erode(img_bn, None, iterations=1)
    img_bn = cv2.dilate(img_bn, None, iterations=1)
    #l_green = (144,200,144)
    #d_green = (10,238,10)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    #img_bn = cv2.inRange(hsv_img,l_green,d_green)
    #_ = cv2.bitwise_and(img, img,mask=img_bn)

    xc,yc,area = foto_data(img_bn)

    print("{:.8f} \t C: ({},{}) \t A: {}p".format(time()-t,xc,yc,int(area)))
    cv2.imshow("orig", img)
    cv2.imshow("hsv", hsv_img)
    cv2.imshow("bin", img_bn)
    cv2.waitKey(0)
    return xc,yc,area

def foto_data(img_bn):
    M = cv2.moments(img_bn)
    if M["m00"] != 0:
        xc = int(M["m10"]/M["m00"])
        yc = int(M["m01"]/M["m00"])
    else:
        xc = None
        yc = None
    area = sum(sum(img_bn/255))
    return xc,yc,area


if __name__ == '__main__':
    if cam.read()[0]:
        i = 0
        while(i < 1):
            xc, yc, area = fotoverde()
            i+=1

#cv2.circle(img,(xc,yc),5,(0,0,0),-1)
#cv2.imshow("orig", img)
#cv2.imshow("bin", img_bn)
#cv2.waitKey(0)
