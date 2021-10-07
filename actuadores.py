import os
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#enable pin GPIO 26
enable_pin = 26

GPIO.setup(enable_pin, GPIO.OUT)
#motors off at start
GPIO.output(enable_pin, GPIO.LOW)

#direction pins [[right1, 2], [left1, 2]]
direction = [[7, 8], [23, 24]]
for i in range(0,2):
    for j in range(0,2):
        GPIO.setup(direction[i][j], GPIO.OUT)
        GPIO.output(direction[i][j], GPIO.LOW)

#PWM0 GPIO 18, PWM1 GPIO 13
# 18 derecha, 13 izquierda
pwm_pin = [18, 13]

#setup pines as outputs and start at 0 dutyCycle
pwm = []
for i in range(0,2):
    GPIO.setup(pwm_pin[i], GPIO.OUT)
    pwm.append(GPIO.PWM(pwm_pin[i], 1000))
    pwm[i].start(0)


#setup pins for direction in H bridge
def actua(vr, vl):
    vr= vr+0.5
    if vl >= 100:
        vl = 100
    v = [vr, vl]
    for i in range(0,2):
        if v[i] > 0:
            GPIO.output(direction[i][0], GPIO.HIGH)
            GPIO.output(direction[i][1], GPIO.LOW)
        else:
            GPIO.output(direction[i][0], GPIO.LOW)
            GPIO.output(direction[i][1], GPIO.HIGH)
            v[i] = abs(v[i])

        if v[i] >= 100:
            v[i] = 100
        pwm[i].ChangeDutyCycle(v[i])


def verActua(vr, vl, sens, qrInfo):
    os.system("clear")
    print("")
    print("  |{:.2f}| |{:.2f}| |{:.2f}| |{:.2f}|".format(sens[3], sens[2], sens[1], sens[0]))
    print("")
    if qrInfo != False:
        print("")
        print(qrInfo)
        print("")
        print("           |--o--|")
    else:
        print("")
        print("")
        print("")
        print("           |-----|")
    print("           |--A--|")
    print("    |{:2.2f}|-|-----|-|{:2.2f}|".format(vl,vr))
    print("           |-----|")
    print("    |{:2.2f}|-|-----|-|{:2.2f}|".format(vl,vr))
    print("")
    print("    |{:.2f}| |{:.2f}| |{:.2f}| |{:.2f}]|".format(sens[4], sens[5], sens[6], sens[7]))
    print("")

if __name__ == '__main__':
    for i in range(-100,101):
        actua(i,i)
        time.sleep(0.3)

