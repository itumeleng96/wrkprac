#!/usr/bin/python
import RPi.GPIO as GPIO
import spidev
import time
import os
import sys

GPIO.setmode(GPIO.BCM)
#initilaize buttons
switch_reset = 23
switch_stop = 24
switch_changeFreq = 25
switch_display = 18

#initilaize pull ups
GPIO.setup(switch_reset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(switch_stop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(switch_changeFreq, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(switch_display, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#open SPI  bus
spi = spidev.SpiDev()   #create spi object
spi.open(0,0)
spi.max_speed_hz = 1000000

#parameters
places=3
frequency = 0.5
startStop = True
consoleTimer = 0
elapsed_Time = 0
counter = 0
#RPI has one bus 0 and tow SPI devices o and 1 
#threaded callbacks

disp = False
consoleTimer = 0
elapsed_Time = 0
results = [" "]*5
#RPI has one bus #0 and two SPI devices 0 and 1 

#threaded callbacks
def changeFrequency(channel):
    global frequency
    if (frequency == 0.5):
        frequency = 1
    elif (frequency == 1):
        frequency=2
    elif (frequency == 2):
        frequency=0.5

def reset(channel):
    global elapsed_Time
    global consoleTimer
    elapsed_Time=time.time()
    consoleTimer=time.time()
    elapsed_Time=time.time()-consoleTimer

def startStop(channel):
    global disp
    global startStop
    if(startStop):
        startStop=False
        disp = True
    else:
        startStop=True

def display(channel):
    global disp
    global results
    if disp == False:
        pass
    else:
        if len(results) > 5:
            for i in range(5):
                print(results[i])
                print("------------------------------------------")
        elif len(results) <= 5:
            for i in range(len(results)):
                print(results[i])
                print("------------------------------------------")
        disp = False

#add event detect for buttons
GPIO.add_event_detect(switch_reset,GPIO.FALLING,callback=reset,bouncetime=200)
GPIO.add_event_detect(switch_stop,GPIO.FALLING,callback=startStop,bouncetime=200)
GPIO.add_event_detect(switch_changeFreq,GPIO.FALLING,callback=changeFrequency,bouncetime=200)
GPIO.add_event_detect(switch_display,GPIO.FALLING,callback=display,bouncetime=200)

#function to read ADC data from a channel
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
    temp = round(temp)
    return temp

#convert data from LDR 
# returns value in volts not percentage yet

def ConvertLDR(data):
    lightInten=(data*3.3)/float(1023)
    lightInten=(3.3-lightInten)/3.3
    lightInten=round(lightInten*100)
    return lightInten

#output 
try:
    print("------------------------------------------")
    print(" Time      Timer     Pot     Temp   Light ")
    print("------------------------------------------")
    pot_reading=0.0
    temp_reading=0.0
    light_reading=0.0
    consoleTimer=time.time()

    while True:
	
	#time
        str_time=time.strftime("%H:%M:%S")
        elapsed_Time=time.time() - consoleTimer
        elapsed_Time=time.strftime("%H:%M:%S",time.gmtime(elapsed_Time))
        #read pot
        pot_reading=ConvertPot(GetData(2),3)
        #read temp sensor
        temp_reading=ConvertTemp(GetData(0),3)
        #read light sensor
        light_reading=ConvertLDR(GetData(1))
        
        if (startStop):  #start or stop sensors
            print(" {}  {}  {}V  {}C  {}%".format(str_time,elapsed_Time,pot_reading,temp_reading,light_reading))
            print("------------------------------------------")
            
            #read pot
            #results.append(" {}  {}  {}V  {}C  {}%".format(str_time,elapsed_Time,pot_reading,temp_reading,light_reading))
        
        elif (startStop == False):
            if(counter<5):
                results[counter] = " {}  {}  {}V  {}C  {}%".format(str_time,elapsed_Time,pot_reading,temp_reading,light_reading)
                
            counter = counter + 1
        time.sleep(frequency)

except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()
