import cv2
from datetime import datetime, date
import imutils
import os

os.system("sudo /home/nvidia/setup_camera.sh")
succesful = False
while succesful == False:
	try:
		cap = cv2.VideoCapture('rtsp://admin:123456@169.254.132.241:554/h264/ch1/main/av_stream')
		succesful = True
	except Exception as e:
		print(e)
#cap = cv2.VideoCapture(0)
save_location = "/media/nvidia/09a28e6f-3e9d-4a62-82d2-06025c635678/videos/" #on ssd
start_count = 0
stop = False
min_area = 1000
show = False
#backgroundFrame = cv2.imread("backgroundImage.jpg")
for i in range(10000):
	if stop == True:
		break
	#cv2.VideoWriter_fourcc('H','2','6','4')
	current_frame_count = 0
	prev_frame = None #for motion detection

	#out = cv2.VideoWriter('video_' + str(start_count) + "_" + dt_string + '.avi',cv2.VideoWriter_fourcc('D','I','V','X'), 30, (1280,720))
	video_string_name = save_location + 'video_' + str(start_count) + '.avi'
	out = cv2.VideoWriter(video_string_name, cv2.VideoWriter_fourcc('D','I','V','X'), 30, (1280,720))
	print("Saving video " + str(start_count))
	saved_video_frames = 0

	while saved_video_frames < 1000: #
		#print('About to start the Read command')
		ret, frame = cap.read()
		if not ret:
			print("could not get camera stream")
			continue
		frame = cv2.resize(frame, (1280,720))
		hd_frame = frame.copy()
		height, width = frame.shape[:2]

		if current_frame_count == 0:
			prev_frame = frame #so that prev_frame is not none
			current_frame_count += 1
			continue

		frame = imutils.resize(frame, width=250)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#gray = cv2.GaussianBlur(gray, (21, 21), 0)

		prev_frame = imutils.resize(prev_frame, width=250)
		prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
		#prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

		frameDelta = cv2.absdiff(gray, prev_gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		prev_frame = frame.copy() #has to be before the rectangles are drawn, otherwise it will detect that as well

		detected_movement = False
		for c in cnts:
			if cv2.contourArea(c) < min_area:
				continue
			else:
				detected_movement = True
				print("Found contour of size: ", cv2.contourArea(c))

			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		if show:
			cv2.imshow("diff", frameDelta)
		#cv2.imshow("motion detection", frame)
		if detected_movement == True:
			print("saved: " + video_string_name + " frame:" + str(current_frame_count))
			#dt_string = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
			#cv2.putText(hd_frame, dt_string, (10, 30) ,cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 1)
			if show:
				cv2.imshow("Saved_frame", hd_frame)
			out.write(hd_frame)
			saved_video_frames += 1
			

		current_frame_count += 1

		if cv2.waitKey(1) & 0xFF == ord('q'):
			stop = True
			break

	start_count += 1
	out.release()

	# When your video is ready, just run the following command
	# You can actually just write the command below in your terminal only works with ubuntu 16.04
	#os.system("ffmpeg -i " + video_string_name + " -vcodec libx264 " + video_string_name)

cap.release()
cv2.destroyAllWindows()
