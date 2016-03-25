# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 14:03:46 2016

@author: Patrick
"""

import serial,time, sys
ser = serial.Serial()

def initializePort():
    global ser
    if sys.platform == 'darwin':
        commPort = '/dev/tty.usbserial'
    else:
        commPort ='/dev/ttyUSB0'
    
    ser.setPort(commPort)
    ser.setBaudrate(9600)
    ser.setParity(serial.PARITY_NONE)
    ser.setByteSize(serial.EIGHTBITS)
    openPort()

def openPort(): 
    while ser.isOpen() :
        cmd = '$026\r\n' #Ask what switches are open
        ser.write(cmd)
        out = ''
            # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)
        if out != '':
            print ">>" + out

if __name__ == "__main__":
    initializePort()