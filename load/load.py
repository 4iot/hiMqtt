#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import subprocess
import sys

sys.path.append('../osinfo')
from osinfo import OsInfo

class Load:
    
    __osi = None
    
    def __init__(self):
        self.__osi = OsInfo()

    def getCpuLoad(self):
        res = subprocess.check_output(['sh', '-c', 'ps -e -o %cpu | awk \'{s+=$1} END {print s}\''])
        return float(res)

    def getStorageStatus(self):
        res = subprocess.check_output(['sh', '-c', 'df -Pk | grep "/dev/" | grep -v tmp']).splitlines()
        drives = {}
        index = 0;
        count = len(res)
        
        while index < count:
            current = res[index].split()
            drive = {}
            if (self.__osi.isMacOS() == True):
                drive['diskDev'] = current[0]
		drive['diskUsed'] = int(current[2]) / 1024
                drive['diskAvail'] = int(current[3]) / 1024
                drive['diskMount'] = current[8]
            elif (self.__osi.isLinux() == True):
                drive['diskDev'] = current[0]
                drive['diskUsed'] = int(current[2]) / 1024
                drive['diskAvail'] = int(current[3]) / 1024
                drive['diskMount'] = current[5]
            else:
                print 'Error: unknown OS'
            if (len(drive) > 0):
                drives[drive['diskMount']] = drive
                del drive['diskMount']
            index += 1
            
        return drives

#l = Load()
#print l.getCpuLoad()
#print l.getStorageStatus()

