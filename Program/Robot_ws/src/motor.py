#! /usr/bin/env python3

__author__ = "Mohamed Amine Ben Ammar"
__date__ = "05/03/2022"

import RPi.GPIO as GPIO 
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor:
    def __init__(self, in1, in2, en, maxSpeed = 100):
        self.maxSpeed = maxSpeed
        self.in1 = in1
        self.in2 = in2
        self.en = en
        GPIO.setup(self.in1,GPIO.OUT)   
        GPIO.setup(self.in2,GPIO.OUT)   
        GPIO.setup(self.en,GPIO.OUT)    
        self.pwm = GPIO.PWM(self.en, 100) 
        self.pwm.start(0)

    def forwards(self, x):
        GPIO.output(self.in1,GPIO.HIGH) 
        GPIO.output(self.in2,GPIO.LOW)  
        self.pwm.ChangeDutyCycle(x)    

    def backwards(self, x):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        self.pwm.ChangeDutyCycle(x)

    def stop(self):
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.HIGH)
        self.pwm.ChangeDutyCycle(0)