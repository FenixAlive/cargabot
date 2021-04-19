import RPi.GPIO as GPIO
import time

trig = 21
echo = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def dis():
    GPIO.output(trig, False)
    time.sleep(0.000002)        # 2us
    GPIO.output(trig, True)
    time.sleep(0.000005)        # 5us
    GPIO.output(trig, False)
    while GPIO.input(echo) == 0:
        t_start = time.time()
    while GPIO.input(echo) == 1:
        t_end = time.time()
    t = t_end-t_start
    d = (34300/2)*t             # cm/s * s
    #d = (0.0343/2)*t            # cm/us
    return d

if __name__ == '__main__':
    while(1):
        print(dis()," cm")


