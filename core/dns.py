# Date: 07/07/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Dns Server

class Dns(object):
 def __init__(self):
  self.a = 12
  self.p = None
  self.e = None
  self.x = None

  self.d = None
  self.r = None

  self.ip = '192.168.0.1'
  self.udp = None

 def configDns(self):
  if (ord(self.e[2]) >> 3) & 15:return
  self.a = 12
  self.p = ord(self.e[self.a])
  while self.p:
   self.r = '{}.'.format(self.e[self.a+1:self.a+self.p+1])
   self.d = self.r if not self.d else self.d+self.r
   self.a+=self.p+1
   self.p=ord(self.e[self.a])

 def redirect(self):
  if self.d:
   self.x = '{}\x81\x80'.format(self.e[:2])
   self.x+='{}{}\x00\x00\x00\x00'.format(self.e[4:6],self.e[4:6])
   self.x+=self.e[12:]
   self.x+='\xc0\x0c'
   self.x+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
   self.x+=str.join('',map(lambda x:chr(int(x)), self.ip.split('.')))
   self.udp.sendto(self.x,self.addr)

 def runDns(self):
  self.e,self.addr = self.udp.recvfrom(1024)
  self.configDns()
  self.redirect()
