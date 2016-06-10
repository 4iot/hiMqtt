#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# $Date$

import json
import urllib2
import platform
import cpuinfo
import cputemp
import cputimes
import datetime
import time
from osinfo import OsInfo
import netinfo
import meminfo
from load import Load
import sys
import re
import os
from os.path import expanduser
from urllib2 import HTTPError
import HMMqtt
# to get ip address, see http://python.developpez.com/faq/?page=Reseau-Web
# 'https://api.ipify.org?format=json'

class HiMessage:
    "Sends and manages a Hi message to the server"
    
    __debug = False
    
    def __init__(self, msg=None, seq=None):
        
        self.reset()
            
        if ( msg != None ) : 
            self.__data['msg'] = msg
        if ( seq != None ) : 
            self.__data['seq'] = seq

    def reset(self):
        a = 1
        self.__data = {}
        from os.path import expanduser
        idFileName = expanduser("~") + '/.hidevid'
        fileExists = os.path.exists(idFileName)
        if ( fileExists ):
            idFileHandle = open(idFileName,'r')
            deviceId = idFileHandle.readline()
            deviceId = deviceId.strip()
            self.__data['id'] = deviceId
            idFileHandle.close
        
        now = datetime.datetime.now()
        self.__data['seq'] = int(round(time.time() * 1000))
        self.__data['tsClient'] = now.isoformat()
        cinfo = cpuinfo.get_cpu_info()
        self.__data['cpu'] = format(cinfo['brand'])
        self.__data['cpuCount'] = cinfo['count']
        osinfo = OsInfo()
        oinfo = osinfo.getOsInfo(cinfo)
        self.__data['os'] = oinfo['os']
        self.__data['osDist'] = oinfo['dist']
        self.__data['osVersion'] = oinfo['version']
        self.__data['osArch'] = oinfo['arch']
        self.__data['osKernel'] = oinfo['kernel']
        self.__data['cpuTemp'] = cputemp.get_cpu_temp()
        l = Load()
        self.__data['cpuLoad'] = l.getCpuLoad()
        MemInfo = meminfo.getMemoryStatus()
        self.__data['memAvail'] = MemInfo['memAvail'] / 1024
        self.__data['memUsed'] = MemInfo['memUsed'] / 1024
        self.__data['swapAvail'] = MemInfo['swpAvail'] / 1024
        self.__data['swapUsed'] = MemInfo['swpUsed'] / 1024
        self.__data['storage'] = l.getStorageStatus()
        self.__data['network'] = netinfo.get_network_interfaces()
        CpuTimes = cputimes.get_cpu_times()
        self.__data['cpuUser'] = CpuTimes['user']
        self.__data['cpuSystem'] = CpuTimes['system']
        self.__data['cpuIdle'] = CpuTimes['idle']
        self.__data['ioWait'] = CpuTimes['iowt']
        self.__data['UpTime'] = CpuTimes['uptime']

    def send(self,publicUrl,msg):
        # append public URL to data
        self.__data['clientIp'] = publicUrl
        HMMqtt.publish_message('messages','insert',self.__data['id'],self.__data)

    def add(self, key, value):
        self.__data[key] = value
        
    def info (self, msg):
        if ( msg != None ): 
            self.__data['msg'] = msg

