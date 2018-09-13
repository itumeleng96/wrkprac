# !/usr/bin/python

import RPi.GPIO as GPIO

# set GPIO mode
GPIO.setmode(GPIO.BCM)

# select pins to trigger interrupts
switch_1 = 17
switch_2 = 27
switch_3 = 22

# switch 1 & switch 2: input - pull-up
GPIO.setup(switch_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# switch 3: input - pull-down
GPIO.setup(switch_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# function definition: threaded callback
def callback1(channel):
	# put code here
	print "Hello"

def callback2(channel):
	# put code here
	print "World!"

# under a falling-edge detection, regardless of current execution
# callback function will be called
GPIO.add_event_detect(switch_1, GPIO.FALLING, callback=callback1, bouncetime=200)
GPIO.add_event_detect(switch_2, GPIO.FALLING, callback=callback2, bouncetime=200)

# 'bouncetime=200' includes the bounce control
# 'bouncetime=200' sets 200 milliseconds during which second button press will be ignored.

# to remove: GPIO.remove_event_detect(port_number)
try:
	GPIO.wait_for_edge(switch_3, GPIO.RISING)

except KeyboardInterrupt:
	GPIO.cleanup()	# clean up GPIO on CTRL+C exit

GPIO.cleanup()	# clean up GPIO on normal exit
