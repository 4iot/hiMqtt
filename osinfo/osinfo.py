#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import platform

class OsInfo:
    "Operating System information"
    
    __isSet = False
    __isMacOS = False
    __isLinux = False
    __isWindows = False

    def getOsInfoLinux(self, cinfo = None):
        rinfo = platform.linux_distribution()
        if (rinfo[1] == ''):
            info = None
        else:
            info = {}
            info['os'] = 'Linux'
            info['dist'] = rinfo[0]
            info['version'] = rinfo[1]
            if (cinfo != None):
                info['arch'] = cinfo['arch']
            else:
                info['arch'] = platform.processor()
            info['kernel'] = platform.uname()[2]
            self.__isLinux = True
            self.__isSet = True
            
        return info

    def getOsInfoWindows(self, cinfo = None):
        return None
    
    def getOsInfoMacOS(self, cinfo = None):
        rinfo = platform.mac_ver()
        if (rinfo == None):
            info = None
        else:
            info = {}
            info['os'] = 'MacOS'
            info['dist'] = 'X'
            info['version'] = rinfo[0]
            info['arch'] = rinfo[2]
            info['kernel'] = platform.uname()[2]
            self.__isMacOS = True
            self.__isSet = True
    
        return info

    def getOsInfo(self, cinfo = None):
        info = None
    
        info = self.getOsInfoLinux(cinfo)
        if not info:
            info = self.getOsInfoWindows(cinfo)
        if not info:
            info = self.getOsInfoMacOS(cinfo)
        return info
    
    def isMacOS(self):
        if self.__isSet == False:
            self.getOsInfo()
        return self.__isMacOS

    def isLinux(self):
        if self.__isSet == False:
            self.getOsInfo()
        return self.__isLinux

#osi=OsInfo()
#print osi.isMacOS()
#print osi.isLinux()
