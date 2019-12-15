

#I split it into two filse to prevent repetition between save_dataset.py and save_dataset_multiprocessing.py

###Constant Declarations###
save_location = "/media/nvidia/09a28e6f-3e9d-4a62-82d2-06025c635678/videos/" #on ssd
min_area = 500
show = False #show's cv2 images
debug = False #debuge messages

cam_device_location = '/sys/bus/usb/devices/1-1/authorized' #location of the camera - can use dmesg to help you get this