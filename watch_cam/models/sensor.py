import shutil
from gpiozero import CPUTemperature
#WARNING: This code is meant to run on a raspberry pi. ########
class Sensor(object):
  def getCPUtemperature():
    cpu = CPUTemperature()
    return cpu.temperature
  def getDiskUsage():
    return shutil.disk_usage('/')
