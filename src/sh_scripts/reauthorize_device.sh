#!/bin/bash
#shebang is important for python
#sudo sh -c 
#eg /sys/bus/usb/devices/1-1/authorized of camera authorization directory
CAMERA_LOCATION=$(<camera_device_location)
sudo echo 1 > $CAMERA_LOCATION
