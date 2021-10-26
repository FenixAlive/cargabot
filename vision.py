import numpy as np
import cv2
import time

img=cv2.imread("seg.jpg")
fil, col, _ = img.shape
Rc = 0*np.ones((fil, col), dtype='float64')
Gc = 250*np.ones((fil, col), dtype='float64')
Bc = 0*np.ones((fil, col), dtype='float64')
r = 100
imgBn = (Rc-(img[:,:,0].astype(np.float64)))**2+(Gc-(img[:,:,1].astype(np.float64)))**2+(Bc-(img[:,:,2].astype(np.float64)))**2
imgBn = 255*(imgBn <= r**2)
imgBn = imgBn.astype(np.uint8)
izq = False
ti = time.time()
for i in range(col):
    for j in range(fil):
        if(imgBn[j,i]):
            print(i,j)
            izq = True
            break
    if izq:
        break
print(time.time()-ti)
print(imgBn.shape)
print(fil, col)
#print(imgBn)
#cv2.imshow("img",(img[:,:,2]+img[:,:,0])/2)
cv2.imshow("img", imgBn)
cv2.waitKey(0)
