#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response,request,abort,jsonify,send_from_directory
from models import Sensor,VideoCamera,Speaker
import math
from dotenv import load_dotenv
import os

app_title = os.getenv('app_title') or 'Cam'

def bytesto(bytes, to, bsize=1024):
  a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
  r = float(bytes)
  return math.floor(bytes / (bsize ** a[to]))

def face_detection(camera):
    while True:
      frame = camera.detect_human_faces()
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def motion_detection(camera):
  while True:
    frame = camera.detect_motion()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


app = Flask(__name__,static_url_path='/static')

@app.route('/')
def index():
  return render_template('index.html', app_title=app_title)

@app.route('/cam/<mode>')
def cam(mode):
  audio_files = []#[file for file in os.listdir('/audio') if file.endswith(".mp3")]
  if mode == 'face':
    return render_template('cam.html', app_title=app_title, stream_url='face_feed', audio_files=audio_files)
  elif mode == 'motion':
    return render_template('cam.html', app_title=app_title, stream_url='motion_feed',audio_files=audio_files)
  else:
    return '<img src="https://http.cat/400"></img>'

@app.route('/face_feed')
def video_feed():
  return Response(face_detection(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/motion_feed")
def motion_feed():
  return Response(motion_detection(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
  cpu_temp = Sensor.getCPUtemperature()
  total, used, free = Sensor.getDiskUsage()

  diskUsage = {"total":bytesto(total,'g'), "used": bytesto(used,'g'),"free": bytesto(free,'g')}
  return render_template('status.html',cpu_temp=cpu_temp, diskUsage=diskUsage)

@app.route('/play/<file>', methods = ['GET','POST'])
def play(file):
  try:
    Speaker.play(f'/audio/{file}')
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp
  except:
    resp = jsonify(success=False)
    resp.status_code = 400
    return resp

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == '__main__':
  load_dotenv()
  app.run(host='0.0.0.0',port='5000')

#docker build -t cam:latest .
#docker tag cam alexbenko/cam && docker push alexbenko/cam
#sudo docker run --device /dev/video0 --device /dev/snd -p 5000:5000 alexbenko/cam