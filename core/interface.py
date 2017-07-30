# Date: 07/20/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Interface handler

import os
import subprocess
from core.mac import Generator as macGen

class Interface(object):
 def __init__(self,iface,bssid=None):
  self.iface = iface
  self.devnull  = open(os.devnull,'w')
  self.macAddress = macGen().generate() if not bssid else bssid

 def managedMode(self):
  subprocess.Popen('ifconfig {} down'.format(self.iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  subprocess.Popen('iwconfig {} mode managed'.format(self.iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  subprocess.Popen('macchanger -p {}'.format(self.iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  subprocess.Popen('ifconfig {} up'.format(self.iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  subprocess.Popen('service network-manager restart',stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  
 def monitorMode(self,iface=None):
  iface = iface if iface else self.iface
  subprocess.Popen('ifconfig {} down'.format(iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  subprocess.Popen('iwconfig {} mode monitor'.format(iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  subprocess.Popen('macchanger -m {} {}'.format(self.macAddress,iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  subprocess.Popen('ifconfig {} up'.format(iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  subprocess.Popen('service network-manager stop',stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def createInterface(self):
  subprocess.Popen('iw {} interface add mon0 type monitor'.format(self.iface),stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  self.monitorMode('mon0')

 def destroyInterface(self):
  subprocess.Popen('iw dev mon0 del',stdout=self.devnull,stderr=self.devnull,shell=True).wait()
