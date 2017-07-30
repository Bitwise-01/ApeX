# Date: 07/29/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Installs requirements

import os
import time
import threading
import subprocess

class Engine(object):
 def __init__(self):
  self.output = '.out'
  self.devnull = open(os.devnull,'w')
  self.required = []
  self.software = ['isc-dhcp-server','python-scapy','aircrack-ng','net-tools',
                   'lighttpd','hostapd','php7.0-cgi','macchanger','wireless-tools']

 def findRequired(self):
  for software in self.software:
   with open(self.output,'w') as output:
    cmd = ['apt-cache','policy',software]
    subprocess.Popen(cmd,stdout=output,stderr=output).wait()
   if not self.readOutput():
    self.required.append(software)

 def readOutput(self):
  with open(self.output,'r') as f:
   n = [n for n in f]
   return False if n[1][14:-2] == 'none' else True

 def aptExists(self):
  if not os.path.exists('/usr/bin/apt'):
   exit('Please install: apt')

 def confirm(self):
  del self.required[:]
  self.findRequired()
  if len(self.required):
   subprocess.call(['clear'])
   for software in self.required:
    print 'Failed to install: {}'.format(software.title())

 def install(self):
  self.aptExists()
  self.findRequired()
  for software in self.required:
   self.loading(software)
   self.fetch(software)
  self.confirm()

 def fetch(self,software):
  cmd = ['apt-get','install',software,'-y']
  subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull).wait()

 def loading(self,software):
  subprocess.call(['clear'])
  print 'Installing: {}'.format(software.title())

if __name__ == '__main__':
 if os.getuid():exit('root access required')
 engine = Engine()
 try:
  engine.install()
  if not engine.required:
   subprocess.call(['clear'])
   print 'requirements found'
 finally:
  os.remove(engine.output)
