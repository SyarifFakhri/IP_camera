import imutils
import cv2
class MotionDetector():
	def __init__(self,
	             minMovementArea=500,
	             debug=True):
		self.minMovementArea = minMovementArea
		self.debug = debug
	def isMovement(self, prevFrame, currentFrame):
		"""Compares two frames and determines if there is movement"""
		frame = imutils.resize(currentFrame, width=250)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		prevFrame = imutils.resize(prevFrame, width=250)
		prevGray = cv2.cvtColor(prevFrame, cv2.COLOR_BGR2GRAY)

		frameDelta = cv2.absdiff(gray, prevGray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		if self.debug:
			cv2.imshow("diff", frameDelta)
			cv2.imshow("prevFrame", prevFrame)
			cv2.imshow("Current Frame", frame)
		for c in cnts:
			if cv2.contourArea(c) < self.minMovementArea:
				continue
			else:
				if self.debug:
					debugFrame = frame.copy()
					(x, y, w, h) = cv2.boundingRect(c)
					cv2.rectangle(debugFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
					cv2.imshow("detected", debugFrame)
					print("Found contour of size: ", cv2.contourArea(c))
				return True
		return False

