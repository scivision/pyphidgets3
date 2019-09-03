# Phidgets servos for C and Python examples

Using Phidgets servo controllers from C and Python on Linux including Raspberry Pi.
**NOTE:** This was written for Phidgets 21, and has not been tested with the major updates in Phidgets 22.


## Python Phidgets

The Python helper code comes directly from Phidgets, and attempts to do
the opening and closing of drive connections without cluttering your
codebase.
Using it requires [Phidgets to be installed](https://www.scivision.dev/phidgets-motor-control-install-linux-python/).

## Detect drive controller connected

This is a test to indicate your drivers are installed and connected to
the controller:

```sh
cc HelloWorld.c -o HelloWorld -lphidget21

./HelloWorld
```

You will see when you plug or unplug the Phidgets controller(s) and get
their serial number(s).

## Simple C example

Allows overriding motor action, to avoid having to pull power cord if
main program crashes:

```sh
cc simple.c -o simple -lphidget21

./simple steps serialnum
```

where:

-   `steps` is the forward or reverse number of steps (signed integer)
-   `serialnum` is the serial number of the controller to use (leaving
    blank autoselects)
