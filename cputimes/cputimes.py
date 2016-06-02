#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
import time
import platform
import subprocess

try:
	import _winreg as winreg
except ImportError as err:
	try:
		import winreg
	except ImportError as err:
		pass

PY2 = sys.version_info[0] == 2


def has_proc_stat():
	bits = platform.architecture()[0]
	return os.path.exists('/proc/stat')

def get_cpu_times():
	cputimes = {}
	if (has_proc_stat()):
		procfile = open('/proc/stat', 'r') 
		while 1:
			cputimeline = procfile.readline() 
			if ( cputimeline == "" ):
				break
			statline = cputimeline.split()
			if (statline[0] == 'cpu'):
				userT = float(statline[1])
				systemT = float(statline[2])
				iowT = float(statline[3])
				idleT = float(statline[4])
				TotalCpu = userT + systemT + idleT + iowT
				cputimes['user'] = int((userT / float(TotalCpu)) * 100)
				cputimes['system'] = int((systemT / float(TotalCpu)) * 100)
				cputimes['idle'] = int((idleT / float(TotalCpu)) * 100)
				cputimes['iowt'] = int((iowT / float(TotalCpu)) * 100)
			elif statline[0] == 'btime':
				btime = int(statline[1])
				#now1000 = int(round(time.time() * 1000))
				now = int(round(time.time()))
				#uptimeSec = (now1000/1000) - btime
				uptimeSec = now - btime
				days = uptimeSec / 86400 
				uptimeSec %= 86400
				hours = uptimeSec / 3600
				uptimeSec %= 3600
				minutes = uptimeSec/60
				uptimeSec %= 60
				cputimes['uptime'] = "%d %02d:%02d:%02d" % (days,hours,minutes,uptimeSec)
	return cputimes
