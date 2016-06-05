#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from HiMessageMqtt import HiMessage
import HMMqtt 
import os.path
from os.path import expanduser
import netinfo
import json
import ConfigParser
import time
import urllib2


# Read the configuration file
Config = ConfigParser.ConfigParser()
from os.path import expanduser
CfgFileName = expanduser("~") + '/hiconfig.ini'
Config.read(CfgFileName)
broker = Config.get('mqtt','broker',raw=False)
port = Config.getint('mqtt','port')
keepalive = Config.getint('mqtt','keepalive')
loopmode = Config.getboolean('misc','loopmode')
loopwait = Config.getint('misc','loopwait')


# Connect to mqtt server
HMMqtt.connectMqtt(broker,port,keepalive)

# Get public IP address
url = 'https://api.ipify.org?format=json'
req = urllib2.Request(url)
try:
    response = urllib2.urlopen(req)
except HTTPError as e:
    print ("HTTP Post error: #%d (%s), while connecting to %s." % (e.code, e.reason, url))


the_page = json.loads(response.read())
publicUrl = the_page['ip']
while True:
   msg = HiMessage()
   if (len(sys.argv) > 0):
      index = 1
      message = ""
      while (index < len(sys.argv)):
         message += sys.argv[index] + ' '
         index += 1
         message = message.rstrip()

         if (message != None) and (message != ""):
            msg.info(message)

   msg.send(publicUrl,msg)
   if (loopmode == True ):
      time.sleep(loopwait)
   else:
       break

                
