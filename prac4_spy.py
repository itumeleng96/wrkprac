#!/usr/bin/python
import RPi.GPIO as GPIO
import spidev
import time
import os
import sys

spi = spidev.SpiDev()   #create spi object
spi.open(0,0)
spi.max_speed_hz=1000000;
#RPI has one bus 0 and tow SPI devices o and 1

# Set pins to trigger interrupts
# set GPIO mode
GPIO.setmode(GPIO.BCM)

# select pins to trigger interrupts
reset = 17
frequency = 27
stop = 22
display = 18

# Set pins as pull-up
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(frequency, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(display, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set defaults
timer = 0
channel = 0
f = 0.5
status = False

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

# convert data from LDR 
# returns value in volts not percentage yet
def ConvertLDR(data):
	lightInten=(data*3.3)/float(1023)
	lightPercent=lightInten*100/3.3
	lightPercent=round(lightPercent)
	return lightPercent

# start program
try:
    print("----------------------------------------------")
    print(" Time       Timer      Pot     Temp     Light ")
    print("----------------------------------------------")

    while True:
        if GPIO.input(stop) == 0:
            
        
        if GPIO.input(reset) == 0:
            timer = 0
        if GPIO.input(frequency) == 0:
            if f == 2.0:
                f = 0.5
            elif f < 2.0:
                f = f*2
        
            #read pot
            pot_reading=ConvertPot(GetData(2),3)
            #read temp sensor
            temp_reading=ConvertTemp(GetData(0),3)
            #read light sensor
            light_reading=ConvertLDR(GetData(1))
            #time
            str_time=time.strftime("%H:%M:%S")
        
        if GPIO.input(stop) == 0:
            print("Monitoring stopped")
            pass
        
        
        #timer not implemented yet
        timer = "00:00:00"
        print(" {} {}   {}V  {}C  {}%".format(str_time,timer,pot_reading,temp_reading,light_reading))
        print("------------------------------------------")
        time.sleep(f)

except KeyboardInterrupt:
    spi.close()
