#!/usr/bin/env python
#-*- coding: utf-8 -*-
# **********************************************************
# Small logic display driver for R2D2 using 1.8" TFT
# **********************************************************
# Copyright 2018 Mascal
version="0.1a"
# **********************************************************

import os, glob, subprocess, time, string, sys, datetime, serial
from random import randint
# Import for graphic display
import TFT as GLCD
import ImageFont
import Image
import ImageDraw

xstart=17 # Starting horizontal led position (increase by 17 for subsequents)
ystart=30 # Starting vertical led position (increase by 17 for subsequents)
ledsize=14 # Diameter of the leds

NORMAL = 0 # Standard display mode (2 colors)
MULTI = 1 # Multicolor display mode
ERROR = 2 # Error display mode
IMAGE = 3 # Image display mode

MODE = NORMAL

Colors=['off','r','g','b','c','y','w'] # Led colors arrray

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.1) # Serial port to receive commands from main RPi

# Write the text centered on the display  
def DisplayText(draw,x,y,txt,size,color):
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', size)
    width=draw.textsize(text,font=fnt)[0] # Width of text
    draw.text(((x-width/2),y),text,font=fnt,fill=color)
    del draw
    del font
    return
    
# Drives the specified led with color
# px should be 0..8, py should be 0..4
# color can be:
#   r : red
#   g : green
#   b : blue
#   c : cyan
#   y : yellow
#   w : white
#   off : led turned off (almost black)
def PutLed(draw,px,py,color):
    global xstart
    global ystart
    global ledsize
    icon = Image.open("img/led"+color+".png")
    draw.paste(icon,((py*ledsize)+ystart,(px*ledsize)+xstart),icon)    
    del icon
    return
    
# Main program
if __name__ == '__main__':
    # Setup the display    
    disp = GLCD.TFT()		# Create TFT LCD display class.
    disp.initialize()		# Initialize display.
    disp.clear()
    
    draw=Image.open("img/smalllogic.png") # Load the main led screen
    
    t=False
    while True:
        if (MODE==NORMAL):
            for i in range (0,randint(0,20)): # Change a random number of leds (from 0 to 20)
                x=randint(0,8) # For every led choose a random one (x)
                y=randint(0,4) # For every led choose a random one (y)
                if (randint(0,1)==0): # Select random color between Cyan and White
                    PutLed(draw,x,y,"c")
                else:
                    PutLed(draw,x,y,"w")
        if (MODE==MULTI):
            for i in range (0,randint(0,20)): # Change a random number of leds (from 0 to 20)
                x=randint(0,8) # For every led choose a random one (x)
                y=randint(0,4) # For every led choose a random one (y)
                PutLed(draw,x,y,Colors[randint(0,6)]) # Put a random color for current led
        if (MODE==ERROR):
            if (t==True): # Every odd cycle turn red the four corners (so they blink)
                PutLed(draw,0,0,'r')
                PutLed(draw,0,4,'r')
                PutLed(draw,8,0,'r')
                PutLed(draw,8,4,'r')
            else:    
                PutLed(draw,0,0,'off')
                PutLed(draw,0,4,'off')
                PutLed(draw,8,0,'off')
                PutLed(draw,8,4,'off')
        if (MODE==IMAGE):
            pass
        
        disp.display(draw) # Display the led screen
        
        t=not(t) # To detect odd/even cycles

        rcv = port.read() # Waits a char for 0.1 seconds
        if (rcv!=''): # Something arrived from serial. Lowest 2 bits : requested mode
            draw=Image.open("img/smalllogic.png") # Resets the led panel
            if ((rcv & 3)==0): # Normal mode requested. 2 colors leds
                MODE=NORMAL
            if ((rcv & 3)==1): # Multicolor mode requested. 7 colors leds
                MODE=MULTI
            if ((rcv & 3)==2): # Error mode requested. Error number in highest 6 bits (max 64 errors)
                MODE=ERROR
                draw=Image.open("img/ERR%03d.png" % (rcv >> 2)) # Loads the error to be shown
            if ((rcv & 3)==3): # Image mode requested. Image number in highest 6 bits (max 64 images)
                MODE=IMAGE
                draw=Image.open("img/IMG%03d.png" % (rcv >> 2)) # Loads the image to be shown
