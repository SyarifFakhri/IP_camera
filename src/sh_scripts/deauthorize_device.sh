#!/bin/bash
#the shebang is pretty important btw, you can't run in python without it.
#releases the usb device
#Obviously you have to find out where it is on the TX2 later
#sudo sh -c
CAMERA_LOCATION=$(<camera_device_location) #have to specify the whole directory cuz running it in python makes the current working directory the python directory
sudo echo 0 > $CAMERA_LOCATION
