# About
<p>
  Using OpenCv and Flask I am able to "live stream" a usb camera connected to my Raspberry Pi. Really just continuously grabs the current frame from the camera as an image and updates it on the front end. I am working on a way to save these images and convert them to a video when desired. There are also features to play audio through a speaker. 
</p>


<ul>
  <h2>Info About My Pi</h2>
  <li>Model: Raspberry Pi4B</li>
  <li>OS: Ubuntu 20.0.4</li>
  <li>Ram: 4Gb</l1>
  <li>Storage Space: 256 Gb</li>
</ul>

# Usage
<p>First ensure you are running Ubuntu (or at least an arm64 distro) on A Raspberry Pi4, have docker and docker-compose installed, have a USB camera attatched, and a speaker if you want to play audio. I set up a docker-compose file since it was getting complex enough that my docker run command was getting really long. Copy and paste my compose file and change anything specific to your needs. You can find it at https://github.com/alexbenko/watch_cam/blob/main/watch_cam/docker-compose.yaml</p>

