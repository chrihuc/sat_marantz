# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 20:17:45 2016

@author: christoph
"""

from msi import *
import serial
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import os

import time
from time import localtime,strftime
import paho.mqtt.client as mqtt
import json

import constants

PORT_NUMBER = 5010
SIZE = 1024

hostName = gethostbyname( '0.0.0.0' )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

serialIn = serial.Serial('/dev/ttyUSB0', 9600, bytesize=8, parity='N', stopbits=1, timeout=0)
MSI = MarantzSerialInterface(serialIn)
MSI.start()

#MSI.cmd('VOL', '0-35')

def connect(ipaddress, port):
    global client
    zeit =  time.time()
    uhr = str(strftime("%Y-%m-%d %H:%M:%S",localtime(zeit)))
    client = mqtt.Client(constants.name +'_sub_' + uhr, clean_session=False)
    assign_handlers(on_connect, dis_con, on_message)
    client.username_pw_set(username=constants.mqtt_.user,password=constants.mqtt_.password)
    client.connect(ipaddress, port, 60)
#    client.loop_start()
    client.loop_forever()

def assign_handlers(connect, disconnect, message):
    """
    :param mqtt.Client client:
    :param connect:
    :param message:
    :return:
    """

    global client
    client.on_connect = connect
    client.on_disconnect = disconnect
    client.on_message = message


def on_connect(client_data, userdata, flags, rc):
    global client, topics
    if rc==0 and not client.connected_flag:
        client.connected_flag=True #set flag
        print("connected OK")
        for topic in topics:
            client.subscribe(topic)
    elif client.connected_flag:
        pass
    else:
        print("Bad connection Returned code=",rc)
#    print "connected"
#    client.subscribe(topic)

def dis_con (*args, **kargs):
    print("disconnected")

def on_message(client, userdata, msg):
#    print(msg.topic + " " + str(msg.payload))
    try:
        m_in=(json.loads(msg.payload)) #decode json data
#        print(m_in)
        if m_in['Name'] == "STOP":
            os.system("sudo killall python")
            #pass
        elif m_in['Name'] == "TV_ein":
            os.system("echo 'on 0' | cec-client -s")
            #os.system("irsend SEND_START TV_3 Power_on")
            #time.sleep(2)
            #os.system("irsend SEND_STOP TV_3 Power_on")  
        elif m_in['Name'] == "AMPein":
            #os.system("irsend SEND_START RC003SR_5 PowerOn")
            #time.sleep(1.5)
            #os.system("irsend SEND_STOP RC003SR_5 PowerOn")
            MSI.cmd('PWR', '2')
        elif m_in['Name'] == "Update":
            dicti = {}
            status = MSI.status()
            dicti['Power'] = str(status.pwr)
            dicti['Volume'] = str(status.vol)
            dicti['Source'] = str(status.src)
            dicti['Mute'] = str(status.mute)
            dicti['Attenuate'] = str(status.att)
            dicti['Bass'] = str(status.bass)
            dicti['Treble'] = str(status.treble)
            #mySocket.sendto(str(dicti),(OUTPUTS_IP,OUTPUTS_PORT))          
        else:
            try:
                    #print data
                    data_ev = eval(data)
                    if m_in.get('Name') == 'TV_ein':
                        os.system("echo 'on 0' | cec-client -s")
                        os.system("irsend SEND_START TV_3 Power_on")
                        time.sleep(2)
                        os.system("irsend SEND_STOP TV_3 Power_on")                         
                    for cmd in m_in:
                        if m_in.get(cmd) <> None:
                            MSI.cmd(str(cmd), str(data_ev.get(cmd)))
            except NameError as serr:
                    pass

    except ValueError:
        print("no json code")
        
        
mqtt.Client.connected_flag=False
client = None
topics = ["Command/Satellite/" + constants.name + "/#"]
ipaddress = constants.mqtt_.server
port = 1883



def main():
    global client, topic, ipaddress, port
    connect(ipaddress, port)


if __name__ == "__main__":
    main()        
