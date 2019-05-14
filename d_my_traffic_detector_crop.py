import numpy as np
import cv2 as cv
from imutils.video import VideoStream
# from imutils import face_utils
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
    # vs = VideoStream(usePiCamera=True).start()
    vs = VideoStream(src=0).start()
    time.sleep(2)

    photo_step = 10
    counter = 0
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=600)
        frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)

        if len(rects) > 0:

            text = "{} sign !!".format(len(rects))
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 2)
            for rect in rects:
                # (bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
                (bX, bY, bW, bH) = (rect.left(), rect.top(), rect.right(), rect.bottom())
                # cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),(0, 255, 0), 1)
                if bX < 0:
                    bX = 0
                if bY < 0:
                    bY = 0
                if bW < 0:
                    bW = 0
                if bH < 0:
                    bH = 0

                cropped = frame[bY : bH, bX : bW]
                # obj_mask = np.zeros(frame.shape[:2], dtype = "uint8")
                # cv2.rectangle(obj_mask, (bX, bY), (bX + bW, bY + bH), 255, -1)
                # bitwiseAnd = cv2.bitwise_and(frame, frame, mask=obj_mask)

            cv2.imshow("Frame", cropped)


            p = os.path.sep.join(['/home/pi/jay_project/mask_img', "{}.jpg".format(str(counter).zfill(5))])

            if counter % photo_step == 0:     
                cv2.imwrite(p, cropped)
            if counter == 10:
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
