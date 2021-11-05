from threading import Thread
import cv2, time
import numpy as np
from pyzbar.pyzbar import decode

class Camera(object):
    def __init__(self, src=0, width=640, height=480):
        self.capture=cv2.VideoCapture(src)
        self.width = width
        self.height = height
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        #start thread to read frames from video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon=True
        self.thread.start()


    def update(self):
        #read the next frame from the stream in other thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read() 
                time.sleep(0.01)


    def show_frame(self):
        #display frame in main thread
        cv2.imshow('frame', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)


    def foto_data(self, img_bn):
        M = cv2.moments(img_bn)
        if M["m00"] != 0:
            xc = int(M["m10"]/M["m00"])
            yc = int(M["m01"]/M["m00"])
        else:
            return False, False, False
        area = sum(sum(img_bn/255))
        return (xc, yc, area)


    def foto_grn(self):
        img_lab = cv2.cvtColor(self.frame, cv2.COLOR_BGR2LAB)
        img_bn = ((img_lab[:,:,0] > 30) & (img_lab[:,:,0] < 220) & ((img_lab[:,:,1] > 0) & (img_lab[:,:,1] < 95)) & (img_lab[:,:,2] > 120) & (img_lab[:,:,2] < 190))*255
        img_bn = img_bn.astype(np.uint8)
        img_bn = cv2.erode(img_bn, None, iterations=1)
        img_bn = cv2.dilate(img_bn, None, iterations=3) 
        #cv2.imshow('img_bn', img_bn)
        #key = cv2.waitKey(0)
        xc,yc, area = self.foto_data(img_bn)
        if xc == False or area < 100:
            return False
        return (xc,2*(area/3.139)**0.5)


    def photo_hsv(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        lower = np.array([50,100,50])
        upper = np.array([80,200,150])
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2) 
        #cv2.imshow('mask', mask)
        #key = cv2.waitKey(1)
        xc,yc, area = self.foto_data(mask)
        if xc == False or area < 100:
            return False
        return (xc,2*(area/3.139)**0.5)

    def cal_foto(self, kind, channel, min_val, max_val):
        img = cv2.cvtColor(self.frame, kind)
        img_bn = ((img[:,:,channel] > min_val) & (img[:,:,channel] < max_val))*255
        img_bn = img_bn.astype(np.uint8)
        cv2.imshow('img'+str(channel), img[:,:,channel])
        cv2.imshow('img_bn', img_bn)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)


    def foto(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        zero = np.zeros((self.height, self.width))
        norm = cv2.normalize(gray, zero, 0, 255, cv2.NORM_MINMAX)
        return self.decodificarQr(norm)


    def decodificarQr(self, img):
        decoded = decode(img)
        if decoded:
            for decoded_i in decoded:
                if decoded_i.data.decode('utf-8') == "git@github.com:FenixAlive/cargabot.git":
                    return (decoded_i.rect.left+decoded_i.rect.width/2, decoded_i.rect.height)
        return False



if __name__ == '__main__':
    video = Camera(width=640, height=480)
    i = 0
    while True:
        try:
            #video.cal_foto(cv2.COLOR_BGR2HSV,2,50,150)
            ti = time.time()
            print(video.photo_hsv())
            print(time.time()-ti)
            #if i > 9:
                #break
            i = i+1
            #video.show_frame()
            #print(video.foto_grn())
        except AttributeError:
            pass
