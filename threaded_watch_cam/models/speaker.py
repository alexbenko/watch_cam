import subprocess

class Speaker(object):
  def play(pathToAudio='/audio/test.mp3'):
    subprocess.run(['play', pathToAudio])
