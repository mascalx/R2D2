#!/usr/bin/env python
#-*- coding: utf-8 -*-

import HOLO,time

holo1=HOLO.HoloProjector(SH=17,SV=18,LW=22,LB=23) # Creates the object

holo1.Off() # Turns off all the LEDs

holo1.Center() # Centers the servos
time.sleep(1) # Waits for positions
holo1.FreeServo() # Frees the servos

holo1.StartProjection(10) # Simulates a 10 seconds holographic projection

time.sleep(11) # As we are using the threaded simulation, we need to stay inside the script for all the time to see the effect...
