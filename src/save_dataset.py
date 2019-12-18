import cv2
from datetime import datetime, date
import imutils
import os
from datasetSaver import DatasetSaver
from robustCamera import RobustCamera
from motionDetector import MotionDetector

from dataset_config import save_location, min_area, show, debug


###Setting up IP camera
os.system("sudo /home/nvidia/setup_camera.sh")

#cap = cv2.VideoCapture('rtsp://admin:123456@169.254.132.241:554/h264/ch1/main/av_stream')
cap = RobustCamera(0)
out = DatasetSaver("test/testPics",  # should become test/testPic_0 etc
                   mode='picture',
                   maxPics=1000,
                   maxSpaceMb=100,
                   debug=debug)  # 100mb
detector = MotionDetector(minMovementArea=min_area,
                          debug=debug)

#backgroundFrame = cv2.imread("backgroundImage.jpg")
prev_frame = None  # for motion detection

while True:
	#out = cv2.VideoWriter('video_' + str(start_count) + "_" + dt_string + '.avi',cv2.VideoWriter_fourcc('D','I','V','X'), 30, (1280,720))
	#out = cv2.VideoWriter(video_string_name, cv2.VideoWriter_fourcc('D','I','V','X'), 30, (1280,720))

	ret, frame = cap.read()
	frame = cv2.resize(frame, (1280,720))
	#height, width = frame.shape[:2]

	if prev_frame is None:
		prev_frame = frame #so that prev_frame is not none
		continue
	#cv2.imshow("motion detection", frame)
	if detector.isMovement(prev_frame, frame):
		if show:
			cv2.imshow("Saved_frame", frame)
		out.write(frame)

	prev_frame = frame

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	# When your video is ready, just run the following command
	# You can actually just write the command below in your terminal only works with ubuntu 16.04
	#os.system("ffmpeg -i " + video_string_name + " -vcodec libx264 " + video_string_name)

cap.release()
cv2.destroyAllWindows()
