import cv2
from robustCamera import RobustCamera

#print("Before URL")
#cap = cv2.VideoCapture('rtsp://admin:123456@169.254.132.241:554/h264/ch1/main/av_stream')
#cap = cv2.VideoCapture('rtsp://admin:123456@169.254.132.241:554/1')
#cap = cv2.VideoCapture("http://admin:123456@169.254.132.241/video.h264")
#print("After URL")

#cap = RobustCamera('rtsp://admin:123456@169.254.132.241:554/h264/ch1/main/av_stream')
cap = RobustCamera(0) #webcam stream

while True:
    #print('About to start the Read command')
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280,720))
    height, width = frame.shape[:2]
    #print("height:", height)
    #print("width:", width)
    #print('About to show frame of Video.')
    cv2.imshow("Capturing",frame)
    #print('Running..')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
