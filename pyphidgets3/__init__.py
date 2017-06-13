
"""Copyright 2010 Phidgets Inc.
This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
"""
from sys import stderr
from time import sleep
__author__ = 'Adam Stelmack'
__version__ = '2.1.8'
__date__ = 'May 17 2010'

from Phidgets.PhidgetException import  PhidgetException #PhidgetErrorCodes,
#from Phidgets.Events.Events import ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.Stepper import Stepper

def DisplayDeviceInfo(stepper):
    print("|------------|----------------------------------|--------------|------------|")
    print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
    print("|------------|----------------------------------|--------------|------------|")
    print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (stepper.isAttached(), stepper.getDeviceName(), stepper.getSerialNum(), stepper.getDeviceVersion()))
    print("|------------|----------------------------------|--------------|------------|")
    print("Number of Motors: %i" % (stepper.getMotorCount()))

def StepperAttached(e):
    attached = e.device
    print("Stepper %i Attached!" % (attached.getSerialNum()))
    print()

def StepperDetached(e):
    detached = e.device
    print("Stepper %i Detached!" % (detached.getSerialNum()))
    
def StepperError(stepper):
    try:
        source = stepper.device
        print("Stepper %i: Phidget Error %i: %s" % (source.getSerialNum(), stepper.eCode, stepper.description), file=stderr)
    except PhidgetException as e:
        stopmotion(stepper)
        print("Phidget Exception %i: %s" % (e.code, e.details), file=stderr)
        raise

def StepperCurrentChanged(e):
     source = e.device
     print("Stepper %i: Motor %i -- Current Draw: %6f" % (source.getSerialNum(), e.index, e.current))
    

def StepperInputChanged(e):
     source = e.device
     print("Stepper %i: Input %i -- State: %s" % (source.getSerialNum(), e.index, e.state))


def StepperPositionChanged(e):
     source = e.device
     print("Stepper %i: Motor %i -- Position: %f" % (source.getSerialNum(), e.index, e.position))


def StepperVelocityChanged(e):
     source = e.device
     print("Stepper %i: Motor %i -- Velocity: %f" % (source.getSerialNum(), e.index, e.velocity))

def phidgetOpener(stepper, sid):
    if stepper is None:
        return
    
    try:
        stepper.openPhidget()
    except PhidgetException as e:
        stopmotion(stepper)
        print("Phidget Exception %i: %s" % (e.code, e.details),file=stderr)
        raise

    print("Waiting for attach....")

    try:
        stepper.waitForAttach(10000)
    except PhidgetException as e:
        stopmotion(stepper)
        print("Phidget Exception %i: %s" % (e.code, e.details), file=stderr)
        raise
    else:
        DisplayDeviceInfo(stepper)
        
def StepperCreate():
    if Stepper is None:
        print('problem loading Phidgets Python module, motion disabled',file=stderr)
        return

    try:
        stepper = Stepper()
    except RuntimeError as e:
        stopmotion(stepper)
        raise 

    try:
        #logging example, uncomment to generate a log file
        #stepper.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")

        stepper.setOnAttachHandler(StepperAttached)
        stepper.setOnDetachHandler(StepperDetached)
        stepper.setOnErrorhandler(StepperError)
        stepper.setOnCurrentChangeHandler(StepperCurrentChanged)
        stepper.setOnInputChangeHandler(StepperInputChanged)
        stepper.setOnPositionChangeHandler(StepperPositionChanged)
        stepper.setOnVelocityChangeHandler(StepperVelocityChanged)


    except PhidgetException as e:
        stopmotion(stepper)
        print("Phidget Exception %i: %s" % (e.code, e.details), file=stderr)
        raise
        
    print("Opening phidget object....")

    return stepper

def moveMotors(stepper, vel, accel, pos,direction):
    timestep = 0.05
# %% The code that actually tells the motors where to go
    print("Set the current position as start position...")
    try:
        stepper.setCurrentPosition(0, 0)
        sleep(0.1)

        print("Set the motor as engaged...")
        stepper.setEngaged(0, True)
        sleep(0.1)

        stepper.setAcceleration(0, 87543)
        stepper.setVelocityLimit(0, 5000)  # TODO check reasonableness
        stepper.setCurrentLimit(0, 0.26)

        sleep(0.2)

        print("pointing axes to initial positions:")

        stepper.setTargetPosition(0, int(pos[0]))
        curr = stepper.getCurrentPosition(0)
        while curr < int(pos[0]):
            curr = stepper.getCurrentPosition(0)

        stepper.setTargetPosition(0, direction*9999999)

        for v in vel:
            stepper.setVelocityLimit(0, v)
            sleep(timestep - 0.01)
        sleep(0.2)

        print("Moving back to home position...")
        stepper.setVelocityLimit(0, 9999)
        stepper.setTargetPosition(0, 0)

        while stepper.getCurrentPosition(0) != 0:
            sleep(0.01)

    except PhidgetException as e:
        stopmotion(stepper)
        print("Phidget Exception %i: %s" % (e.code, e.details),file=stderr)
        raise

    try:
        stopmotion(stepper)
    except PhidgetException as e:
        raise RuntimeError("Phidget Exception %i: %s" % (e.code, e.details), file=stderr)

def stopmotion(stepper):
    stepper.setEngaged(0, False)
    sleep(0.01)
    stepper.closePhidget()
    