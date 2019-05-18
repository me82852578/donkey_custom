from imutils.video import VideoStream
from imutils import paths
import argparse
import imutils
import time
import cv2
import numpy as np


vs = VideoStream(usePiCamera=True).start()
# vs = VideoStream(src=0).start()
time.sleep(2)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break


cv2.destroyAllWindows()
vs.stop()
