#!/usr/bin/env python3
import Adafruit_PCA9685
import sys


if len(sys.argv) !=2:
    print('Usage: {} <run type>'.format(sys.argv[0]))
    sys.exit(2)

situation = sys.argv[1]

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

def start_V():
    pwm.set_pwm(0,0,420)
    pwm.set_pwm(1,0,390)

start_V()


if situation == "STOP":
    pwm.set_pwm(0,0,389)
    pwm.set_pwm(1,0,390)

