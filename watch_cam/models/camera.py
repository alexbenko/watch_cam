#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import cv2
import os
import imutils
import numpy as np
import time

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
class VideoCamera(object):
	images_folder_path= '/recordings'
	accumWeight=0.5
	bg = None
	outputFrame = None
	total = 0

	def __init__(self,):
		self.video = cv2.VideoCapture(0)
		self.save_images = os.getenv('save_images', False).lower() in ('true', '1', 't')

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

	def update_background(self, image):
		# if the background model is None, initialize it
		if self.bg is None:
			self.bg = image.copy().astype("float")
			return
		# update the background model by accumulating the weighted
		# average
		cv2.accumulateWeighted(image, self.bg, self.accumWeight)

	def find_motion(self, image, tVal=25):
		delta = cv2.absdiff(self.bg.astype("uint8"), image)
		thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
		# perform a series of erosions and dilations to remove small
		# blobs
		thresh = cv2.erode(thresh, None, iterations=2)
		thresh = cv2.dilate(thresh, None, iterations=2)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		(minX, minY) = (np.inf, np.inf)
		(maxX, maxY) = (-np.inf, -np.inf)

		# if no contours were found, return None
		if len(cnts) == 0:
			return None
		# otherwise, loop over the contours
		for c in cnts:
			# compute the bounding box of the contour and use it to
			# update the minimum and maximum bounding box regions
			(x, y, w, h) = cv2.boundingRect(c)
			(minX, minY) = (min(minX, x), min(minY, y))
			(maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))
		# otherwise, return a tuple of the thresholded image along
		# with bounding box
		return (thresh, (minX, minY, maxX, maxY))

	def detect_motion(self,frameCount=32):
		motion_detected  = False
		#requires use of self.find_motion and self.update_background
		ret, frame = self.video.read()
		frame = imutils.resize(frame, width=400)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)
		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
		# if the total number of frames has reached a sufficient
		# number to construct a reasonable background model, then
		# continue to process the frame
		if self.total > frameCount:
			# detect motion in the image
			motion = self.find_motion(gray)
			# check to see if motion was found in the frame
			if motion is not None:
				motion_detected = True
				# unpack the tuple and draw the box surrounding the
				# "motion area" on the output frame
				(thresh, (minX, minY, maxX, maxY)) = motion
				cv2.rectangle(frame, (minX, minY), (maxX, maxY),(0, 0, 255), 2)

		# update the background model and increment the total number
		# of frames read thus far
		self.update_background(gray)
		self.total += 1
		ret, jpeg = cv2.imencode('.jpg', frame)
		if self.save_images and motion_detected:
			self.save_image(frame)
		return jpeg.tobytes()

