#!/usr/bin/python
# coding=utf-8

from __future__ import print_function
import serial
import struct
import sys
import urllib
import time
import Adafruit_DHT

ser = serial.Serial()
ser.port = sys.argv[1]
ser.baudrate = 9600

ser.open()
ser.flushInput()

byte, data = 0, ""
humidity, temperature = Adafruit_DHT.read_retry(11, 4)

def dump_data(d):
    print(' '.join(x.encode('hex') for x in d))

def process_frame(d):
    # dump_data(d)
    r = struct.unpack('<HHxxBBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    # print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))
    
    if humidity is not None and temperature is not None and checksum==r[2] and r[3]==0xab:
    	params = urllib.urlencode({'key': '866D1Z9RN369X1J5', 'field1': pm25, 'field2': pm10, 'field3': temperature, 'field4': humidity })
    	response = urllib.urlopen("https://api.thingspeak.com/update", data=params)

    time.sleep(2*60)

while True:
    while byte != "\xaa":
        byte = ser.read(size=1)
    d = ser.read(size=10)
    if d[0] == "\xc0":
        process_frame(byte + d)
