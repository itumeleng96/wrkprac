#!/usr/bin/python
import RPi.GPIO as GPIO

import spidev

import time

import os

import sys

#GPIO.setmode(GPIO.BCM)
#open SPI  bus

spi= spidev.SpiDev()   #create spi object

spi.open(0,0)

spi.max_speed_hz=1000000;
#RPI has one bus 0 and tow SPI devices o and 1 

#function to read ADC data from a channel
places = 3

def GetData(channel):
    adc=spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8)+adc[2]
    return data
#converts data from potentiometer to voltage 
def ConvertPot(data,places):
    volts = (data*3.3)/float(1023)
    volts=round(volts,places)
    return volts
#convert data from Temp sensor to degrees celcius
def ConvertTemp(data,places):
	temp = (((data*3.3)/float(1023))-0.5)*100
	temp = round(temp,places)
	return temp

def ConvertLDR(data,places):
	#still to be calibrated
channel = 0
delay = .5

try:
    while True:
        sensr_data = GetData(channel)
        sensr_volt = ConvertTemp(sensr_data,2)
        print(sensr_volt)
        time.sleep(delay)
        
except KeyboardInterrupt:
    spi.close()
