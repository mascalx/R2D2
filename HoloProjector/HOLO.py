#!/usr/bin/env python
#-*- coding: utf-8 -*-

from gpiozero import LED, Servo
import time, random, threading

# Holographic Projector class

# Servos limits
MAXH = 1.0
MINH = -1.0
MAXV = 1.0
MINV = -1.0

# To create the object you can specify:
# - Horizontal servo pin (SH default GPIO 17)
# - Vertical servo pin (SV default GPIO 18)
# - White LEDS pin (LW default GPIO 22)
# - Blue LED pin (LB default GPIO 23)
# if one parameter is set to None it will not be created the correspondent output device
class HoloProjector(object):

    # Creates the new object
    def __init__(self,SH=17,SV=18,LW=22,LB=23):
        if not(SH is None): 
            self.servo_h = Servo(SH) # Servo for horizontal motion
        else:
            self.servo_h = None # No instance for the servo        
        if not(SV is None): 
            self.servo_v = Servo(SV) # Servo for vertical motion
        else:
            self.servo_v = None # No instance for the servo        
        if not(LW is None): 
            self.led_w = LED(LW) # White leds
        else:
            self.led_w = None # No instance for the LED        
        if not(LB is None): 
            self.led_b = LED(LB) # Blue led
        else:
            self.led_b = None # No instance for the LED        
            
        # Now let's start the simulation thread
        self.startprojection=False # Be sure to not start a simulation
        thread = threading.Thread(target=self._ProjectionB, args=())
        thread.daemon = True 
        thread.start()              
        
    # Turns off all the LEDs    
    def Off(self):
        if not(self.led_w is None): self.led_w.off() # Turn off white leds
        if not(self.led_b is None): self.led_b.off() # Turn off blue led
        
    # Turns on all the LEDs    
    def On(self):    
        if not(self.led_w is None): self.led_w.on() # Turn on white leds
        if not(self.led_b is None): self.led_b.on() # Turn on blue led
        
    # Turns on just the white LEDs    
    def White(self):    
        if not(self.led_w is None): self.led_w.on() # Turn on white leds
        if not(self.led_b is None): self.led_b.off() # Turn off blue led

    # Turns on just the blue LED    
    def Blue(self):    
        if not(self.led_w is None): self.led_w.off() # Turn off white leds
        if not(self.led_b is None): self.led_b.on() # Turn on blue led
     
    # Centers both servos
    def Center(self):
        if not(self.servo_h is None): self.servo_h.mid() # Center horizontally
        if not(self.servo_v is None): self.servo_v.mid() # Center vertically
        
    # Disconnects the servos from controller so they can be moved freely    
    def FreeServo(self):
        if not(self.servo_h is None): self.servo_h.value=None # Disconnects horizontal servo
        if not(self.servo_v is None): self.servo_v.value=None # Disconnects vertical servo
        
    # Sets vertical position (-1..+1). If free is True, then this servo will be disconnected (1 second wait). If False (default) than it will be kept locked into position.
    def Vertical(self,position,free=False):
        if (position<-1): position=-1
        if (position>1): position=1
        realpos = (((position - MINV) * (MAXV - MINV)) / 2) + MINV # Calculates position considering the servo limits
        if not(self.servo_v is None): 
            self.servo_v.value=realpos
            if (free):
                time.sleep(1)
                self.servo_v.value=None
        
    # Sets horizontal position (-1..+1). If free is True, then this servo will be disconnected (1 second wait). If False (default) than it will be kept locked into position.
    def Horizontal(self,position,free=False):
        if (position<-1): position=-1
        if (position>1): position=1
        realpos = (((position - MINH) * (MAXH - MINH)) / 2) + MINH # Calculates position considering the servo limits
        if not(self.servo_h is None): 
            self.servo_h.value=realpos
            if (free): 
                time.sleep(1)
                self.servo_h.value=None
        
    # Simulates holographic projection for a specific amount of time (default 10 seconds)
    # NOTE: this is a blocking function. Control returns to the main script only after the elapsed time!!!
    def Projection(self,duration=10):        
        self.White() # Turns on white LEDs
        t1 = time.time()
        if not(self.led_b is None): 
            while ((time.time()-t1)<duration):
                self.led_b.toggle()    
                time.sleep(random.random()/200.0) # Waits a random value between 0 and 0.05 seconds
        self.Off()

    # Simulates holographic projection for a specific amount of time (default 10 seconds)
    def StartProjection(self,duration=10):
        if (self.startprojection==False): # Starts the simulation only if not already in progress
            self.duration=duration # Set the duration of the simulation
            self.startprojection=True # Request the start of the simulation
    
    # Thread for simulation in background. Never call it directly, but use the above StartProjection() instead
    # NOTE: this is a test non-blocking function. Use at your own risk!!!
    def _ProjectionB(self):
        while True: # Loop forever
            if (self.startprojection==True): # Parameters becom True when asked for starting from elsewhere
                self.White() # Turns on white LEDs
                t1 = time.time()
                if not(self.led_b is None): 
                    while ((time.time()-t1)<self.duration): # Duratino is set elsewhere
                        self.led_b.toggle()    
                        time.sleep(random.random()/200.0) # Waits a random value between 0 and 0.1 seconds
                self.Off()
                self.startprojection=False # When simulation is finished then reset the request
