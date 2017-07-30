# Date: 07/04/2017
# Distro: Kali linux
# Author: Ethical-H4CK3R
# Description: Creates configuration files

class Dhcpd(object):
 def __init__(self):
  self._file = 'dhcpd.conf'
  self.config = '''authoritative;
max-lease-time 7200;
default-lease-time 600;
subnet 192.168.0.0 netmask 255.255.255.0
{
   option routers 192.168.0.1;
   range 192.168.0.2 192.168.0.254;
   option subnet-mask 255.255.255.0;
   option domain-name-servers 192.168.0.1;
   option broadcast-address 192.168.0.255;
}'''

 def write(self):
  with open('dhcpd.leases','w+') as dhcpd:pass
  with open(self._file,'w+') as fwrite:
   fwrite.write(self.config)

class Lighttpd(object):
 def __init__(self):
  self._file = 'lighttpd.conf'
  self.config = '''
# location of index.html
server.document-root="/tmp/ApeX/site"

# set permissions
server.modules = (
	"mod_access",
	"mod_alias",
	"mod_accesslog",
	"mod_fastcgi",
	"mod_redirect",
	"mod_rewrite"
	)

# php configs
fastcgi.server = ( ".php" => ((
		  "bin-path" => "/usr/bin/php-cgi",
		  "socket" => "/php.socket"
		)))

server.port = 80
server.pid-file = "/var/run/lighttpd.pid"

mimetype.assign = (
	".html" => "text/html",
	".htm" => "text/html",
	".txt" => "text/plain",
	".jpg" => "image/jpeg",
	".png" => "image/png",
	".css" => "text/css"
	)

static-file.exclude-extensions = (".fcgi", ".php", ".rb", "~", ".inc")
index-file.names = ("index.htm", "index.html")

# 404 handler
server.error-handler-404 = "/"

# redirect
$HTTP["host"] =~ "^www\.(.*)$" {
    url.redirect = ( "^/(.*)" => "http://192.168.0.1")
	ssl.engine  = "enable"
	ssl.pemfile = "/tmp/ApeX/cert.pem"
}'''

 def write(self):
  with open(self._file,'w+') as fwrite:
   fwrite.write(self.config)

class Hostapd(object):
 def __init__(self,channel,ssid,interface):
  self.essid = ssid
  self.iface = interface
  self._file = 'hostapd.conf'
  self.channel = channel
  self.config = 'interface={}\ndriver=nl80211\nssid={}\nchannel={}\n'.format(self.iface,self.essid,self.channel)

 def write(self):
  with open(self._file,'w+') as fwrite:
   fwrite.write(self.config)
