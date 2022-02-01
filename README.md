# About
<p>
  Using OpenCv and Flask I am able to "live stream" a usb camera connected to my Raspberry Pi. Currently only the server in the face_detection folder works on the my Pi. The threaded_face_detection works on my MacBook Pro 2019 though.
</p>


<ul>
  <h2>Info About My Pi</h2>
  <li>Model: Raspberry Pi4B</li>
  <li>OS: Ubuntu 20.0.4</li>
  <li>Ram: 4Gb</l1>
  <li>Storage Space: 256 Gb</li>
</ul>

#Usage
First ensure you are running Ubuntu on A Raspberry Pi4.
<code>sudo docker run --device /dev/video0 -p 5000:5000 alexbenko/cam</code>
