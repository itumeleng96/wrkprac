# !/usr/bin/python

import RPi.GPIO as GPIO
import Adafruit_MCP3008 as MCP
import time
import os


# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# define pins
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# setup SPI pins for I/O
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# initialise communication with MCP3008
mcp = MCP.MCP3008 (clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

# create a global variable to store adc values
values = [0]*8

# delay between each reading
delay = 0.5

try:
	while True:
		for i in range(8):
			values[i] = mcp.read_adc(i)

		# provide delay
		time.sleep(delay)

		print (values)

except KeyboardInterrupt:
	GPIO.cleanup()	# clean up GPIO on CTRL+C exitt

# cleanup GPIO when finished
GPIO.cleanup()
