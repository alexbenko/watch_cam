#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response
from models import Sensor,VideoCamera
import math
def bytesto(bytes, to, bsize=1024):
    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    return math.floor(bytes / (bsize ** a[to]))

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('i.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    cpu_temp = Sensor.getCPUtemperature()

    total, used, free = Sensor.getDiskUsage()
    total = bytesto(total,'g')
    used = bytesto(used,'g')
    free = bytesto(free,'g')
    diskUsage = {"total":total, "used": used,"free": free}

    return render_template('status.html',cpu_temp=cpu_temp, diskUsage=diskUsage)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000')

#docker build -t cam:latest .
#docker tag cam alexbenko/cam && docker push alexbenko/cam
#sudo docker run --device /dev/video0 -p 5000:5000 alexbenko/cam