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

PORT_NUMBER = 5010
SIZE = 1024

hostName = gethostbyname( '0.0.0.0' )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

serialIn = serial.Serial('/dev/ttyUSB0', 9600, bytesize=8, parity='N', stopbits=1, timeout=0)
MSI = MarantzSerialInterface(serialIn)
MSI.start()

#MSI.cmd('VOL', '0-35')

while True:
        (data,addr) = mySocket.recvfrom(SIZE)
        #print data
        #print addr
        isdict = False
        try:
            data_ev = eval(data)
            if type(data_ev) is dict:
                isdict = True
                #print data_ev
        except NameError as serr: 
            isdict = False        
        if data == "STOP":
            os.system("sudo killall python")
            #pass
        elif data == "TV_ein":
            os.system("echo 'on 0' | cec-client -s")
            #os.system("irsend SEND_START TV_3 Power_on")
            #time.sleep(2)
            #os.system("irsend SEND_STOP TV_3 Power_on")  
        elif data == "AMPein":
            #os.system("irsend SEND_START RC003SR_5 PowerOn")
            #time.sleep(1.5)
            #os.system("irsend SEND_STOP RC003SR_5 PowerOn")
            MSI.cmd('PWR', '2')
        elif data == "Update":
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
                    if (data_ev.get("Command") <> "") and (data_ev.get("Value") <> ""):
                        MSI.cmd(str(data_ev.get("Command")), str(data_ev.get("Value")))
            except NameError as serr:
                    pass
        #print type(data_ev)
sys.ext()