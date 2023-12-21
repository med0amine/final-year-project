"""
   Copyright [2023] [Mohamed Amine Ben Ammar]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
#! /usr/bin/env python3

__author__ = "Mohamed Amine Ben Ammar"
__date__ = "24/05/2022"

import RPi.GPIO as GPIO
import cv2
import sys
from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from motor import Motor
from servo import Servo
from flask_basicauth import BasicAuth
import time
from time import sleep
import threading
import serial
import adafruit_us100


email_update_interval = 10 

video_camera = VideoCamera(flip=False)
object_classifier = cv2.CascadeClassifier(
    "models/fullbody_recognition_model.xml") 

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'robot'
app.config['BASIC_AUTH_PASSWORD'] = 'mohamedamine'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
us100 = adafruit_us100.US100(uart)

ser = serial.Serial("/dev/tty/USB0", baudrate=9600, timeout=1)


buzzer = 25
GPIO.setup(buzzer, GPIO.OUT)

motor1 = Motor(18, 23, 24)
motor2 = Motor(22, 27, 17)

servo1 = Servo(5)
servo2 = Servo(6)
x = 0
y = 0
servo1.turn(x)
servo2.turn(y)

def check_for_objects():
    global last_epoch
    while True:
        try:
            frame, found_obj = video_camera.get_object(object_classifier)
            if found_obj and (time.time() - last_epoch) > email_update_interval:
                last_epoch = time.time()
                GPIO.output(buzzer, GPIO.HIGH)
                sleep(2)
                GPIO.output(buzzer, GPIO.LOW)
                sleep(0.5)
                print ("Sending email...")
                sendEmail(frame)
                print ("done!")
        except:
            print ("Error sending email: ", sys.exc_info()[0])


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/left_side')
def left_side():
    data1 = "LEFT"
    motor1.forwards(90)
    motor2.backwards(90)
    return 'true'


@app.route('/right_side')
def right_side():
    data1 = "RIGHT"
    motor1.backwards(90)
    motor2.forwards(90)
    return 'true'


@app.route('/up_side')
def up_side():
    data1 = "FORWARD"
    motor1.forwards(60)
    motor2.forwards(60)
    return 'true'


@app.route('/down_side')
def down_side():
    data1 = "BACK"
    motor1.backwards(60)
    motor2.backwards(60)
    return 'true'


@app.route('/stop')
def stop():
    data1 = "STOP"
    motor1.stop()
    motor2.stop()
    return 'true'

@app.route('/s1r')
def servxoright():
    data1 = "SERVOXRIGHT"
    x = x + 10
    servo1.turn(x)
    return 'true'

@app.route('/s1l')
def servoxleft():
    data1 = "SERVOXLEFT"
    x = x - 10
    servo1.turn(x)
    return 'true'

@app.route('/s2u')
def servoyup():
    data1 = "SERVOYUP"
    y = y + 10
    servo1.turn(y)
    return 'true'

@app.route('/s2d')
def servoydown():
    data1 = "SERVOYDOWN"
    y = y - 10
    servo1.turn(y)
    return 'true'

@app.route('/autome_navigation')
def autonome():
    data1 = "ON"
    try:
       while True:
          usL = ser.read(distanceLeft)
          usD = ser.read(distanceRight)
          if  us100.distance <= 20 & int.from_byte(number, byteorder='big') == 2: #us right
              motor1.backwards(80)
              motor2.forwards(80)
          elif us100.distance <= 20 & int.from_byte(number, byteorder='big') == 1: #us left
              motor1.forwards(80)
              motor2.backwards(80)
          else:
              motor1.forwards(40)
              motor2.forwards(40)
    except:
        motor1.stop()
        motor2.stop()
        while True :
             GPIO.output(buzzer, GPIO.HIGH)
             sleep(2)
             GPIO.output(buzzer, GPIO.LOW)
             sleep(0.5)
        print ('robot blocked')
    return 'true'


@app.route('/manual_navigation')
def manual():
   data = "OFF"
   motor1.stop()
   motor2.stop()
   return 'true'

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
