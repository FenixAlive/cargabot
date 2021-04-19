import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
trig = [21, 6, 19]
echo = [20, 5, 13]
for i in range(len(trig)):
    GPIO.setup(trig[i], GPIO.OUT)
    GPIO.setup(echo[i], GPIO.IN)

def dis(trig, echo):
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

def data(trig, echo):
    data = []
    for i in range(len(trig)):
        data.append(dis(trig[i], echo[i]))
        time.sleep(0.01)        # 2us
    return data




if __name__ == '__main__':
    while(1):
        for i in range(len(trig)):
            print("Sensor {}: {} cm".format(i, dis(trig[i], echo[i])))
            time.sleep(0.01)        # 2us
        time.sleep(0.2)        # 2us
        print("-------------")


