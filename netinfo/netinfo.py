#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import platform
import subprocess

def add_interface (ifaces, iface, requireIp=False):
    if (iface == None):
        return ifaces
    if (len(iface) == 0):
        return ifaces
    if ('mac' not in iface):
        return ifaces
    if ( ((requireIp == True) and (('ipv4' in iface) or ('ipv6' in iface))) or (requireIp == False) ):
        ifaces[iface['name']] = iface
        del iface['name']
    return ifaces
    
def get_network_interfaces():
    if (platform.system() == 'Darwin'):
        return get_network_interfaces_mac()
    else:
        return get_network_interfaces_linux()

def get_network_interfaces_linux():
    ifaces = {}
    iface = {}
    
    res = subprocess.check_output(['ifconfig', '-a']).splitlines()
    #with open ("test/ubuntu-14.04.1.txt", "r") as myfile:
    #with open ("test/raspbian-4.4.7.txt", "r") as myfile:
    #    res = myfile.readlines()
    length = len(res)
    index = 0
    context = ''
    while (index < length):
        currentLine = res[index]
        values = currentLine.split()
        if currentLine != '':
            if (currentLine[0].isspace() != True):
                ifaces = add_interface(ifaces, iface)
                iface = {}
                iface['name'] = values[0]
                if (len(values) > 4):
                    iface['mac'] = values[4]
            else:
                if (len(values) > 0):
                    if (values[0] == 'inet'):
                        iface['ipv4'] = values[1][5:]
                    elif (values[0] == 'inet6'):
                        iface['ipv6'] = values[2]
       
        index += 1
    ifaces = add_interface(ifaces, iface)

    return ifaces

def get_network_interfaces_mac():
    ifaces = {}
    iface = {}
    
    res = subprocess.check_output(['ifconfig', '-a']).splitlines()
    length = len(res)
    index = 0
    context = ''
    while (index < length):
        currentLine = res[index]
        if (currentLine[0].isspace() != True):
            # New context
            context = res[index].split(':')[0]
            ifaces = add_interface(ifaces, iface)
            iface = {}
            iface['name'] = context
        else:
            # analyze the line
            values = currentLine.split()
            if (values[0] == 'ether'):
                iface['mac'] = values[1]
            elif (values[0] == 'inet'):
                iface['ipv4'] = values[1]
            elif (values[0] == 'inet6'):
                iface['ipv6'] = values[1]
        index += 1
    ifaces = add_interface(ifaces, iface)
    return ifaces


#interfaces = get_network_interfaces_linux()
#interfaces = get_network_interfaces()
#print interfaces

#
