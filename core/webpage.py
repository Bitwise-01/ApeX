# Date: 07/04/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Password validator

import os
import time
import subprocess

class Webpage(object):
 def __init__(self):
  self.page = None
  self.load = None
  self.output = None
  self.capture = None
  self.passlist = None
  self.passphrase = None

 def setConfig(self):
  self.page = '/tmp/ApeX/site/index.html'
  self.load = '/tmp/ApeX/site/load.html'
  self.output = '/tmp/ApeX/.output'
  self.capture = '/tmp/ApeX/handshake.cap'
  self.passlist = '/tmp/ApeX/site/php/pass.lst'

 def aircrack(self):
  with open(self.output,'w') as output:
   cmd = ['aircrack-ng','-w',self.passlist,self.capture]
   subprocess.Popen(cmd,stdout=output).wait()

 def readOutput(self):
  with open(self.output,'r') as aircrackOutput:
   passphrase = [line.split()[3] for line in aircrackOutput if 'KEY FOUND' in line]
   self.passphrase = passphrase if not self.passphrase else self.passphrase

 def createIndex(self):
  if not self.passphrase:return
  with open(self.page,'w') as writeHtml:
   for line in open(self.load,'r'):
    writeHtml.write(line)

 def runServer(self):
  if os.path.exists(self.passlist):
   self.aircrack()
   self.readOutput()
   self.createIndex()
   os.remove(self.passlist)
