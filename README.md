# About
<p>
  Using OpenCv and Flask I am able to "live stream" a usb camera connected to my Raspberry Pi. Really just continuously grabs the current frame from the camera as an image and updates it on the front end. I am working on a way to save these images and convert them to a video when desired. Currently only the server in the watch_cam folder works on the my Pi and has face detection as well. The threaded_watch_cam works on my MacBook Pro 2019 though and has motion detection.
</p>

<p>I have set up a docker container pushed to Dockerhub. See below on everything you need set up.</p>


<ul>
  <h2>Info About My Pi</h2>
  <li>Model: Raspberry Pi4B</li>
  <li>OS: Ubuntu 20.0.4</li>
  <li>Ram: 4Gb</l1>
  <li>Storage Space: 256 Gb</li>
</ul>

# Usage
<p>First ensure you are running Ubuntu (or at least an arm64 distro) on A Raspberry Pi4, have docker installed, and Have a USB camera attatched.</p>
<code>sudo docker run --device /dev/video0 -p 5000:5000 alexbenko/cam</code>
<p>If you only have 1 usb camera you dont have to change anything, otherwise you need to figure out what the name of the camera is.</p>
