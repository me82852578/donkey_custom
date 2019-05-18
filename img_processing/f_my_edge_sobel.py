import cv2 as cv
import time
from imutils.video import VideoStream
import imutils
import pickle
import cv2
import dlib
import numpy as np


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

            cv2.rectangle(frame, (bX, bY), (bW, bH),(255, 255, 255), 5)



# vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0).start()
time.sleep(2)
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=750)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)


    lap = cv2.Laplacian(frame, cv2.CV_64F)
    lap = np.uint8(np.absolute(lap))
    # cv2.imshow("Laplacian", lap)
    # cv2.waitKey(0)

    # Sobel edge detection
    sobelX = cv2.Sobel(frame, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(frame, cv2.CV_64F, 0, 1)

    sobelX = np.uint8(np.absolute(sobelX))
    sobelY = np.uint8(np.absolute(sobelY))

    sobelCombined = cv2.bitwise_or(sobelX, sobelY)
    detector(sobelCombined)
    cv2.imshow("Frame", sobelCombined)
    key = cv2.waitKey(100)
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()
