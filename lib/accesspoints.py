from time import sleep
from csv import reader
from os.path import exists
from subprocess import call
from lib.settings import COLORS, DISTANCE, SCAN_OUPUT

class Accesspoints(object):
 def __init__(self, essid=None):
  self.mem = []
  self.map = []
  self.aps = {}

  self.essid = essid
  self.is_alive = False
  self.csv_file = '{}-01.csv'.format(SCAN_OUPUT)

 def start(self):
  while self.is_alive:

   if not exists(self.csv_file):continue
   with open(self.csv_file, 'r') as csvfile:
    self.organize(reader(csvfile,delimiter = ','))
    self.setMap()
    self.display()

 def organize(self, csv):
  for line in csv:

   # where router info is displayed
   if len(line) == 15:
    self.updateInfo(line)

   # where clients are displayed
   if len(line) == 7:
    self.setClient(line)

 def setClient(self, data):
  # assign
  bssid = data[5].strip()

  # filter
  if any([len(bssid) != 17, not bssid in self.aps]):
   return

  # update
  self.aps[bssid]['client'] = True

 def updateInfo(self, data):
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
   self.aps[bssid]['bssid'] = bssid
   self.aps[bssid]['client'] = False

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
  ap['power'] = abs(int(power))

 def sort(self):
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
     self.mem[a], self.mem[b] = self.mem[b], self.mem[a]

 def power(self, power):
  return '-{}{}{}'.format(COLORS['green'] if power <= DISTANCE['MIN'] else
                         COLORS['yellow'] if all([power > DISTANCE['MIN'],
                                                  power < DISTANCE['MAX']]) else
                         COLORS['red'], power, COLORS['white']) if power else ' {}{}{} '.\
                         format(COLORS['green'], power, COLORS['white'])

 def clients(self, client):
  return '{}{}{}'.format(COLORS['green'] if client else COLORS['red'],
                         '!' if client else '-', COLORS['white'])

 def num(self, num):
  n = num%2
  num = '{:03}'.format(num)
  return '{}{}{}'.format(COLORS['red'] if not n else COLORS['blue'],
                         num, COLORS['white'])

 def mac(self, num, mac):
  return '{}{}{}'.format(COLORS['red'] if not num%2 else COLORS['blue'], mac, COLORS['white'])

 def setMap(self):
  if self.aps:
   self.mem = self.aps.keys()
   self.sort()

  if self.mem:
   del self.map[:]

  for n, mac in enumerate(self.mem):
   if not self.is_alive:break

   # assign
   try:
    ap = self.aps[mac]
   except KeyError:continue
   essid = ap['essid']

   num = self.num(n)
   mac = self.mac(n, mac)
   power = self.power(ap['power'])
   clnt = self.clients(ap['client'])

   # first ouput
   if not n:
    self.map.append('-'*61)
    self.map.append('|| {}NUM{} ||\tBSSID\t    ||  POWER  ||  CLIENT || ESSID ||'.\
     format(COLORS['yellow'], COLORS['white']))

    self.map.append('-'*61)
    self.map.append('+{}+'.format('-'*59))
   self.map.append('|| {} || {} ||   {}   ||    {}    || {}'.\
    format(num,mac,power,clnt,essid))
  if len(self.mem):self.map.append('+{}+'.format('-'*59))

 def display(self):
  if not self.map:
   call(['clear'])
   print '[-] Scanning ...' if not self.essid else '[-] Scanning {} ...'.format(self.essid)
   sleep(0.5)

  for n, display in enumerate(self.map):
   if not n:call(['clear'])
   print display

  if len(self.map) and self.is_alive:
   sleep(1.2)
