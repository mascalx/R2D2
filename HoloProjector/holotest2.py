#!/usr/bin/env python
#-*- coding: utf-8 -*-

import HOLO,time

holo1=HOLO.HoloProjector(SH=17,SV=18,LW=22,BL=23) # Creates the object

holo1.Off() # Turns off all the LEDs

holo1.Center() # Centers the servos
time.sleep(1) # Waits for positions
holo1.FreeServo() # Frees the servos

holo1.Projection(10) # Simulates a 10 seconds holographic projection