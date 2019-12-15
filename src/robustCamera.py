"""
Wrapper around the basic cv2 video camera function.
The idea is that this is a more robust version that can withstand camera hangups, restarts etc.
"""

import cv2
import time
import os
import glob

class RobustCamera(object):
	def __init__(self, videoStream, device_location, autoSearchCamera=False,debug=True):
		###Variable initializations
		self.videoStream = videoStream
		self.cap = None
		self.debug = debug
		self.device_location = device_location
		self.autoSearchCamera = autoSearchCamera

		self.VideoCapture(self.videoStream)

	def findCameraStream(self):
		largest = 0
		saved_stream = '/dev/video0'
		for stream in glob.glob("/dev/video?"):
			if self.debug:
				print("found camera stream: " + stream)
			if int(stream.split('video')[1]) > largest:

				largest = int(stream.split('video')[1])
				saved_stream = stream

		return saved_stream

	def resetDevicePorts(self): #need to test this before runnning. Think for now it's safer to manually specify the device location.
		for device in glob.glob("/sys/bus/usb/devices/1-?/authorized"):
			if self.debug:
				print("Found devices: ", device)
			command = "echo " + device + " > ./camera_device_location"
			os.system(command)
			os.system("sudo ./sh_scripts/deauthorize_device.sh")
			time.sleep(1)
			os.system("sudo ./sh_scripts/reauthorize_device.sh")

	def VideoCapture(self,videoStream, retry=True, timeOut=2):
		isSuccesful = False
		while not isSuccesful:
			try:
				if self.cap is not None:
					if self.debug:
						print("Releasing camera.")
					self.cap.release() #release the old camera first
					# self.resetDevicePorts() #this could have unintended consequences...like disconnecting the pcie bus or smth important. Test thoroughly first
					#Resetting the usb port #Only works in linux...so if you're using windows...yeah...
					#os.system("echo zxcvbnm, | sudo -S ./sh_scripts/deauthorize_device.sh")
					#set device location
					command = "echo " + self.device_location + " > ./camera_device_location"
					os.system(command)
					os.system("sudo ./sh_scripts/deauthorize_device.sh")
					time.sleep(1)
					os.system("sudo ./sh_scripts/reauthorize_device.sh")

					if self.debug:
						print("Ran shell, camera released.")

				if self.autoSearchCamera == True:
					self.videoStream = self.findCameraStream()

				self.cap = cv2.VideoCapture(self.videoStream)

				if self.cap.isOpened():
					isSuccesful = True
				else:
					raise Exception("Could not get camera stream")

				if self.debug:
					print("Initialized camera: ", self.videoStream)


			except Exception as e:
				print(e)
				if retry:
					print("Something went wrong. Pausing for " + str(timeOut) + " seconds, then restarting.")
					time.sleep(timeOut)
				else:
					raise Exception("Camera error. Retry is false.")

	def read(self, retry=True, timeOut = 2):
		if self.cap == None:
			#video stream hasn't been initialised
			self.VideoCapture(self.videoStream)
		ret = False

		while ret == False:
			if self.cap.isOpened():
				ret, frame = self.cap.read()

				if ret == False:
					print("Returned nothing from the camera stream")
					if retry:
						print("Reattempting in " + str(timeOut) + " seconds.")
						time.sleep(timeOut)
						self.VideoCapture(self.videoStream)
				else:
					return ret,frame
			else:
				print("Video is not open. Waiting " + str(timeOut) + " then retrying again.")
				time.sleep(timeOut)
				print("Timeout over. Restarting.")
				self.VideoCapture(self.videoStream)
