# Demo of Motion Detector

https://user-images.githubusercontent.com/37863173/153511768-f405b4e0-3528-4df7-9e3c-1343e66033fa.mp4
# About
<p>
  Using OpenCv and Flask I am able to "live stream" a usb camera connected to my Raspberry Pi. Really just continuously grabs the current frame from the camera as an image and updates it on the front end. There are also features to play audio through a speaker. 
</p>

</br>

<p>It has an estimated detection range of around 70-100 feet. I am almost postive this is due to my low quality USB camera and once I get one that can record in 1080 the range will be a lot farther.</p>

<p>There are 2 different versions of this as I developed this in my free time. </p>

<p>Version 1.0 is the watch_cam folder. This was practice as I learned how to use OpenCV and I do not recommend using.</p>

<p> Uses multiple threads. The main one is the flask server, which grabs the current frame global variable (which is the current frame loaded into memory) and continuoulsy updates the front end. The second thread is setting the globabl current frame variable from the camera, running the motion detection logic, setting a globabl boolean if it detects motion, and saves frames of detected motion to folders sorted by todays date . The final, optional, thread is a timer thread that is created every 7 seconds after the previous one is done. This thread checks the global motion detected variable, and will upload all frames of detected motion for today to the google drive if the boolean is true. Since all the camera and motion detection logic is in its own thread, supports multiple connected clients. Probably wont work well with more than 3.</p>

<ul>
  <h2>Info About My Pi</h2>
  <li>Model: Raspberry Pi4B</li>
  <li>OS: Debian GNU/Linux 11 (Bullseye)</li>
  <li>Ram: 4Gb</l1>
  <li>Storage Space: 256 Gb</li>
</ul>

# Major To Do's
<ol>
  <li><strike>Camera always on mode - currently camera only turns on when a user goes to the webpage. (mainly till i can do testing) </strike></li>
  <li><strike>Move image/video saving,getting,creating logic out of Camera model into their own (For watch_cam)</strike></li>
  <li>Optimize uploading to google drive. Worked perfectly for about 2 days, but then stopped uploading for an unknown reason.(For threaded watch cam</li>
  <li>Support other cloud storage tech, like AWS' S3.</li>
  <li>Notification system for user to be notified on motion.</li>
  <li><strike>Working docker-compose file for threaded_watch_cam</strike></li>
  <li>Only upload new frames of motion. Currently just grabs todays folder and uploads it to my google drive without any logic to verify if the file has already been uploaded.</li>
</ol>

<ol>
  <li><p>First ensure you are running Raspberry Pi OS (or at least an arm64 distro) on A Raspberry Pi4 since the docker image is built off of  <code>arm64v8/debian:bullseye</code>.</p></li>
  <li><p>Install Docker and Docker-Compose</p></li>
  <li><p>Attatch a USB camera(required) and attatch a speaker (optional)</p></li>
  <li><p>Copy the docker-compose file to wherever you want to run it and change any environment variables in a .env file.</p></li>
  <li><p>Look at my compose file for reference, create a .env (look bellow for all that you can set) file in the same directory as your docker-compose file.</p></li>
  <li><p>Type: </p> <code>sudo docker-compose up </code></li>
  <li><p>If everything is set type in your browser: [your pis local IP address]:[your specified port env]/</p></li>
  <li><p>If you want to play audio, put desired .mp3 files into the /recordings in the same directory as your compose file and buttons will appear in either detector.</p></li>
</ol>
<br></br>

# Enviornment Variables to set
<p>There are a good amount of environment variables to set. Some arent that private and can be set in your compose file but others are more should be hidden in a .env file if it will be in a public </p>
<br></br>
<p>To set a boolean env true, the value can be True, T, or 1. Any other value will be false and if it is not set, all booleans default to false</p>
<ul>
  <li><code>app_title</code> - String - The name of the app displayed in the tab and various webpages. Defaults to 'Cam'. (optional)</li>
  <li><code>save_images</code> -  Boolean- Whether or not the server will save the images it detects motion/faces in. (optional)</li>
  <li><code>local_access_only</code> -  Boolean- Whether or not the server will accept requests from external IPs. Only necessary if the server is publicly accessible. (optional)</li>
  <li><code>PORT</code> - The port you want the flask server to run on, defaults to 5000</li>
</ul>
<p>The next variables should be hidden from public view. Right now no user/password set up</p>
<ul>
  <li><code>EMAIL</code> - String - Email you want to use to forward texts if you desire. Currently only works with Gmail (optional).</li>
  <li><code>EMAIL_PASSWORD</code> - String - Password for your email account (required if you set EMAIL).</li>
  <li><code>PHONE_NUMBER</code> - String - The phone number you want texts to be forwarded to. (required if you set EMAIL and EMAIL_PASSWORD)</li>
  <li><code>CARRIER</code> - String - Name of your carrier. Currently only works with Verizon and AT&T. Valid options are 'att' or 'verizon' (required if you set EMAIL, EMAIL_PASSWORD, and PHONE_NUMBER)</li>
  <li><code>PYTHONUNBUFFERED</code> 0 or 1 - After the initial start up prints, all other prints in the app are ignored. Set this to 1 if you still want to see prints.</li>
</ul>
