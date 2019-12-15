"""
Wrapper around cv2 functions as a way to write datasets easily.
Intended for an external SSD or Harddrive.

You can choose:
	1. space for datasets (in Megabytes)
	2. Video mode or picture mode (default to picture mode)
	2. Length of a video
	3. Video encoding/decoding
	4. ffmpeg encoding (experimental)

Features:
- You can set how much space you want it to contain and it will automatically overwrite if it detects
it's too full.
- It will autoresume from the last found video device! Unless you set it not too!

Notes on Naming:
Video: it saves it as yourvideo_0, then yourvideo_1 etc. Basically, it taks on the _0, _1 etc.
Picture: It saves it as yourpicture_0, yourpicture_1 etc. Same as video really.
Pictures: Don't specify an extension, you set that in picExtension parameter. Default .jpg.
"""

import cv2
import os

class DatasetSaver():
	def __init__(self,
	             saveLocation,
	             codec=cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'),
	             fps=30,
	             resolution=(1280,720),
	             mode='picture',
	             framesPerVideo=1000,
	             maxPics=999999,
	             maxSpaceMb=1000,
	             picExtension='.jpg',
	             debug=True): #1gb default
		self.debug = debug
		self.mode = mode
		self.saveLocation = saveLocation
		self.maxSpace = float(maxSpaceMb)
		self.videoName = os.path.basename(self.saveLocation)
		self.pathName = os.path.dirname(self.saveLocation)
		self.currentFrame = 0
		self.framesPerVideo = framesPerVideo
		self.spaceUsed = 0
		self.codec = codec
		self.picExtension = picExtension
		self.fps = fps
		self.resolution = resolution
		self.averagePicSize = None

		self.lastSaved = self.determineLastSavePoint()
		if mode == 'video':
			self.lastSaved = self.lastSaved + 1 #don't want to overwrite the old one
			saveDir = self.getSaveDir()
			self.out = cv2.VideoWriter(saveDir, codec, fps, resolution)
			print("Initialised as video.")

		elif mode == 'picture':
			self.maxPics = maxPics

			if self.debug:
				print("Initialised as picture.")
		else:
			print("Invalid mode. Mode must be either 'picture' or 'video'.")
			raise NotImplementedError

	def getSaveDir(self):
		if self.debug:
			print("Getting directory: ")
			print(os.path.join(self.pathName, self.videoName + "_" + str(self.lastSaved)))
		return os.path.join(self.pathName, self.videoName + "_" + str(self.lastSaved))

	def determineLastSavePoint(self):
		dirs = os.listdir(self.pathName)
		currentGreatestVideoNum = 1
		for file in dirs:
			splitBaseName = file.split('_')
			baseName = splitBaseName[0] #remove it's extension, leaving only the base name
			if baseName != self.videoName:
				continue
			splitNumAndExt = os.path.splitext(splitBaseName[1])
			currentGreatestVideoNum = max(int(splitNumAndExt[0]), currentGreatestVideoNum)

		return currentGreatestVideoNum #so we don't overrwrite the old one but start a new one instead

	def isDirectoryFull(self): #"We just check if the current size < max size, but when we write the new image, it could exceed it. Only on the next check will it then trigger, and if it's resource constrained, might be too big"
		# size = os.path.size(self.pathName) #return size in bytes
		#Worried this might be a bit slow...It has to walk through every single directory.
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(self.pathName):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				# skip if it is symbolic link
				if not os.path.islink(fp):
					total_size += os.path.getsize(fp)
		sizeMB = total_size*0.000001 #convert to MB
		self.spaceUsed = sizeMB
		if sizeMB >= self.maxSpace:
			return True
		else:
			return False

	def isDirectoryFullFast(self, averagePicsToTake=10):
		#Fast implementation of isDirectoryFull
		#Basically counts the first x images
		#Then just multiplies that by the current number of last saved
		#Won't give you a super accurate number, but should be good enough
		#Assumes the directory is full of only pictures, as it'll take 10 random files
		#And sum those average
		if self.averagePicSize == None: #Most likely it's none because there's not enough pictures to take an average
			if len(os.listdir(self.pathName)) > averagePicsToTake: #check the number of pics
				numberOfPathsWalked = 0
				total_size = 0
				for dirpath, dirnames, filenames in os.walk(self.pathName):
					for f in filenames:
						fp = os.path.join(dirpath, f)
						# skip if it is symbolic link
						if not os.path.islink(fp):
							numberOfPathsWalked += 1
							total_size += os.path.getsize(fp)
						if numberOfPathsWalked >= averagePicsToTake:
							break
				self.averagePicSize = (total_size/averagePicsToTake) * 0.000001
			else: #not enough pics so just do it the slow way
				return self.isDirectoryFull()

		self.spaceUsed = self.averagePicSize * self.lastSaved
		if self.spaceUsed >= self.maxSpace:
			return True
		else:
			return False




	def resetVideoWriter(self):
		#Current video has the max number of frames, so make a new video writer, with an increment of 1
		self.lastSaved += 1 #increment the last saved position
		#then reset the video writer
		if self.out is not None:
			self.out.release()
		saveDir = self.getSaveDir()
		self.out = cv2.VideoWriter(saveDir, self.codec, self.fps, self.resolution)

	def write(self, frame):
		if self.mode == "video":
			#check first if it's full
			if self.isDirectoryFullFast() == False:
				if self.debug:
					print("Writing video to directory.")
				self.out.write(frame)
				self.currentFrame += 1

				if self.currentFrame > self.framesPerVideo:
					self.resetVideoWriter() # create a new file and save that instead
					self.currentFrame = 0

			else:
				print("Directory is full, Video will not be saved.")
				print("Current amount of space allocated: ", str(self.spaceUsed) + "Mb")

		elif self.mode == "picture":
			if (self.isDirectoryFullFast() == False) and (self.lastSaved <= self.maxPics): #last saved refers to the number designation after the pics are saved
				saveDir = self.getSaveDir()
				if self.debug:
					print("Writing pic to directory: ", saveDir)
				self.lastSaved += 1
				cv2.imwrite(saveDir + self.picExtension, frame)
			else:
				print("Directory is full, Images will not be saved.")
				print("Current amount of space allocated: ", str(self.spaceUsed) + "Mb. Max Space: " + str(self.maxSpace) + "MB")
				print("No of pics allocated: ", str(self.maxPics), " No of pics written: ", str(self.lastSaved - 1))

		else:
			raise Exception("Mode not set!")

	def release(self):
		if self.mode == 'video':
			self.out.release()





