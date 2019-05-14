from imutils.video import VideoStream
from imutils import face_utils
from imutils import paths
import argparse
import imutils
import time
import dlib
import cv2
import numpy as np


detector = dlib.fhog_object_detector('mysign.svm')
detector_light = dlib.fhog_object_detector('mytraffic_light.svm')

# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0).start()
time.sleep(2)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    rects_light = detector_light(gray, 0) 

    if len(rects) > 0:

        text = "{} sign !!".format(len(rects))
        cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 2)
        for rect in rects:
            (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),(0, 255, 0), 3)

    if len(rects_light) > 0:

        text = "{} sign !!".format(len(rects))
        cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 2)
        for rect in rects_light:
            (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),(0, 255, 0), 3)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break


cv2.destroyAllWindows()
vs.stop()
