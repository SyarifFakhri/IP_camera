Description

# Description
Some useful utility scripts for cameras. Particularly saving datasets for machine learning.
Based around cv2 camera.

Note * Works best in linux

## Features

**Robust camera** 
- It'll automatically reconnect a camera if it disconnects
- Autosearch for the camera usb port
- Instead of crashing if it can't find a camera it'll attempt to reconnect, even if that involves
resetting all the USB ports

**Robust dataset saving**
- You can set it in video mode or picture mode
- You can set the maximum size in megabytes so it won't overflow
- It'll autoresume from the last save point
- Fast size search so it's not spending a lot of time just trying to read the size of the folder

**Motion detection** 
- Finds the difference in frames between the current and previous
- You can set a threshold of motion detection

**Multi threaded**
- Motion detection and saving happens on a different thread
- Uses Python multiprocessing instead of threading for true multiprocessing

## Examples
You can find example in test_ip_camera.py or save_dataset.py
Includes multiprocessing implementation in save_dataset_multiprocessing.py



