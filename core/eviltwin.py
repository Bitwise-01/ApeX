# Date: 07/18/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Monitors hostapd output

import time

class MonitorEviltwin(object):
 def __init__(self):
  self._mem = {} # holds initial sessions
  self.devices = {}
  self.clients = []
  self.hostapdOutput = '.hostapd.log'

 def removeDevice(self):
  # devices that aren't connected anymore
  macs = [device for device in self.devices if not self.devices[device]['State']]
  for mac in macs:
   del self.devices[mac]

 def memorize(self,bssid):
  return self._mem[bssid]

 def analyzeOutput(self):
  with open(self.hostapdOutput,'r') as output:
   for line in output:
    # authenticated or unauthenticated
    if len(line.split()) == 6:
     msg = line.split()[-1]
     bssid = line.split()[2]
     self.authenication(bssid,msg)
    # AP-STA-CONNECTED or AP-STA-DISCONNECTED
    if len(line.split()) == 3:
     msg = line.split()[1]
     bssid = line.split()[2]
     self.authenication(bssid,msg)
    # session id
    if len(line.split()) == 8:
     if line.split()[-2] == 'session':
      bssid = line.split()[2]
      if bssid in self._mem:
       session = self.memorize(bssid)
      else:
       session = line.split()[-1]
       self._mem[bssid] = session
      self.devices[bssid]['Session'] = session

 def authenication(self,bssid,msg):
  state = True if any([msg == 'authenticated',msg == 'AP-STA-CONNECTED']) else False
  if not bssid in self.devices:
   self.devices[bssid] = {'Session':None,'State':state,'Time':time.strftime('%I:%M %p',time.localtime())}
  else:
   self.devices[bssid]['State'] = state

 def setOrder(self):
  devices = self.devices.keys()
  for a,device1 in enumerate(devices):
   for b,device2 in enumerate(devices):
    if a==b:continue
    s1 = self.devices[device1]['Session'][9:]
    s2 = self.devices[device2]['Session'][9:]
    if all([a>b,s1<s2]):
     devices[a],devices[b] = devices[b],devices[a]
  return devices

 def organizeInfo(self):
  self.clients = []
  for num,device in enumerate(self.setOrder()):
   bssid = device
   session = self.devices[device]['Session']
   timeConnected = self.devices[device]['Time']
   num = '{}   '.format(num) if len(str(num)) == 1 else '{}  '.format(num) if len(str(num)) == 2 else '{} '.format(num) if len(str(num)) == 3 else num
   if not eval(num):
    self.clients.append('                  +------------------------+')
    self.clients.append('                  ||  Clients  Connected  ||')
    self.clients.append('------------------                          --------------------')
    self.clients.append('|| #    ||\t Bssid\t     ||\t     Session   \t  ||   Time   ||  ')
    self.clients.append('----------------------------------------------------------------')
    self.clients.append('----------------------------------------------------------------')
   self.clients.append('|| {} || {} || {} || {} ||'.format(num,bssid.upper(),session,timeConnected))
   if len(self.devices)-1 == eval(num):
    self.clients.append('+--------------------------------------------------------------+')

 def eviltwinInfo(self):
  self.analyzeOutput()
  self.removeDevice()
  self.organizeInfo()
  return self.clients
