# Date: 07/20/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Interface handler

from os import devnull
from subprocess import Popen
from core.mac import Generator as macGen

class Interface(object):
 def __init__(self,iface):
  self.iface = iface
  self.devnull  = open(devnull,'w')
  self.mac = macGen().generate()

 def managedMode(self):
  [self.destroyInterface(mon) for mon in ['mon0','mon1']]
  cmd = 'service network-manager restart'
  Popen(cmd,stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def changeMac(self,iface):
  cmd ='ifconfig {0} down && iwconfig {0} mode monitor &&\
        macchanger -m {1} {0} && service\
        network-manager stop && ifconfig {0} up'.format(iface,self.mac)

  Popen(cmd,stdout=self.devnull,stderr=self.devnull,shell=True).wait()

 def monitorMode(self,iface):
  self.destroyInterface(iface)
  Popen('iw {} interface add {} type monitor'.format(self.wlan,iface),
  stdout=self.devnull,stderr=self.devnull,shell=True).wait()
  self.changeMac(iface)

 def destroyInterface(self,iface):
  Popen('iw dev {} del'.format(iface),stdout=self.devnull,
  stderr=self.devnull,shell=True).wait()
