#
# nes-keypress.py
#
# Usage: python nes-keypress.py [--verbose] -if INPUT_FILE
#
# Input File Format:
# {
#  "latch_pin": 10,
#  "clock_pin": 3,
#  "data_pin": 7,
#  "key_mapping": {
#    "a": "KEY_Z",
#    "b": "KEY_X",
#    "select": "KEY_Q",
#    "start": "KEY_E",
#    "up": "KEY_W",
#    "down": "KEY_S",
#    "left": "KEY_A",
#    "right": "KEY_D",
#    "menu": "KEY_P"
#  }
# }
##

#!/usr/bin/env python

"""
Thanks to:
https://github.com/WiringPi/WiringPi/
http://little-scale.blogspot.ca/2007/07/nes-controller-to-arduino.html
http://blog.thestateofme.com/2012/08/10/raspberry-pi-gpio-joystick/
"""

import argparse
import uinput
import time
import atexit
import sys
import os
import json
import RPi.GPIO as GPIO

verbose = False

MENU_TIMER = 1
MENU_TIMER_WAIT = 50

# The controller button bit masks 
NES_RIGHT   = 0x01
NES_LEFT    = 0x02
NES_DOWN    = 0x04
NES_UP      = 0x08
NES_START   = 0x10
NES_SELECT  = 0x20
NES_B       = 0x40
NES_A       = 0x80

def main():
    # Get the config
    config = getConfig();

    # Set up pins
    setupNes(config)

    # Get the key mapping
    keyMapping = getKeyMapping(config['key_mapping'])

    # Set up the keyboard bindings
    device = uinput.Device(keyMapping.values())

    # Register the shutdown function
    atexit.register(cleanup)

    if verbose == True:
        sys.stdout.write('Ready...\n')

    while True:
        buttons = readNes(config)
        processButtonState(buttons, device, keyMapping)          
        time.sleep(0.01)    

##
# Retrieve and validate the command line parameters and intialize the config
#
# @return Dict
##
def getConfig():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Display verbose log messages', action="store_true")
    parser.add_argument('-if', type=str, required=True, help='The file in which to read the button and pin mappings', dest='input_file')
  
    input = parser.parse_args()

    verbose = input.verbose
    input_file = open(input.input_file)
  
    return json.load(input_file)

##
# Setup the NES GPIO ports
#
# @param Dict config The NES configuration dictionary
##
def setupNes(config):
    #Use Raspberry Pi board pin numbers
    GPIO.setmode(GPIO.BOARD)

    #data in, clock out, latch out
    GPIO.setup(config['data_pin'], GPIO.IN)
    GPIO.setup(config['clock_pin'], GPIO.OUT)
    GPIO.setup(config['latch_pin'], GPIO.OUT)

    GPIO.output(config['latch_pin'], GPIO.HIGH)
    GPIO.output(config['clock_pin'], GPIO.HIGH)

##
# Get the key mapping. This dictionary will map the presses on the NES
# controller to the keyboard presses
#
# @param Dict config The NES config dictionary
#
# @return Dict
##
def getKeyMapping(config):
    keyMapping = {}

    for index in config:
        keyMapping[index] = getattr(uinput, input[config])

    return keyMapping

##
# Read the state of the NES controller
#
# @param Dict config The NES config dictionary
#
# @return integer
##
def readNes(config):
    GPIO.output(config['latch_pin'], GPIO.LOW)
    GPIO.output(config['clock_pin'], GPIO.LOW)

    GPIO.output(config['latch_pin'], GPIO.HIGH)
    time.sleep(0.02)
    GPIO.output(config['latch_pin'], GPIO.LOW)

    value = GPIO.input(config['data_pin'])

    for i in range(0,7):
        GPIO.output(config['clock_pin'], GPIO.HIGH)

        #Shift it one bit over and add the data input state
        value = (value << 1) + GPIO.input(config['data_pin']) 
        GPIO.output(config['clock_pin'], GPIO.LOW)

    #Do a bitwise XOR
    return value ^ 0xFF 

##
# Send out keyboard presses
#
# @param integer buttons The bit string representing the buttons state
# @param Device device The keyboard Device object
# @param Dict keyMapping The mapping of NES presses to keyboard presses
##
def processButtonState(buttons, device, keyMapping):

    if (buttons & NES_A) != 0:   
        device.emit(keyMapping['a'], 1)
    else:
        device.emit(keyMapping['a'], 0)    

    if (buttons & NES_B) != 0:
        device.emit(keyMapping['b'], 1)
    else:
        device.emit(keyMapping['b'], 0)    
        
    if (buttons & NES_DOWN) != 0:
        device.emit(keyMapping['down'], 1)
    else:
        device.emit(keyMapping['down'], 0)    

    if (buttons & NES_UP) != 0:
        device.emit(keyMapping['up'], 1)
    else:
        device.emit(keyMapping['up'], 0)    

    if (buttons & NES_LEFT) != 0:  
        device.emit(keyMapping['left'], 1)
    else:
        device.emit(keyMapping['left'], 0)    

    if (buttons & NES_RIGHT) != 0:   
        device.emit(keyMapping['right'], 1)
    else:
        device.emit(keyMapping['right'], 0)    

    if (buttons & NES_START) != 0:
        startPressed = True
        device.emit(keyMapping['start'], 1)
    else:
        startPressed = False
        device.emit(keyMapping['start'], 0)      

    if (buttons & NES_SELECT) != 0:
        selectPressed = True
        device.emit(keyMapping['select'], 1)
    else:
        selectPressed = False
        device.emit(keyMapping['select'], 0)

    # Trigger an extra 'menu' event when start and select are held down
	# for a determined amount of time
    if (selectPressed == True and startPressed == True):
        global MENU_TIMER    

        MENU_TIMER += 1
			
        if (MENU_TIMER >= MENU_TIMER_WAIT):
            device.emit(keyMapping['menu'], 1)
    else:
        MENU_TIMER = 0
        device.emit(keyMapping['menu'], 0)

##
# Clear the state of the GPIO
##        
def cleanup():
    if verbose == True:
        sys.stdout.write('Cleaning up...')
    
    GPIO.cleanup()

if __name__ == "__main__":
    main()

