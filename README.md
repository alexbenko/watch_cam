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
<p>My docker-compose file is at: https://github.com/alexbenko/watch_cam/blob/main/watch_cam/docker-compose.yaml</p>

<ol>
  <li><p>First ensure you are running Ubuntu (or at least an arm64 distro) on A Raspberry Pi4</p></li>
  <li><p>Install Docker and Docker-Compose</p></li>
  <li><p>Attatch a USB camera(required) and attatch a speaker (optional)/p></li>
  <li><p>Copy the docker-compose file to wherever you want to run it and change.</p></li>
  <li><p>Type: </p> <code>sudo docker-compose up </code></li>
  <li><p>If everything is set type in your browser: <your pis local IP address>:5000/</p></li>
</ol>
