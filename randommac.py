#!/usr/bin/env python
# Name:     randommac.py
# Purpose:  Set Mac Address To Random Address.
# By:       Jerry Gamblin
# Date:     24.07.15
# Modified  24.07.15
# Rev Level 0.1
# -----------------------------------------------

import os
import random
import fcntl
import socket 
import struct
import subprocess
import uuid
from itertools import imap
from random import randint
import time

def randomMAC():
	rmac = ':'.join(['%02x'%x for x in imap(lambda x:randint(0,255), range(6))])
	return rmac
	


def hwMAC():
	hwaddr = subprocess.Popen("networksetup -getmacaddress en0 | awk '{print $3}'", shell=True, stdout=subprocess.PIPE).stdout.read()
	hwaddr2 = hwaddr[0:17]
	return hwaddr2

def currentMAC():
	cmac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
	return cmac

#Store currentMAC as oldMAC
oldMAC = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
rMAC = randomMAC()

#Say what I am doing
print "\n"
print "Changing your MAC address to %s from %s." % (rMAC,oldMAC)
print "This will take 30 seconds."

#Change Mac Address
print "Changing Mac Address to %s" %rMAC
os.system("ifconfig en0 ether %s" %rMAC) 
time.sleep(10)


#Turn Off Wireless
print "Turning Off Wireless"
os.system("ifconfig en0 down")
time.sleep(10)

#Turn On Wireless
print "Turning On Wireless"
os.system("ifconfig en0 up")
time.sleep(10)

#Print New Mac
nmac = subprocess.Popen("ifconfig en0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'", shell=True, stdout=subprocess.PIPE).stdout.read()
print "Your new MAC address is %s" %nmac
