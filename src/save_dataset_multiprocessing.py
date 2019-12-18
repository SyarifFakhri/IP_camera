#TX2 is pretty slow so we gotta run multiprocessing, otherwise it hangs up
#Essentially the same as save_dataset.py

import dataset_config
from datasetSaver import DatasetSaver
from robustCamera import RobustCamera
from motionDetector import MotionDetector
import multiprocessing as mp
import cv2
import os
import sys

def frameGrabber(queue, quit):
	#os.system("sudo /home/nvidia/setup_camera.sh")

	cap = RobustCamera(1,autoSearchCamera=False,
	                   device_location=dataset_config.cam_device_location,
	                   debug=dataset_config.debug)

	while True:
		ret, frame = cap.read()
		frame = cv2.resize(frame, (1280, 720))
		if queue.full():
			continue
		else:
			queue.put(frame)

		if quit.is_set():
			break

	cap.release()
	sys.exit(1)


def frameProcessor(queue):
	#processes and deals with motion capture
	out = DatasetSaver("test/testPic",
	                   mode='picture',
	                   maxPics=1000,
	                   maxSpaceMb=20,
	                   debug=dataset_config.debug)
	detector = MotionDetector(minMovementArea=dataset_config.min_area,
	                          debug=dataset_config.debug)
	prev_frame = None

	while True:
		frame = queue.get(True) #True -> block until there is a frame in the queue

		if prev_frame is None:
			prev_frame = frame
			continue
		if detector.isMovement(prev_frame, frame):
			if dataset_config.show:
				cv2.imshow("Saved_Frame", frame)
			out.write(frame)

		prev_frame = frame

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	out.release() #Doesn't do anything since it's picture mode
	cv2.destroyAllWindows()


if __name__ == '__main__':
	print("Starting program")
	queue = mp.Queue(1) #shared queue to store pictures
	quit = mp.Event()

	grabber = mp.Process(target=frameGrabber, args=(queue,quit,))
	grabber.start()

	frameProcessor(queue)

	#on exit
	quit.set()
	grabber.terminate()
	print("Shutting down...")
