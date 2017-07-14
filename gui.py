#!/usr/bin/env python
# original code by O. Doghmi
from tkinter import Tk, Label, Button, Place
#
from pyphidgets3 import StepperCreate,phidgetOpener,moveMotors


class baseGUI:
    def __init__(self, master):
        self.master = master
        master.title("Motor Control")


        self.label = Label(master, text="Select a Motor")
        self.label.pack()
        self.space = Label(master, text= "")
        self.space.pack()

#%% Button for Motor 0
        #self.label1 = Label(master, text="Motor 0")
        #self.label1.pack()
        self.motor_button = Button(master, text="Slit", width=15, command=self.ButtonClick0)
        self.motor_button.pack()

#%% Button for Motor 1
  #self.label2 = Label(master, text="Motor 0")
        #self.label2.pack()
        self.motor_button = Button(master, text="Grading Postion", width=15, command=self.message2)
        self.motor_button.pack()

#%% Button for Motor 2
        self.motor_button = Button(master, text="Spectrometer Focus", width=15, command=self.message3)
        self.motor_button.pack()

#%% Button for Motor 3
        self.motor_button = Button(master, text="Slit Focus", width=15, command=self.message4)
        self.motor_button.pack()

#%% Quitting program functionality
        self.close_button = Button(master, text="Close", width=15, command=master.quit)
        self.close_button.pack()

    def ButtonClick0(self):
        print("Motor 0 Selected")
        print("Executing...")

        # Motor 0 will now move
        # Note, StepperCreate, phidgetOpener, and moveMotors are located

        vel=   [380]  # no more than 383 for model 1062
        accel=10000
        steps=[2000]
        direction=1
        serialnum=-1
        #serialnum=321656

        # %% Create a stepper object
        stepper = StepperCreate()
        # %% Open each stepper
        phidgetOpener(stepper, serialnum)
        # %% move motor
        moveMotors(stepper,vel,accel,steps,direction)

        print("Motor 0 has moved")
        print("Terminating program...")

    def message2(self):
        print("Motor 1 Selected")

    def message3(self):
        print("Motor 2 Selected")

    def message4(self):
        print("Motor 3 Selected")


root = Tk()
my_gui = baseGUI(root)
root.mainloop()
