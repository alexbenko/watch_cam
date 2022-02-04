#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import cv2
import os
import time

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
class VideoCamera(object):
    images_folder_path= './recordings'
    save_images = False
    def __init__(self):
       self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    def save_image(self, image):
      todays_date = datetime.date.today()
      todays_folder = f'{self.images_folder_path}/{todays_date}'

      if(not os.path.isdir(todays_folder)): #if todays folder doesnt exist
        os.makedirs(todays_folder,exist_ok = True) #create it

      rn = int(time.time()) # simplest way to generate unique name for each frame
      cv2.imwrite(f'{todays_folder}/{rn}.png', image)
    def createVideo(self, date):
      #date is expected to be in: yyyy-mm-dd ie datetime.date.today()
      image_folder = f'{self.images_folder_path}/{date}'
      video_name = f'{self.images_folder_path}/{date}/{date}.avi'

      images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
      frame = cv2.imread(os.path.join(image_folder, images[0]))
      height, width, layers = frame.shape

      video = cv2.VideoWriter(video_name, 0, 1, (width,height))

      for image in images:
          video.write(cv2.imread(os.path.join(image_folder, image)))

      cv2.destroyAllWindows()
      video.release()
    def detect_human_faces(self):
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

      if self.save_images:
        self.save_image(frame)

      return jpeg.tobytes()

    def detect_motion(self,baseline_image=None):
      ret, frame = self.video.read()
      frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)

      gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      gray_frame=cv2.GaussianBlur(gray_frame,(25,25),0)

      if baseline_image is None:
        #this means it needs to grab first image
        baseline_image=gray_frame
        return baseline_image

      delta=cv2.absdiff(baseline_image,gray_frame)
      threshold=cv2.threshold(delta,35,255, cv2.THRESH_BINARY)[1]
      (contours,_)=cv2.findContours(threshold,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

      for contour in contours:
        if cv2.contourArea(contour) < 3000:
          continue
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)

      timestamp = datetime.datetime.now()
      cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,255,0), 1)
      # encode OpenCV raw frame to jpg and displaying it
      ret, jpeg = cv2.imencode('.jpg', frame)

      if self.save_images:
        self.save_image(frame)

      return jpeg.tobytes()


