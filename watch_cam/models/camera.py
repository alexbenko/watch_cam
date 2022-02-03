#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import cv2
import os
import time

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
save_images = False

class VideoCamera(object):
    def __init__(self):
       self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    def save_image(self, image):
      folderPath= './images'
      todays_date = datetime.date.today()
      todays_folder = f'{folderPath}/{todays_date}'

      if(not os.path.isdir(todays_folder)): #if todays folder doesnt exist
        os.makedirs(todays_folder,exist_ok = True) #create it

      rn = int(time.time()) # simplest way to generate unique name for each frame
      cv2.imwrite(f'{todays_folder}/{rn}.png', image)

    def get_frame(self):
      #extracting frames
      ret, frame = self.video.read()
      frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)

      gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      face_rects=face_cascade.detectMultiScale(gray,1.3,5)
      face_detected = len(face_rects) == 1

      for (x,y,w,h) in face_rects:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        break
      timestamp = datetime.datetime.now()
      cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,255,0), 1)
      # encode OpenCV raw frame to jpg and displaying it
      ret, jpeg = cv2.imencode('.jpg', frame)

      if save_images:
        self.save_image(frame)

      return jpeg.tobytes()