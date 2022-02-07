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
<p>First ensure you are running Ubuntu (or at least an arm64 distro) on A Raspberry Pi4, have docker and docker-compose installed, have a USB camera attatched, and a speaker if you want to play audio. I set up a docker-compose file since it was getting complex enough that my docker run command was getting really long. Copy and paste my compose file and change anything specific to your needs. </p>
<code>
  version: "3"
  services:
    app:
      image: alexbenko/cam:latest
      volumes:
        - ./audio:/audio
        - ./recordings:/recordings
      environment:
        app_title: Watch Cam
        PORT: 5000
        save_images: True
      ports:
        - "5000:5000"
      devices:
        - /dev/video0:/dev/video0
        - /dev/snd:/dev/snd
      command: python3 main.py
      restart: unless-stopped
</code>

