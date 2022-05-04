# Originally posted:
# https://samedayrules.com/using-smd-npn-relay-board

import RPi.GPIO as GPIO # access to GPIO pins
import time # use this to pause execution below

pins = [2, 3, 4, 17, 27, 22, 10, 9] # list of pins we'll be using
GPIO.setmode(GPIO.BCM) # reference pins using logical pin numbers
GPIO.setup(pins, GPIO.OUT) # set all pins to output mode
GPIO.output(pins, GPIO.LOW) # set all pins low (de-activates relays)

# Loop through pins, turning them ON, pausing, then OFF
for p in pins:
  GPIO.output(p, GPIO.HIGH) # relay associated with this pin should now be ON
  time.sleep(3) # pause for 3 seconds
  GPIO.output(p, GPIO.LOW) # relay should now be OFF

# Turn all the relays ON and then OFF
GPIO.output(pins, GPIO.HIGH)
time.sleep(3)
GPIO.output(pins, GPIO.LOW)

# Cleanup
GPIO.cleanup()
