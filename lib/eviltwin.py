import time
from lib.settings import COLORS, EVIL_TWIN_OUTPUT

class MonitorEviltwin(object):
 def __init__(self):
  self.mem = {} # holds initial sessions
  self.devices = {}
  self.clients = []

 def remove_device(self):
  # devices that aren't connected anymore
  macs = [device for device in self.devices if not self.devices[device]['State']]
  for mac in macs:
   del self.devices[mac]

 def memorize(self,bssid):
  return self.mem[bssid]

 def analyze_output(self):
  with open(EVIL_TWIN_OUTPUT, 'r') as output:
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
      if bssid in self.mem:
       session = self.memorize(bssid)
      else:
       session = line.split()[-1]
       self.mem[bssid] = session
      self.devices[bssid]['Session'] = session

 def authenication(self,bssid,msg):
  state = True if any([msg == 'authenticated',msg == 'AP-STA-CONNECTED']) else False
  if not bssid in self.devices:
   self.devices[bssid] = {'Session':None,'State':state,'Time':time.strftime('%I:%M %p',time.localtime())}
  else:
   self.devices[bssid]['State'] = state

 def set_order(self):
  devices = self.devices.keys()
  for a, device1 in enumerate(devices):
   for b, device2 in enumerate(devices):
    if a==b:continue

    if all([a>b, device1<device2]):
     devices[a], devices[b] = devices[b], devices[a]
  return devices

 def organize_info(self):
  self.clients = []
  for num, device in enumerate(self.set_order()):
   bssid = device
   session = self.devices[device]['Session']
   time_connected = self.devices[device]['Time']
   colored = lambda item: '{}{}{}'.format(COLORS['blue'] if num%2 else COLORS['red'], item, COLORS['white'])
   _num =  '{:03}'.format(num)

   if not num:
    self.clients.append('                  +------------------------+')
    self.clients.append('                  ||  Clients  Connected  ||')
    self.clients.append('------------------                          --------------------')
    self.clients.append('|| {}NUM{} ||\t Bssid\t     ||\t     Session   \t  ||   Time   ||  '.\
    format(COLORS['yellow'], COLORS['white']))
    self.clients.append('-'*64)
    self.clients.append('+{}+'.format('-'*62))
   self.clients.append('|| {} || {}  ||  {} || {} ||'.format(colored(_num),
    colored(bssid.upper()), colored(session), colored(time_connected)))
   if len(self.devices)-1 == num:
    self.clients.append('+{}+'.format('-'*62))

 def evil_twin_info(self):
  self.analyze_output()
  self.remove_device()
  self.organize_info()
  return self.clients
