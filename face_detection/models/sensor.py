import shutil
from gpiozero import CPUTemperature

class Sensor(object):
  def getCPUtemperature():
    cpu = CPUTemperature()
    return cpu.temperature
  def getDiskUsage():
    return shutil.disk_usage('/')
