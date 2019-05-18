import numpy as np
import cv2 as cv
from imutils.video import VideoStream
from imutils import paths
import argparse
import imutils
import time
import dlib
import cv2
import numpy as np
import os
import command_donkey as cdky

def detector_strat():
    detector = dlib.fhog_object_detector('mysign.svm')
    vs = VideoStream(src=0).start()
    time.sleep(2)

    photo_step = 10
    counter = 0
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=800)
        frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       # frame = cv2.GaussianBlur(frame, (5, 5), 0)
       # frame = cv2.Canny(frame, 30, 150)
        rects = detector(gray, 0)

        if len(rects) > 0:

            text = "{} sign !!".format(len(rects))
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 2)
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

                cropped = frame[bY : bH, bX : bW]

            cv2.imshow("Frame", cropped)

            p = os.path.sep.join(['/home/pi/cust_func/data_img', "{}.jpg".format(str(counter).zfill(5))])

            if counter % photo_step == 0:     
                cv2.imwrite(p, cropped)
            if counter == 10000:
                counter = 0
            counter += 1

        else:
            cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    vs.stop()
if __name__ == '__main__':
   detector_strat()
