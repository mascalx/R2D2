#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time, random
from gpiozero import LED, Servo

servo_h = Servo(17) # Servo for horizontal motion
servo_v = Servo(18) # Servo for vertical motion
led_w = LED(22) # White leds
led_b = LED(23) # Blue led

led_w.off() # Turn off white leds
led_b.off() # Turn off blue led

servo_h.mid() # Center horizontally
servo_v.mid() # Center vertically

time.sleep(1) # Wait for positions

servo_h.value=None # Disconnect horizontal servo
servo_v.value=None # Disconnect vertical servo

#
# Simulate holographic projection
#

led_w.on() # Turn on white leds
t1 = time.time()
while ((time.time()-t1)<10): # 10 seconds cycle
    if (random.randint(0, 1)==0):
        led_b.off() # Turn off the blue led
    else:
        led_b.on() # Turn on the blue led
    #led_b.toggle()    
    #time.sleep(random.random()/10.0) # Waits a random value between 0 and 0.1 seconds
    
# Turns off all the leds    
led_b.off()
led_w.off()    