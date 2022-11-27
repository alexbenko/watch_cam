import numpy as np
from pathlib import Path
import imutils, cv2, uuid, datetime, time
class SingleMotionDetector:
  def __init__(self, accum_weight=0.5):
    self.accum_weight = accum_weight

    # initialize the background model
    self.bg = None

  def update(self, image):
    # if the background model is None, initialize it
    if self.bg is None:
      self.bg = image.copy().astype("float")
      return
    # update the background model by accumulating the weighted
    # average
    cv2.accumulateWeighted(image, self.bg, self.accum_weight)

  def detect(self, image, t_val=25):
    # compute the absolute difference between the background model
    # and the image passed in, then threshold the delta image
    delta = cv2.absdiff(self.bg.astype("uint8"), image)
    thresh = cv2.threshold(delta, t_val, 255, cv2.THRESH_BINARY)[1]
    # perform a series of erosions and dilations to remove small
    # blobs
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
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

  def save_image(self, image):
    todays_date = str(datetime.date.today())

    path = Path('..','recordings', todays_date)
    path.mkdir(parents=True, exist_ok=True)

    rn = str(time.time()) # simplest way to generate unique name for each frame
    name = uuid.uuid4().hex + rn

    cv2.imwrite(f'{path}/{name}.png', image)