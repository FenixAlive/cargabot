import os
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#enable pin GPIO 26
enable_pin = 16

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
def move(vr, vl):
    safe_duty = 90
    v = [vr, vl]
    for i in range(0,2):
        if v[i] > 0:
            GPIO.output(direction[i][0], GPIO.HIGH)
            GPIO.output(direction[i][1], GPIO.LOW)
        else:
            GPIO.output(direction[i][0], GPIO.LOW)
            GPIO.output(direction[i][1], GPIO.HIGH)
            v[i] = abs(v[i])
        if v[i] > safe_duty:
            v[i] = safe_duty
        pwm[i].ChangeDutyCycle(v[i])

def enable_motors(val):
    GPIO.output(enable_pin, val)


def watch_moving(vr, vl, sens, img_info):
    os.system("clear")
    print("")
    print("  |{:.2f}| |{:.2f}| |{:.2f}|".format(sens[2], sens[1], sens[0]))
    print("")
    if qrInfo != False:
        print("")
        print(img_info)
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
    print("    |{:.2f}| |{:.2f}| |{:.2f}|".format(sens[3], sens[4], sens[5]))
    print("")

if __name__ == '__main__':
    GPIO.output(enable_pin, GPIO.HIGH)
    for i in range(-100,101):
        actua(i,i)
        print(i,i)
        time.sleep(0.1)

