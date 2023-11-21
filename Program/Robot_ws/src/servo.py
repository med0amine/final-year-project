#! /usr/bin/env python3

__author__ = "Mohamed Amine Ben Ammar"
__date__ = "12/03/2022"

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Servo:
    def __init__(self, pin, MIN_DUTY = 5, MAX_DUTY = 10):
        self.pin = pin
        self.MIN_DUTY = MIN_DUTY
        self.MAX_DUTY = MAX_DUTY
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.pwm(self.pin, 50)
        self.pwm.start()

    def deg_to_duty(self, x):
        return (x - 0) * (self.MAX_DUTY- self.MIN_DUTY) / 180 + self.MIN_DUTY

    def turn(self, x):
        if (x > 180):
            x = 180
        elif (x < 0):
            x = 0;
        duty_cycle = deg_to_duty(x)
        self.pwm.ChangeDutyCycle(duty_cycle)