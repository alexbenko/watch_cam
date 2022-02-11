# About
<p>
  Using OpenCv and Flask I am able to "live stream" a usb camera connected to my Raspberry Pi. Really just continuously grabs the current frame from the camera as an image and updates it on the front end. I am working on a way to save these images and convert them to a video when desired. There are also features to play audio through a speaker. Currently has two detection modes, face detection and motion detection.
</p>


<ul>
  <h2>Info About My Pi</h2>
  <li>Model: Raspberry Pi4B</li>
  <li>OS: Ubuntu 20.0.4</li>
  <li>Ram: 4Gb</l1>
  <li>Storage Space: 256 Gb</li>
</ul>

# Usage
<p>My docker-compose file is  <a target="_blank" rel="noopener noreferrer" href="https://github.com/alexbenko/watch_cam/blob/main/watch_cam/docker-compose.yaml">Here</a></p>

<ol>
  <li><p>First ensure you are running Ubuntu (or at least an arm64 distro) on A Raspberry Pi4</p></li>
  <li><p>Install Docker and Docker-Compose</p></li>
  <li><p>Attatch a USB camera(required) and attatch a speaker (optional)</p></li>
  <li><p>Copy the docker-compose file to wherever you want to run it and change any environment variables, etc.</p></li>
  <li><p>Look at my compose file for reference, create a .env file in the same directory as your docker-compose file.</p></li>
  <li><p>Type: </p> <code>sudo docker-compose up </code></li>
  <li><p>If everything is set type in your browser: [your pis local IP address]:5000/</p></li>
  <li><p>If you want to play audio, put desired .mp3 files into the /recordings and buttons will appear in either detector.</p></li>
</ol>
<br></br>

<p>If everything is set up correctly, you should see this web-page</p>
<img src="https://github.com/alexbenko/watch_cam/blob/main/gh/index.png"></img>

<p>Demo of Motion Detector</p>

https://user-images.githubusercontent.com/37863173/153511768-f405b4e0-3528-4df7-9e3c-1343e66033fa.mp4



# Enviornment Variables
