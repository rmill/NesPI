#!/usr/bin/env python


"""
Thanks to:
https://github.com/WiringPi/WiringPi/
http://little-scale.blogspot.ca/2007/07/nes-controller-to-arduino.html
http://blog.thestateofme.com/2012/08/10/raspberry-pi-gpio-joystick/

"""
import uinput
import time
import atexit
import sys
import os

import RPi.GPIO as GPIO



#Set pin numbers    
data_pin = 7
clock_pin = 3
latch_pin = 5



NES_RIGHT   = 0x01
NES_LEFT    = 0x02
NES_DOWN    = 0x04
NES_UP      = 0x08
NES_START   = 0x10
NES_SELECT  = 0x20
NES_B       = 0x40
NES_A       = 0x80



def main():
    

    

    #Set up pins
    setupNes()



    # Up, Down, left, right, A button, Z button
    
    events = (uinput.KEY_A, uinput.KEY_Z, uinput.KEY_P, uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT)

    device = uinput.Device(events)
    """
    # Bools to keep track of movement

    a_btn = False

    z_btn = False

    up = False

    down = False

    left = False

    right = False
    """

    atexit.register(cleanup)


    #sys.stdout.write('Ready...\n')


    


    while True:

        #Read button states
        button = readNes()

        

        if (button & NES_A) != 0:   
            device.emit(uinput.KEY_Z, 1)
        else:
            device.emit(uinput.KEY_Z, 0)    

        if (button & NES_B) != 0:
            device.emit(uinput.KEY_A, 1)
        else:
            device.emit(uinput.KEY_A, 0)    
        

        if (button & NES_DOWN) != 0:
            device.emit(uinput.KEY_DOWN, 1)
        else:
            device.emit(uinput.KEY_DOWN, 0)    

        if (button & NES_UP) != 0:
            device.emit(uinput.KEY_UP, 1)
        else:
            device.emit(uinput.KEY_UP, 0)    

        if (button & NES_LEFT) != 0:  
            device.emit(uinput.KEY_LEFT, 1)
        else:
            device.emit(uinput.KEY_LEFT, 0)    

        if (button & NES_RIGHT) != 0:   
            device.emit(uinput.KEY_RIGHT, 1)
        else:
            device.emit(uinput.KEY_RIGHT, 0)    

        if (button & NES_START) != 0:
            device.emit(uinput.KEY_P, 1)
        else:
            device.emit(uinput.KEY_P, 0)      

        if (button & NES_SELECT) != 0:
            #something
        else:
            #do something else             

 
        time.sleep(0.01)    

    

def setupNes():
    #Use Raspberry Pi board pin numbers
    GPIO.setmode(GPIO.BOARD)

    #data in, clock out, latch out
    GPIO.setup(data_pin, GPIO.IN)
    GPIO.setup(clock_pin, GPIO.OUT)
    GPIO.setup(latch_pin, GPIO.OUT)

    GPIO.output(latch_pin, GPIO.HIGH)
    GPIO.output(clock_pin, GPIO.HIGH)





def readNes():
    GPIO.output(latch_pin, GPIO.LOW)
    GPIO.output(clock_pin, GPIO.LOW)

    GPIO.output(latch_pin, GPIO.HIGH)
    time.sleep(0.02)
    GPIO.output(latch_pin, GPIO.LOW)
    #time.sleep(0.02)

    value = GPIO.input(data_pin)
    

    for i in range(0,7):
        GPIO.output(clock_pin, GPIO.HIGH)
        #time.sleep(0.02)

        
        #Shift it one bit over and add the data input state
        value = (value << 1) + GPIO.input(data_pin) 
        #time.sleep(0.04)
        GPIO.output(clock_pin, GPIO.LOW)

        
    #Do a bitwise XOR
    return value ^ 0xFF 




#Reset all the channels        
def cleanup():
    sys.stdout.write('Cleaning up...')
    GPIO.cleanup()


if __name__ == "__main__":
    main()
