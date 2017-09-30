# Date: 07/29/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Installs requirements

import subprocess

# requirements
software = ['isc-dhcp-server', 'python-scapy', 'lighttpd', 'hostapd', 'php7.0-cgi']

# update
subprocess.call('apt-get update && apt-get upgrade -y', shell=True)

# install
for software in software:
  subprocess.call('apt-get install -y {}'.format(software), shell=True)
