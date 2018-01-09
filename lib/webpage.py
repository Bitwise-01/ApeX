import os
import time
import subprocess
import lib.settings as settings
from commands import getoutput as shell

class Webpage(object):
 def __init__(self, handshake):
  self.is_alive = True
  self.passphrase = None
  self.handshake = handshake

 def aircrack(self):
  aircrack = shell('aircrack-ng -w {} {}'.format(settings.PASSLIST,
   self.handshake)).split('\n')[-1]

  if any([not 'KEY FOUND' in aircrack, self.passphrase]):return
  self.passphrase = aircrack.split()[-2]

 def create_index(self):
  if not self.passphrase:return
  with open(settings.INDEX_PAGE, 'w') as index_file:
   with open(settings.LOADING_PAGE, 'r') as html:
    index_file.write(html.read())

 def monitor(self):
  while all([not self.passphrase, self.is_alive]):
   if not os.path.exists(settings.PASSLIST):
    continue
   self.aircrack()
   self.create_index()
