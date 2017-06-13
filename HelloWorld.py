#!/usr/bin/env python
"""
basic example of Phidgets stepper motor control
"""
vel=100
accel=100
steps=1000
direction=1
serialnum=    #set your serial number (integer) here

# %% Create a stepper object
stepper = StepperCreate()
# %% Open each stepper
phidgetOpener(stepper, serialnum)
# %% move motor
moveMotors(stepper,vel,accel,steps,direction)

