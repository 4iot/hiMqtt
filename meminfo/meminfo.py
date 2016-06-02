#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

def getMemoryStatus():
   memory = {}
   miexists = os.path.exists('/proc/meminfo')
   if ( miexists <> 0 ):
      meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())
      mem_total_kib = meminfo['MemTotal']  
      mem_free_kib = meminfo['MemFree']  
      swp_total_kib = meminfo['SwapTotal'] 
      swp_free_kib = meminfo['SwapFree']  
      memory['memAvail'] = mem_free_kib
      memory['memUsed'] = mem_total_kib - mem_free_kib
      memory['swpAvail'] = swp_free_kib
      memory['swpUsed'] = swp_total_kib - swp_free_kib
   else:
      a = 1
   return memory

