#!/usr/bin/python
import sys
import Adafruit_DHT
import urllib
import time

humidity, temperature = Adafruit_DHT.read_retry(11, 4)

def process_frame():
   if humidity is not None and temperature is not None:
   	# print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
   	params = urllib.urlencode({'key': '866D1Z9RN369X1J5', 'field3': temperature, 'field4': humidity})
   	response = urllib.urlopen("https://api.thingspeak.com/update", data=params)
   else:
   	print 'Failed to get reading. Try again!'

while True:
    process_frame()
    time.sleep(2*60)
