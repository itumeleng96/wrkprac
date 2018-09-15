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


try:
    while True:        
except KeyboardInterrupt:
    spi.close()
