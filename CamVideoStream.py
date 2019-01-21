# import the necessary packages
from threading import Thread
import datetime
import cv2

class CamVideoStream:
	def __init__(self, src=0, name="CamVideoStream"):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

		# set resolution at maximum
		HIGH_VALUE = 10000
		WIDTH = HIGH_VALUE
		HEIGHT = HIGH_VALUE
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

		self.width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
		self.height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
		# (self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False
		self.cnt = 0

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
			if self.grabbed:
				# self.cnt += 1
				self.cnt = datetime.datetime.now()
				# print(self.cnt)

	def read(self):
		# return the frame most recently read
		return self.grabbed, self.frame, self.cnt, self.width, self.height

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
