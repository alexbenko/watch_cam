from fastapi.staticfiles import StaticFiles
from models import SingleMotionDetector, G_Drive, RepeatedTimer, Speaker
from imutils.video import VideoStream
from fastapi import FastAPI
from dotenv import load_dotenv
from threading import Thread, Lock
import os, cv2, argparse, datetime, imutils, time
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse

load_dotenv()
ENVIORNMENT = os.getenv('ENVIORNMENT', 'development')
is_production = ENVIORNMENT == 'production'

outputFrame = None
lock = None
motion_detected = False
conversation = None
vs = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global vs, outputFrame, lock
    #im deploying this on a pi but using a normal usb camera, if i ever use the RPi camera module, i would use this line instead
    #vs = VideoStream(usePiCamera=1).start()
    lock = Lock()
    vs = VideoStream(src=0).start()
    time.sleep(2.0) #let camera start up
    print("Camera initialized")
    thread = Thread(target=detect_motion, daemon=True)
    thread.start()
    print('Motion detection thread started')
    yield

    # Clean up
    vs = vs.stop()
    vs = None
    print("Camera Stopped")

app = FastAPI(lifespan=lifespan)
IMAGES_PATH= '/recordings'
SAVE_IMAGES = os.getenv("save_images", "False").lower() in ('true', '1', 't')

@app.get("/video_feed")
async def video_feed():
  return StreamingResponse(generate(),media_type = "multipart/x-mixed-replace; boundary=frame")

def detect_motion(frame_count=32):
  # grab global references to the video stream, output frame, and lock variables
  global vs, outputFrame, lock, motion_detected

  md = SingleMotionDetector(accum_weight=0.1)
  total = 0
  while True:
    # read the next frame from the video stream, resize it,
    # convert the frame to grayscale, and blur it
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    # grab the current timestamp and draw it on the frame
    timestamp = datetime.datetime.now()
    cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # if the total number of frames has reached a sufficient
    # number to construct a reasonable background model, then
    # continue to process the frame
    if total > frame_count:
      motion = md.detect(gray)
      if motion is not None:
        motion_detected = True
        # draw the box surrounding the "motion area" on the output frame
        (thresh, (min_x, min_y, max_x, max_y)) = motion
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)
      else:
        motion_detected = False

    # update the background model and increment the total number of frames read thus far
    md.update(gray)
    total += 1

    # acquire the lock, set the output frame, and release the lock
    with lock:
      frame_copy = frame.copy()
      outputFrame = frame_copy
      if motion_detected and SAVE_IMAGES:
        # Save images in a separate thread to avoid blocking
        Thread(target=md.save_image, args=(frame_copy,)).start()


def generate():
  global outputFrame, lock
  while True:
    with lock:
      if outputFrame is None:
        print('no outputFrame')
        continue

      (flag, encoded_image) = cv2.imencode(".jpg", outputFrame)
      if not flag:
        print('no flag')
        continue
    # yield the output frame in the byte format
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
      bytearray(encoded_image) + b'\r\n')

# TODO
#@app.route('/videos')
#def list_videos():
#  days = [day for day in os.listdir('./recordings')]
#  days_with_pictures = []
#  for day in days:
#    count = len([pic for pic in os.listdir(f'./recordings/{day}') if pic.endswith(".png") ])
#    days_with_pictures.append({"name": day, "count": count})
#  existing_videos = [vid for vid in os.listdir('./static') if vid.endswith(".avi")]
#  return render_template('download_video.html', daysWithPictures=days_with_pictures, app_title='Watch Cam', existing_videos=existing_videos)
#
#@app.route('/recordings/<path:file>')
#def download_video(file):
#  path = file.split("/")[1].split(".")[0]
#  image_folder = f'{IMAGES_PATH}/{path}'
#  video_path = os.path.join('static', f'{path}.mp4')
#  images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
#  frame = cv2.imread(os.path.join(image_folder, images[0]))
#  height, width, layers = frame.shape
#  video = cv2.VideoWriter(video_path, 0, 1, (width,height))
#  for image in images:
#      video.write(cv2.imread(os.path.join(image_folder, image)))
#  time.sleep(0.15) #give the pi some time to save the video to prevent accidental 404s
#  return send_file(video_path)

#@app.route('/play/<file>', methods = ['POST'])
#def play(file):
#  print('PLAYING SOUND')
#  try:
#    Speaker.play(f'/audio/{file}')
#    resp = jsonify(success=True)
#    resp.status_code = 200
#    return resp
#  except:
#    return abort(404),404


#def backup_recordings_if_motion():
#    g = G_Drive()
#    todays_date = str(datetime.date.today())
#    folder_path = Path("..", "recordings", todays_date)
#    todays_id = g.get_folder_id(RECORDINGS_FOLDER_ID, todays_date)
#    if todays_id == None:
#      todays_id = g.create_folder(RECORDINGS_FOLDER_ID, todays_date)
#    g.back_up_recordings(todays_id,folder_path)

if is_production:
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")

if __name__ == '__main__':
    import uvicorn
    print(f'Starting server in {ENVIORNMENT} mode.')
    print(f'Is production: {is_production}')
    to_run = app if is_production else "main:app"
    uvicorn.run(to_run, host="0.0.0.0", port=os.getenv('PORT', 4269), log_level="debug", reload= not is_production)


#this are just my docker commands so i dont have to memorize them
#docker build -t threaded_cam:latest .
#docker tag threaded_cam alexbenko/threaded_cam && docker push alexbenko/threaded_cam
#sudo docker run -p 5000:5000 --device /dev/video0 alexbenko/threaded_cam:latest