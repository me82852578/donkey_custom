import cv2 as cv
import time
from imutils.video import VideoStream
import imutils
import pickle
import cv2

vs = VideoStream(usePiCamera=True).start()
time.sleep(2)
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=750)
    #rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()
