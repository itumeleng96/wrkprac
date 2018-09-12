#!/usr/bin/python
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import spidev
import time
import os
import sys

#open SPI  bus
spi= spidev.SpiDev()	#create spi object
spi.open(0,0)		# initialise SPI

spi.max_speed_hz=1000000;
#RPI has one bus 0 and two SPI devices 0 and 1

#function to read ADC data from a channel
places = 3

def GetData(channel):
    adc=spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8)+adc[2]
    return data

def ConvertVolts(data,places):
    volts = (data*3.3)/float(1023)
    volts=round(volts,places)
    return volts

channel = 1
delay = .5

try:
    while True:
        sensr_data = GetData(channel)
        sensr_volt = ConvertVolts(sensr_data,2)
        print(sensr_volt)
        time.sleep(delay)
        
except KeyboardInterrupt:
    spi.close()
