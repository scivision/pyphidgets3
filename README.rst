=========================================
Phidgets servos for C and Python exmaples
=========================================

:author: Michael Hirsch, Ph.D.



Simple C example
=================
Allows overriding motor action, to avoid having to pull power cord if main program crashes.

    gcc simple.c -o simple -lphidget21

    ./simple steps serialnum

    where ``steps`` is the forward or reverse number of steps (signed integer)

    ``serialnum`` is the serial number of the controller to use (leaving blank autoselects)
