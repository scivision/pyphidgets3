// - Stepper simple -
// This simple example sets up a Stepper object, hooks the event handlers and opens it for device connections.  
// Once an Advanced Servo is attached it will move the motor to various positions.
//
// Please note that this example was designed to work with only one Phidget Stepper connected. 
//
// Copyright 2008 Phidgets Inc.  All rights reserved.
// This work is licensed under the Creative Commons Attribution 2.5 Canada License. 
// view a copy of this license, visit http://creativecommons.org/licenses/by/2.5/ca/
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <phidget21.h>
//#include <unistd.h>

int CCONV AttachHandler(CPhidgetHandle stepper, void *userptr)
{
	int serialNo;
	const char *name;

	CPhidget_getDeviceName (stepper, &name);
	CPhidget_getSerialNumber(stepper, &serialNo);
	printf("%s %10d attached.\n", name, serialNo);

	return 0;
}

int CCONV DetachHandler(CPhidgetHandle stepper, void *userptr)
{
	int serialNo;
	const char *name;

	CPhidget_getDeviceName (stepper, &name);
	CPhidget_getSerialNumber(stepper, &serialNo);
	printf("%s %10d detached!\n", name, serialNo);

	return 0;
}

int CCONV ErrorHandler(CPhidgetHandle stepper, void *userptr, int ErrorCode, const char *Description)
{
	printf("Error handled. %d - %s\n", ErrorCode, Description);
	return 0;
}

int CCONV PositionChangeHandler(CPhidgetStepperHandle stepper, void *usrptr, int Index, __int64 Value)
{
	printf("Motor: %d > Current Position: %lld\r", Index, Value);
	return 0;
}

//Display the properties of the attached phidget to the screen.  We will be displaying the name, serial number and version of the attached device.
int display_properties(CPhidgetStepperHandle phid)
{
	int serialNo, version, numMotors;
	const char* ptr;

	CPhidget_getDeviceType((CPhidgetHandle)phid, &ptr);
	CPhidget_getSerialNumber((CPhidgetHandle)phid, &serialNo);
	CPhidget_getDeviceVersion((CPhidgetHandle)phid, &version);

	CPhidgetStepper_getMotorCount (phid, &numMotors);

	printf("%s\n", ptr);
	printf("Serial Number: %10d\nVersion: %8d\n# Motors: %d\n", serialNo, version, numMotors);

	return 0;
}

int stepper_simple(int pos, int serialnum)
{
	int result;
	__int64 curr_pos;
	const char *err;
	double minAccel, maxVel;
	int stopped;

	//Declare an stepper handle
	CPhidgetStepperHandle stepper = 0;

	//create the stepper object
	CPhidgetStepper_create(&stepper);

	//Set the handlers to be run when the device is plugged in or opened from software, unplugged or closed from software, or generates an error.
	CPhidget_set_OnAttach_Handler((CPhidgetHandle)stepper, AttachHandler, NULL);
	CPhidget_set_OnDetach_Handler((CPhidgetHandle)stepper, DetachHandler, NULL);
	CPhidget_set_OnError_Handler((CPhidgetHandle)stepper, ErrorHandler, NULL);

	//Registers a callback that will run when the motor position is changed.
	//Requires the handle for the Phidget, the function that will be called, and an arbitrary pointer that will be supplied to the callback function (may be NULL).
	CPhidgetStepper_set_OnPositionChange_Handler(stepper, PositionChangeHandler, NULL);

	//open the device for connections
	CPhidget_open((CPhidgetHandle)stepper, serialnum);

	//get the program to wait for an stepper device to be attached
	printf("Waiting for Phidget to be attached....\n");
	if((result = CPhidget_waitForAttachment((CPhidgetHandle)stepper, 10000)))
	{
		CPhidget_getErrorDescription(result, &err);
		printf("Problem waiting for attachment: %s\n", err);
		return EXIT_FAILURE;
	}

	//Display the properties of the attached device
	display_properties(stepper);

	//This example assumes stepper motor is attached to index 0

	//Set up some initial acceleration and velocity values
	CPhidgetStepper_getAccelerationMin(stepper, 0, &minAccel);
	CPhidgetStepper_setAcceleration(stepper, 0, minAccel*50);
	CPhidgetStepper_getVelocityMax(stepper, 0, &maxVel);
	CPhidgetStepper_setVelocityLimit(stepper, 0, maxVel/2);

	//display current motor position if available
	if(CPhidgetStepper_getCurrentPosition(stepper, 0, &curr_pos) == EPHIDGET_OK)
		printf("Motor: 0 > Current Position: %lld\n", curr_pos);


	//Step 1: Position 0 - also engage stepper
	printf("Set as home position and engage.\n");

	CPhidgetStepper_setCurrentPosition(stepper, 0, 0);
	CPhidgetStepper_setEngaged(stepper, 0, 1);

	//Step 2: Position request
	printf("Move to position %i. Press any key to Continue\n",pos);
	getchar();

	CPhidgetStepper_setTargetPosition (stepper, 0, pos);

	stopped = PFALSE;
	while(!stopped)
	{
		CPhidgetStepper_getStopped(stepper, 0, &stopped);
		usleep(10000);
	}

	CPhidgetStepper_setEngaged(stepper, 0, 0);


	//since user input has been read, this is a signal to terminate the program so we will close the phidget and delete the object we created
	printf("\nClosing...\n");
	CPhidget_close((CPhidgetHandle)stepper);
	CPhidget_delete((CPhidgetHandle)stepper);

	//all done, exit
	return EXIT_SUCCESS;
}

int main(int argc, char **argv)
{
    int pos = 0;
    int serialnum = -1;  // -1 means autoselect controller

    if (argc>1) 
        pos = atoi(argv[1]);

    if (argc>2)
        serialnum = atoi(argv[2]);

	stepper_simple(pos, serialnum);
	return 0;
}

