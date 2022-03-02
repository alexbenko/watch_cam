# About
<p>
  Using OpenCv and Flask I am able to "live stream" a usb camera connected to my Raspberry Pi. Really just continuously grabs the current frame from the camera as an image and updates it on the front end. I am working on a way to save these images and convert them to a video when desired. There are also features to play audio through a speaker. Currently has two detection modes, face detection and motion detection.
</p>

</br>

<p>It has an estimated detection range of around 70-100 feet. I am almost postive this is due to my low quality USB camera and once I get one that can record in 1080 the range will be a lot farther.</p>

<ul>
  <h2>Info About My Pi</h2>
  <li>Model: Raspberry Pi4B</li>
  <li>OS: Ubuntu 20.0.4</li>
  <li>Ram: 4Gb</l1>
  <li>Storage Space: 256 Gb</li>
</ul>

# Major To Do's
<ol>
  <li>Optimize image saving - Right now it saves all image as fast as possible which is equal to (camera_framerate * seconds). Which is way too much and causes my pi to lag after 10secs of detection. Work on only saving an image a second</li>
  <li>Camera always on mode - currently camera only turns on when a user goes to the webpage. (mainly till i can do testing)</li>
  <li>Support for Pi's native camera module as well as USB cameras. (I only have a USB camera right now)</li>
</ol>

# Usage
<p>My docker-compose file is  <a target="_blank" rel="noopener noreferrer" href="https://github.com/alexbenko/watch_cam/blob/main/watch_cam/docker-compose.yaml">Here</a></p>

<ol>
  <li><p>First ensure you are running Ubuntu (or at least an arm64 distro) on A Raspberry Pi4</p></li>
  <li><p>Install Docker and Docker-Compose</p></li>
  <li><p>Attatch a USB camera(required) and attatch a speaker (optional)</p></li>
  <li><p>Copy the docker-compose file to wherever you want to run it and change any environment variables, etc.</p></li>
  <li><p>Look at my compose file for reference, create a .env (look bellow for all that you can set) file in the same directory as your docker-compose file.</p></li>
  <li><p>Type: </p> <code>sudo docker-compose up </code></li>
  <li><p>If everything is set type in your browser: [your pis local IP address]:[your specified port env]/</p></li>
  <li><p>If you want to play audio, put desired .mp3 files into the /recordings in the same directory as your compose file and buttons will appear in either detector.</p></li>
</ol>
<br></br>

<p>If everything is set up correctly, you should see this web-page</p>
<img src="https://github.com/alexbenko/watch_cam/blob/main/gh/index.png"></img>

<p>Demo of Motion Detector</p>

https://user-images.githubusercontent.com/37863173/153511768-f405b4e0-3528-4df7-9e3c-1343e66033fa.mp4



# Enviornment Variables to set
<p>There are a good amount of environment variables to set. Some arent that private and can be set in your compose file but others are more should be hidden in a .env file if it will be in a public </p>
<br></br>
<p>To set a boolean env true, the value can be True, T, or 1. Any other value will be false and if it is not set, all booleans default to false</p>
<ul>
  <li><code>app_title</code> - String - The name of the app displayed in the tab and various webpages. Defaults to 'Cam'. (optional)</li>
  <li><code>save_images</code> -  Boolean- Whether or not the server will save the images it detects motion/faces in. (optional)</li>
  <li><code>local_access_only</code> -  Boolean- Whether or not the server will accept requests from external IPs. Only necessary if the server is publicly accessible. (optional)</li>
</ul>
<p>The next variables should be hidden from public view. Right now no user/password set up</p>
<ul>
  <li><code>MONGODB_DATABASEe</code> - String - Name of your mongodb database.</li>
  <li><code>MONGODB_HOSTNAME</code> - String - Name of your mongodb host for the connection string.</li>
  <li><code>EMAIL</code> - String - Email you want to use to forward texts if you desire. Currently only works with Gmail (optional).</li>
  <li><code>EMAIL_PASSWORD</code> - String - Password for your email account (required if you set EMAIL).</li>
  <li><code>PHONE_NUMBER</code> - String - The phone number you want texts to be forwarded to. (required if you set EMAIL and EMAIL_PASSWORD)</li>
  <li><code>CARRIER</code> - String - Name of your carrier. Currently only works with Verizon and AT&T. Valid options are 'att' or 'verizon' (required if you set EMAIL, EMAIL_PASSWORD, and PHONE_NUMBER)</li>
  <li><code>PYTHONUNBUFFERED</code> 0 or 1 - After the initial start up prints, all other prints in the app are ignored. Set this to 1 if you still want to see prints.</li>
</ul>

<p>Currently the only collection is of banned ips. To seed this collection, create a a file called <code>ips.json</code></p>
<p>Put this file in a folder called data and put the folder in the same directory as your compose file.</p>
<p>The json file should be in the format:</p>
</br>
<code>
[
  {"ip": "[the ip you want banned]"},
  ...
]
</code>
<p>The server will use this file to seed the banned ip collection if that collection is empty on startup.</p>
