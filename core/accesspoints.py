# Date: 06/14/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Accesspoint handler

from csv import reader
from subprocess import Popen, call

class Accesspoints(object):
 def __init__(self,essid=None):
  self.green = '\033[92m'
  self.reset = '\033[0m'
  self.essid = essid
  self.red = '\033[91m'
  self.aps = {}
  self.mem = []
  self.map = []
  self.lst = []

 def open(self,csvfile):
  with open(csvfile,'r') as csvfile:
   self.csv = reader(csvfile,delimiter = ',')
   self.organize()
   self.setMap()
   self.display()

 def organize(self):
  for line in self.csv:
   # where router info is displayed
   if len(line) == 15:
    self.updateInfo(line)

   # where clients are displayed
   if len(line) == 7:
    self.setClient(line)

 def setClient(self,data):
  # assign
  bssid = data[5].strip()

  # filter
  if len(bssid) != 17 or not bssid in self.aps:
   return

  # update
  self.aps[bssid]['client'] = True

 def updateInfo(self,data):
  # assign
  bssid = data[0]
  chann = data[3]
  power = data[8]
  essid = data[13]

  # reassign
  power = power.strip()
  chann = chann.strip()
  essid = essid.strip()

  # check for existence
  if not bssid in self.aps:
   self.aps[bssid] = {}
   self.aps[bssid]['client'] = None

  # filter
  if not chann.isdigit() or eval(chann)==-1 or eval(power)==-1:
   del self.aps[bssid]
   return

  # change essid of hidden ap
  essid = essid if not '\\x00' in essid else 'HIDDEN'
  essid = essid if essid else 'UNKNOWN'

  # update
  ap = self.aps[bssid]
  ap['essid'] = essid
  ap['chann'] = chann
  ap['power'] = power

 def sort(self):
  self.mem = self.aps.keys()
  for a,alpha in enumerate(self.mem):
   for b,beta in enumerate(self.mem):
    if a==b:continue

    # set aps
    ap1 = self.aps[alpha]
    ap2 = self.aps[beta]

    # set power levels
    pw1 = ap1['power']
    pw2 = ap2['power']

    # sort
    if a>b and pw1<pw2:
     self.mem[a],self.mem[b]=self.mem[b],self.mem[a]

 def setMap(self):
  if self.aps:
   self.sort()

  if self.mem:
   del self.map[:]

  for num,mac in enumerate(self.mem):
   # assign
   try:
    ap = self.aps[mac]
   except KeyError:return
   power = ap['power']
   essid = ap['essid'] if not self.essid else self.essid if self.essid != mac else ap['essid']
   clnt = '{}*{}'.format(self.green,self.reset) if ap['client'] else '{}-{}'.format(self.red,self.reset)
   num = '{}   '.format(num) if len(str(num)) == 1 else '{}  '.format(num) if len(str(num)) == 2 else '{} '.format(num) if len(str(num)) == 3 else num
   power = ' {} '.format(power) if len(str(power)) == 1 else '{} '.format(power) if len(str(power)) == 2 else power
   power = '{}{}{}'.format(self.green,power,self.reset) if abs(eval(power))<=70 else '{}{}{}'.format(self.red,power,self.reset)
   mac = self.supported(mac)
   # first ouput
   if not eval(num):
    self.map.append('-------------------------------------------------------------')
    self.map.append('|| num  ||\t Bssid\t     ||  Power  || Client || Essid ||')
    self.map.append('-------------------------------------------------------------')
    self.map.append('-------------------------------------------------------------')
   self.map.append('|| {} || {} ||   {}   ||    {}   || {}'.format(num,mac,power,clnt,essid))
   if len(self.mem)-1 == eval(num):
    self.map.append('+-----------------------------------------------------------+')
  self.lst = [display for line in self.map for display in line]

 def display(self):
  if self.lst:
   call(['clear'])
   for line in self.map:
    print line

 def supported(self,bssid):
  out = open('.mac','w')
  mac = bssid[:8].lower()
  Popen('macchanger -l | grep {} | grep -i arris'.format(mac),stdout=out,stderr=out,shell=True).wait()
  with open('.mac','r') as f:
   n = [n for n in f]
   return '{}{}{}'.format(self.green,bssid,self.reset) if n else '{}{}{}'.format(self.red,bssid,self.reset)
