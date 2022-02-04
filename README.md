# About
<p>
  Using OpenCv and Flask I am able to "live stream" a usb camera connected to my Raspberry Pi. Currently only the server in the face_detection folder works on the my Pi. The threaded_face_detection works on my MacBook Pro 2019 though.
</p>

<p>I have set up a docker container pushed to Dockerhub. See bellow on everything you need set up.</p>


<ul>
  <h2>Info About My Pi</h2>
  <li>Model: Raspberry Pi4B</li>
  <li>OS: Ubuntu 20.0.4</li>
  <li>Ram: 4Gb</l1>
  <li>Storage Space: 256 Gb</li>
</ul>

# Usage
<p>First ensure you are running Ubuntu on A Raspberry Pi4, have docker installed, and Have a USB camera attatched.</p>
<code>sudo docker run --device /dev/video0 -p 5000:5000 alexbenko/cam</code>
<p>If you only have 1 usb camera you dont have to change anything, otherwise you need to figure out what the name of the camera is.</p>
