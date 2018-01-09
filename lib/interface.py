from commands import getoutput as shell
from lib.mac import Generator as macchanger

class Interface(object):

 def get_ifaces(self):
  return shell('airmon-ng')

 def remove_iface(self, iface):
  shell('iw dev {} del'.format(iface))

 def create_iface(self, iface, output_iface, mac=None):
  if output_iface in self.get_ifaces():self.remove_iface(output_iface)
  shell('iw {} interface add {} type monitor'.format(iface, output_iface))
  self.spoof_mac(output_iface, mac)

 def spoof_mac(self, iface, custom):
  mac = macchanger().generate() if not custom else custom
  if not custom:
   if mac.lower() in shell('ifconfig'):self.spoof_mac(iface, custom)

  shell('macchanger -m {} {}'.format(mac, iface))
  shell('ifconfig {} up'.format(iface))
