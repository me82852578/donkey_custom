import numpy as np
import argparse
import cv2
import dlib
from imutils.video import VideoStream
import imutils
import time


def detector(image):
    frame = image 
    detector = dlib.fhog_object_detector('mysign.svm')
    detector_light = dlib.fhog_object_detector('mytraffic_light.svm')
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(frame, 0)
    rects_light = detector_light(frame, 0) 

    if len(rects) > 0:
        for rect in rects:
            (bX, bY, bW, bH) = (rect.left(), rect.top(), rect.right(), rect.bottom())
            if bX < 0:
                bX = 0
            if bY < 0:
                bY = 0
            if bW < 0:
                bW = 0
            if bH < 0:
                bH = 0

            cv2.rectangle(frame, (bX, bY), (bW, bH),(0, 255, 0), 5)



# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0).start()
time.sleep(2)
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # stack output images together
    blurred = np.hstack([
        # cv2.bilateralFilter(frame, 5, 21, 21),
        # cv2.bilateralFilter(frame, 7, 31, 31),
        # cv2.bilateralFilter(frame, 9, 41, 41)])
        cv2.bilateralFilter(frame, 50, 100, 100)])
    detector(blurred)
    cv2.imshow("Bilateral", blurred)

    # cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break


cv2.destroyAllWindows()
vs.stop()

