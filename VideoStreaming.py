from __future__ import print_function

from FramePSec import FramePSec
from CamVideoStream import CamVideoStream
import numpy as np
import argparse

# import skimage.io as sio
# from skimage import external as etif
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())


# created a *threaded *video stream, allow the camera senor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = CamVideoStream(src=0).start()
fps = FramePSec().start()
grabbed, frame, timestamp, cnt, width, height = vs.read()
print('width: ' + str(width) + ', height: ' + str(height))
# loop over some frames...this time using the threaded stream
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output2.avi',fourcc,30,(width,height))#(1920,1080))
count = -1
Cap_Time = []
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	grabbed, frame, timestamp, cnt, width, height = vs.read()

	# print(grabbed)
	#frame = imutils.resize(frame, width=400)
	if grabbed and count != cnt:
		out.write(frame)
		# tif.save(frame,compress=0)
		# check to see if the frame should be displayed to our screen
		if args["display"] > 0:
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
		count = cnt
		Cap_Time.append(cnt)
		# update the FPS counter
		fps.update()
	# print("Obtained # of frame: {:.1f}".format(fps._numFrames))

fps.stop()
# stop the timer and display FPS information

cv2.destroyAllWindows()
# print(Cap_Time)

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
vs.stop()
out.release()

# # Save as tiff files
# cap = cv2.VideoCapture('output2.avi')
# with etif.tifffile.TiffWriter('temp.tif',imagej=True) as tif:
# 	while cap.isOpened():
# 		ret, img = cap.read()
#
# 		if ret:
# 			# Datatype conversion and make it as unit8 type
# 			imgdat = np.array(img, dtype=np.uint8)
#
# 			# Use only green channel
# 			imgdat[:,:,0] = 0
# 			imgdat[:,:,2] = 0
# 			tif.save(imgdat,compress=9)
#
# 			if cv2.waitKey(1) & 0xFF == ord('q'):
# 				break
# 		else:
# 			break
#
# cap.release()
# print("Finish convert as TIFF")
