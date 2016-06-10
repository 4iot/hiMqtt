import paho.mqtt.client as mqttcl
from os.path import expanduser
import netinfo
import os
import json
import re
import shutil

def on_connect(client, userdata, flags, rc):
    print("Device connected as " + client._client_id + " status " +str(rc))

global deviceId

def on_message(client, userdata, msg):
    match = re.search('4iot/register_accepted',msg.topic)
    if ( match != None ):
        print "Device accepted"
        match = re.search('device is now identified as \[(\w{33})',msg.payload)
        if ( match == None ):
            a = 1
        else:
            deviceId = match.group(1)
            idFileName = expanduser("~") + '/.hidevid'
            if ( os.path.exists(idFileName)):
                # if file already exists, remove to be replaced
                os.remove(idFileName)

            fileExists = os.path.exists(idFileName)
            idFileHandle = open(idFileName,'w')
            idFileHandle.write(deviceId)
            idFileHandle.close
            # copy file to /tmp for if any other user
            copyfile('/tmp/.hidevid',idFileName)
            client.unsubscribe(expected_topic)
    else:
        print "Device rejected"
        exit(1)

def connectMqtt(Broker,Port,Keepalive):
    global broker
    global port
    global keepalive
    broker = Broker
    port = Port
    keepalive = Keepalive
    from os.path import expanduser
    deviceCacheFileName = expanduser("~") + '/.deviceCache'
    idFileName = expanduser("~") + '/.hidevid'
    while  not (os.path.exists(idFileName)):
        if ( os.path.exists('/tmp/.hidevid')):
            # hi has been launched sometime by another user
            # take /tmp/.hidevid and copy to user's home
            idFileHandle = open(idFileName,'r')
            deviceId = idFileHandle.readline()
            deviceId = deviceId.strip()
            idFileHandle.close
            idFileName = expanduser("~") + '/.hidevid'
            copyfile('/tmp/.hidevid',idFileName)
        else:
            network = netinfo.get_network_interfaces()
            networkMac = network['eth0']['mac']
            if ( networkMac != None ):
                client =  "4iot@" + networkMac + ":" + str(os.getpid())
                clientId = client
                deviceId = None
                break

    if ( os.path.exists(idFileName) ):
        idFileHandle = open(idFileName,'r')
        deviceId = idFileHandle.readline()
        deviceId = deviceId.strip()
        idFileHandle.close
        print("Device connected as " + deviceId)
    elif ( deviceId == None and clientId != None ):
        expected_topic = "4iot/register_accepted/" + clientId
        mqttc = mqttcl.Client(client)
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.connect(broker,port,keepalive)
        mqttc.subscribe(expected_topic,2)
        mqttc.publish("4iot/please_register", clientId,2)
        mqttc.loop_forever()
    else:
        print ('No way to register, sorry!')
        
def publish_message(collection,statement,client,contents):
    mqttc = mqttcl.Client(client)
    mqttc.connect(broker,port,keepalive)
    topic = '4iot/' + statement + '/' + collection
    #mqttc.publish("4iot/message", json.dumps(contents),1)
    mqttc.publish(topic, json.dumps(contents),1)
    mqttc.disconnect()
