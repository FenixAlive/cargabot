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
    def __init__(self, cam_type='grn'):    
        self.cam_type = cam_type
        self.const_cam, self.var_cam = control.define_variables_control_cam(cam_type)
        self.thread = Thread(target=self.update_cam, args=())
        self.thread.daemon=True
        self.thread.start()
        self.thread = Thread(target=self.update_sen, args=())
        self.thread.daemon=True
        self.thread.start()


    def update_cam(self):
        self.camera = Camera(width=640, height=480)
        if self.cam_type == 'grn':
            while True:
                try:
                    self.cam_info = self.camera.foto_grn()
                except AttributeError:
                    self.cam_info = (240, 0)
                time.sleep(0.01)
        elif self.cam_type == 'qr':
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
                    actuators.move(vr, vl)
                except:
                    print("error al actuar")
            except AttributeError:
                pass
            #print(time.time()-ti)



if __name__ == '__main__':
    main = Main()
    main.run()
