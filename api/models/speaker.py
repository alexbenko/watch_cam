import subprocess

class Speaker(object):
  def play(self, path_to_audio='/audio/test.mp3'):
    subprocess.run(['mpg321', path_to_audio, '&'])
