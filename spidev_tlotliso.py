# !/usr/bin/python
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import spidev
import time
import os
import sys

# open SPI  bus
spi= spidev.SpiDev()	# create spi object
spi.open(0,0)		# initialise SPI
spi.max_speed_hz=1000000;
# RPI has one bus (#0) and two SPI devices #0 and #1

places = 3	# holder ...

# function to read ADC data from a channel
def GetData(channel):			# integer 0-7
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# function to convert data to voltage level
# places: number of decimal places needed
def ConvertVolts(data, places):
    volts = (data*3.3) / float(1023)
    volts = round(volts, places)
    return volts

# define sensor channels
channel = 0

# define delay after each reading
delay = .5

try:
    while True:
	# read data
        sensr_data = GetData(channel)
        sensr_volt = ConvertVolts(sensr_data, 2)

	print(sensr_volt)	# test statement

	# wait before repeating the loop
	time.sleep(delay)

except KeyboardInterrupt:
    spi.close()
