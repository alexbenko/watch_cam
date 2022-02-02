#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import cv2

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6

class VideoCamera(object):
    def __init__(self):
       self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
      #extracting frames
      ret, frame = self.video.read()
      frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,
      interpolation=cv2.INTER_AREA)
      gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      face_rects=face_cascade.detectMultiScale(gray,1.3,5)
      for (x,y,w,h) in face_rects:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        break
      # encode OpenCV raw frame to jpg and displaying it
      timestamp = datetime.datetime.now()
      cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,255,0), 1)
      ret, jpeg = cv2.imencode('.jpg', frame)
      return jpeg.tobytes()