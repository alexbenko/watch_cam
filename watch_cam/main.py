#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response,request,abort,jsonify,request,send_file
from models import Sensor,VideoCamera,Speaker, Database
import math
from dotenv import load_dotenv
import os
from funcs import sms
import datetime
app_title = os.getenv('app_title', 'Cam')

error_responses = {
  "400": '<img src="https://http.cat/400"></img>',
  "404": '<img src="https://http.cat/404"></img>'
}

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

CAMERA = VideoCamera()
app = Flask(__name__,static_url_path='/static')

@app.before_request
def check_if_ip_banned():
  ip = request.remote_addr
  mongo = Database()
  matching_ip = mongo.get_one("ips", {"ip": ip})

  if matching_ip is None:
    return
  else:
    sms.send("Attempt from banned ip address " + str(ip))
    return error_responses["400"], 400

@app.before_request
def local_only():
  local_access_only = os.getenv("local_access_only", "False").lower() in ('true', '1', 't')
  ip = request.remote_addr

  if local_access_only and (ip == '127.0.0.1' or ip.split(".")[0] == "10"):
    return
  elif not local_access_only:
    return
  else:
    return error_responses["400"], 400

@app.route('/')
def index():
  cpu_temp = Sensor.getCPUtemperature()
  total, used, free = Sensor.getDiskUsage()

  diskUsage = {"total":bytesto(total,'g'), "used": bytesto(used,'g'),"free": bytesto(free,'g')}
  return render_template('index.html', app_title=app_title,cpu_temp=cpu_temp, diskUsage=diskUsage)

@app.route('/videos')
def list_videos():
  days = [day for day in os.listdir('./recordings')]
  daysWithPictures = []
  for day in days:
    count = len([pic for pic in os.listdir(f'./recordings/{day}') if pic.endswith(".png") ])
    daysWithPictures.append({"name": day, "count": count})
  existing_videos = [vid for vid in os.listdir('./static') if vid.endswith(".avi")]
  return render_template('download_video.html', daysWithPictures=daysWithPictures, app_title=app_title, existing_videos=existing_videos)

@app.route('/recordings/<path:file>')
def download_video(file):
  path = file.split("/")[1].split(".")[0]
  video = CAMERA.createVideo(path)
  return send_file(video)

@app.route('/cam/<mode>')
def cam(mode):
  audio_files = [file for file in os.listdir('./audio') if file.endswith(".mp3")]
  if mode == 'face':
    return render_template('cam.html', app_title=app_title, stream_url='face_feed', audio_files=audio_files)
  elif mode == 'motion':
    return render_template('cam.html', app_title=app_title, stream_url='motion_feed',audio_files=audio_files)
  else:
    return error_responses["404"], 404

@app.route('/face_feed')
def video_feed():
  return Response(face_detection(CAMERA),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/motion_feed")
def motion_feed():
  return Response(motion_detection(CAMERA),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/play/<file>', methods = ['POST'])
def play(file):
  try:
    Speaker.play(f'/audio/{file}')
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp
  except:
    return abort(404),404

# just a honeypot. /admin is one of the most commons endpoints bots will try to access. easy way to get them all banned
@app.route('/admin')
def ban():
  ip = request.remote_addr
  mongo = Database()
  mongo.ban_ip(ip)
  return error_responses["400"], 400

if __name__ == '__main__':
  load_dotenv()
  print("Checking if seed is necesary ...")
  mongo = Database()
  mongo.seed_ips()
  local_access_only = os.getenv("local_access_only", "False").lower() in ('true', '1', 't')
  save_images = os.getenv("save_images", "False").lower() in ('true', '1', 't')

  print(f'Only local access: {local_access_only}')
  print(f'Save images: {save_images}')

  timestamp = datetime.datetime.now()
  sms.send(f"Server started at {timestamp}")
  app.run(host='0.0.0.0',port='5000')

#docker build -t cam:latest .
#docker tag cam alexbenko/cam && docker push alexbenko/cam