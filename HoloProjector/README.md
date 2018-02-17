# Holo projector

Scripts to drive the holoprojectors. HOLO.py contains the class for one hp. You need to specify gpios for the 2 servos and for white leds and blue led.

For the servos you should find the limits and change them at the beginnng of HOLO.py to make sure that you never go too far and broke the hp.

First test drives the hp without a class. Second test uses the class and the code it's a bit cleaner.

You can see some video of a test here:

https://youtu.be/bjU9V6c27Ko

https://youtu.be/rCtzolWliGY

Only requirement is the gpiozero library. The png image is the circuit schematic.

REMEMBER this is just a draft code. Please use at your own risk!
