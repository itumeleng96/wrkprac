#!/usr/bin/python
import RPi.GPIO as GPIO

import spidev

import time

import os

import sys

GPIO.setmode(GPIO.BCM)
#initilaize buttons
switch_reset=23
switch_stop=24
switch_changeFreq=25
#initilaize pull ups
GPIO.setup(switch_reset,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_stop,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_changeFreq,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#function definition:threaded callback

#not done


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
#convert data from LDR 
# returns value in volts not percentage yet
def ConvertLDR(data,places):
	lightInten=(data*3.3)/float(1023)
	lightInten=(3.3-lightInten)/3.3
	lightInten=round(lightInten*100,places)
	return lightInten

channel = 0
delay = 2

#output 
try:
    print("----------------------------------------------")
    print(" Time       Timer      Pot     Temp     Light ")
    print("----------------------------------------------")

    while True:
	#read pot
	pot_reading=ConvertPot(GetData(2),3)
	#read temp sensor 
	temp_reading=ConvertTemp(GetData(0),3)
	#read light sensor 
	light_reading=ConvertLDR(GetData(1),1)
	#time 
	str_time=time.strftime("%H:%M:%S")
	#timer not implemented yet 
	timer ="----------"

	print(" {} {}   {}V  {}C  {}%".format(str_time,timer,pot_reading,temp_reading,light_reading))
	print("---------------------------------------------")
	time.sleep(delay)

except KeyboardInterrupt:
    spi.close()
