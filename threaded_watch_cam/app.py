#!/usr/bin/python
# -*- coding: utf-8 -*-
from models import SingleMotionDetector, G_Drive, RepeatedTimer
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import os
import uuid
from pathlib import Path
import atexit

RECORDINGS_FOLDER_ID = "1VJvjQRTzpDSehsjNAYjSlUc5tbgCEviB"

def save_image(image):
  todays_date = str(datetime.date.today())
  todays_folder = f'/recordings/{todays_date}'

  path = Path('..','recordings', todays_date)
  path.mkdir(parents=True, exist_ok=True)

  rn = str(time.time()) # simplest way to generate unique name for each frame
  name = uuid.uuid4().hex + rn

  cv2.imwrite(f'{path}/{name}.png', image)

outputFrame = None
lock = threading.Lock()
motion_detected = False
# initialize a flask object
app = Flask(__name__,static_url_path='/static')

#im deploying this on a pi but using a normal usb camera, if i ever use the RPi camera module, i would use this line instead
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0) #let camera start up

@app.route('/videos')
def list_videos():
  days = [day for day in os.listdir('../recordings')]
  daysWithPictures = []
  for day in days:
    count = len([pic for pic in os.listdir(f'../recordings/{day}') if pic.endswith(".png") ])
    daysWithPictures.append({"name": day, "count": count})
  existing_videos = [vid for vid in os.listdir('./static') if vid.endswith(".avi")]
  return render_template('download_video.html', daysWithPictures=daysWithPictures, app_title=app_title, existing_videos=existing_videos)

@app.route('/recordings/<path:file>')
def download_video(file):
  path = file.split("/")[1].split(".")[0]
  image_folder = f'{images_folder_path}/{path}'
  video_path = os.path.join('static', f'{path}.avi')
  images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
  frame = cv2.imread(os.path.join(image_folder, images[0]))
  height, width, layers = frame.shape
  video = cv2.VideoWriter(video_path, 0, 1, (width,height))
  for image in images:
      video.write(cv2.imread(os.path.join(image_folder, image)))
  time.sleep(0.15) #give the pi some time to save the video to prevent accidental 404s
  return send_file(video_path)

@app.route("/video_feed")
def video_feed():
  # return the response generated along with the specific media
  # type (mime type)
  return Response(generate(),
    mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/cam')
def cam():
  return render_template("cam.html")

def detect_motion(frameCount):
  # grab global references to the video stream, output frame, and
  # lock variables
  global vs, outputFrame, lock, motion_detected
  # initialize the motion detector and the total number of frames
  # read thus far
  md = SingleMotionDetector(accumWeight=0.1)
  total = 0
    # loop over frames from the video stream
  while True:
    # read the next frame from the video stream, resize it,
    # convert the frame to grayscale, and blur it
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    # grab the current timestamp and draw it on the frame
    timestamp = datetime.datetime.now()
    cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # if the total number of frames has reached a sufficient
    # number to construct a reasonable background model, then
    # continue to process the frame
    if total > frameCount:
      # detect motion in the image
      motion = md.detect(gray)
      # check to see if motion was found in the frame
      if motion is not None:
        motion_detected = True
        # unpack the tuple and draw the box surrounding the
        # "motion area" on the output frame
        (thresh, (minX, minY, maxX, maxY)) = motion
        cv2.rectangle(frame, (minX, minY), (maxX, maxY), (0, 0, 255), 2)
      else:
        motion_detected = False


    # update the background model and increment the total number
    # of frames read thus far
    md.update(gray)
    total += 1

    # acquire the lock, set the output frame, and release the
    # lock
    with lock:
      frame_copy = frame.copy()
      outputFrame = frame_copy
      if motion_detected:
        save_image(frame_copy)


def generate():
  global outputFrame, lock, motion_detected
  while True:
    # wait until the lock is acquired
    with lock:
      if outputFrame is None:
        print('no outputFrame')
        continue

      (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
      if not flag:
        print('no flag')
        continue
    # yield the output frame in the byte format
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
      bytearray(encodedImage) + b'\r\n')

def OnServerClose(timer):
  timer.stop()

def backup_recordings_if_motion():
  global motion_detected
  if motion_detected:
    print("MOTION DETECTED, backing up images")
    g = G_Drive()
    todays_date = str(datetime.date.today())
    folder_path = Path("..", "recordings", todays_date)
    todays_id = g.get_folder_id(RECORDINGS_FOLDER_ID, todays_date)
    if todays_id == None:
      todays_id = g.create_folder(RECORDINGS_FOLDER_ID, todays_date)
    g.back_up_recordings(todays_id,folder_path)

if __name__ == '__main__':
  SAVE_TIMER = 7
  ap = argparse.ArgumentParser()

  ap.add_argument("-f", "--frame-count", type=int, default=32,help="# of frames used to construct the background model")
  args = vars(ap.parse_args())

  # start a thread that will perform motion detection
  t = threading.Thread(target=detect_motion, args=(
    args["frame_count"],))
  t.daemon = True
  t.start()

  #start a timer thread that will check if there is motion every 10 secs and upload to my google drive if there is
  print(f'Checking for motion every {SAVE_TIMER} seconds')
  timer_thread = RepeatedTimer(int(SAVE_TIMER), backup_recordings_if_motion) #starts automatically
  atexit.register(OnServerClose, timer=timer_thread)
  app.run(host='0.0.0.0', port=4269,threaded=True, use_reloader=False)

vs.stop()

#this are just my docker commands so i dont have to memorize them
#docker build -t threaded_cam:latest .
#docker tag threaded_cam alexbenko/threaded_cam && docker push alexbenko/threaded_cam
#sudo docker run -p 5000:5000 --device /dev/video0 alexbenko/threaded_cam:latest