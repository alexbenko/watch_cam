import psutil
from gpiozero import CPUTemperature

class Monitor(object):
  def getCPUtemperature():
    cpu = CPUTemperature()
    return cpu.temperature
