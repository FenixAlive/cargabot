try:
    import RPi.GPIO as GPIO
    import actuators
except:
    print('falla en gpio')
import control
from threading import Thread
import time
from cam_thread import Camera
from sen_thread import Sensors


class Main(object):
    def __init__(self, tipo_cam='grn'):    
        self.tipo_cam = tipo_cam
        self.const_cam, self.var_cam = control.define_variables_control_cam(tipo_cam)
        self.thread = Thread(target=self.update_cam, args=())
        self.thread.daemon=True
        self.thread.start()
        self.thread = Thread(target=self.update_sen, args=())
        self.thread.daemon=True
        self.thread.start()


    def update_cam(self):
        self.camera = Camera()
        if self.tipo_cam == 'grn':
            while True:
                try:
                    self.cam_info = self.camera.foto_grn()
                except AttributeError:
                    self.cam_info = (240, 0)
                time.sleep(0.01)
        elif self.tipo_cam == 'qr':
            while True:
                try:
                    self.cam_info = self.camera.foto()
                except AttributeError:
                    self.cam_info = (240, 0)
                time.sleep(0.01)


    def update_sen(self):
        self.sensors = Sensors()
        while True:
            try:
                self.dist_sen, self.sen_max = self.sensors.adaData()
            except AttributeError:
                self.dist_sen, self.sen_max = ([0,0,0,0,0,0], 0)
            time.sleep(0.01)


    def run(self):
        while True:
            #ti = time.time()
            try:
                #print(self.cam_info)
                if self.cam_info != False:
                    vr_cam, vl_cam, self.var_cam = control.control_camera(self.cam_info, self.const_cam, self.var_cam)
                else:
                    vr_cam = 0
                    vl_cam = 0
                vr_sen, vl_sen, var_sen = control.control_sensors(self.dist_sen)
                vr = vr_cam*var_sen + vr_sen
                vl = vl_cam*var_sen + vl_sen
                try:
                    if self.sen_max > 0.1 or self.cam_info != False or vr_cam > 3 or vl_cam > 3:
                        actuators.enable_motors(GPIO.HIGH)
                    else:
                        actuators.enable_motors(GPIO.LOW)
                    actuators.actua(vr, vl)
                except:
                    print("error al actuar")
            except AttributeError:
                pass
            #print(time.time()-ti)


async def maintemp():
    # qr o grn
    tipo_cam = "grn"
    if not camara.cam.read()[0]:
        print("fallo al detectar camara")
        return False
    const_cam, var_cam = control.defineVariablesControlCam(tipo_cam)
    i=0
    while(True):
        ti = time.time()
        i += 1
        if tipo_cam == "qr":
            infoto = asyncio.create_task(camara.foto())
        elif tipo_cam == "grn":
            infoto = asyncio.create_task(camara.foto_grn())
        #print(dist)
        #control de sensores
        vrSen, vlSen, varSen = control.controlSensores(dist)
        qrInfo = await infoto
        #print(qrInfo)
        if qrInfo != False:
            vrCam, vlCam, var_cam = control.controlCamara(qrInfo, const_cam, var_cam)
        else:
            vrCam = 0
            vlCam = 0
        if sen_max > 0.1 or qrInfo != False or vrCam > 9 or vlCam > 9:
            actuators.enable_motors(GPIO.HIGH)
        else:
            actuators.enable_motors(GPIO.LOW)
        vr = vrCam*varSen + vrSen
        vl = vlCam*varSen + vlSen
        #print(vlSen, vrSen)
        #print(vl, vr)
        #print(vlCam, vrCam, vlSen, vrSen, vl, vr)
        actuators.move(vr, vl)
        print(time.time()-ti)


if __name__ == '__main__':
    main = Main()
    main.run()
