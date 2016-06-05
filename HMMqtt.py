import paho.mqtt.client as mqttcl
from os.path import expanduser
import netinfo
import os
import json
import re
import time

global deviceId

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


def on_message(client, userdata, msg):
    match = re.search('4iot/register_accepted/(.+)',msg.topic)
    if ( match != None ):
        clientId = match.group(1)
        match = re.search('device is now identified as \[(\w{33})',msg.payload)
        if ( match == None ):
            a = 1
        else:
            deviceId = match.group(1)
            print "Device registered: " + deviceId
            idFileName = expanduser("~") + '/.hidevid'
            fileExists = os.path.exists(idFileName)
            if fileExists:
                # if file already exists, remove to be replaced
                os.remove(idFileName)
            fileExists = os.path.exists(idFileName)
            idFileHandle = open(idFileName,'w')
            idFileHandle.write(deviceId)
            idFileHandle.close
            client.unsubscribe(msg.topic)
            client.disconnect()
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
    fileExists = os.path.exists(idFileName)
    if ( fileExists ):
        idFileHandle = open(idFileName,'r')
        deviceId = idFileHandle.readline()
        deviceId = deviceId.strip()
        idFileHandle.close
    else:
	client = ''
        network = netinfo.get_network_interfaces()
	for dvc in network:
		if network[dvc]['mac'] != None:
			client = client + network[dvc]['mac']

        if ( client != None ):
            clientId = client
            deviceId = None


    if ( deviceId == None and clientId != None ):
        expected_topic = "4iot/register_accepted/" + clientId
        topic = "4iot/please_register"
        mqttc = mqttcl.Client(client)
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.connect(broker,port,keepalive)
        mqttc.publish(topic, clientId,2)
        mqttc.subscribe(expected_topic,2)
        mqttc.loop_forever()
	
    else:
        a = 1   
        
def publish_message(client,message):
    mqttc = mqttcl.Client(client)
    mqttc.connect(broker,port,keepalive)
    mqttc.publish("4iot/message", json.dumps(message),1)
    mqttc.loop(timeout=1.0, max_packets=1)
