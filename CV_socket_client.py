import socket
import sys
import time
import os

from imutils.video import VideoStream
from imutils import paths
import argparse
import imutils
import dlib
import cv2
import numpy as np
#ip_path = '192.168.1.115'
#ip_path = '192.168.32.187'
# ip_path = '192.168.32.171'
#ip_path = '172.20.10.4'
ip_path = '192.168.32.187'

sserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sserver.connect((ip_path, 8001)) 
print('socket connected!')

detector = dlib.fhog_object_detector('mysign.svm')
detector_light = dlib.fhog_object_detector('mytraffic_light.svm')
vs = VideoStream(src=0).start()
time.sleep(2)
photo_step = 2
counter = 0
# scp_command = 'scp /home/pi/cust_func/mask_img/* andrew@192.168.1.115:/home/andrew/cust_func/mask_img'
#scp_command = 'scp /home/pi/cust_func/mask_img/* jay@172.20.10.4:/home/jay/cust_func/mask_img'
scp_command = 'scp /home/pi/cust_func/mask_img/* jay@192.168.32.187:/home/jay/cust_func/mask_img'
while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=300)
    frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    rects_light = detector_light(gray, 0)

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
        p = os.path.sep.join(['/home/pi/cust_func/mask_img', "{}.jpg".format(str(0).zfill(5))])

        if counter % photo_step == 0:     
            cv2.imwrite(p, cropped)
            os.system(scp_command)

            data = 'gogogo'
            sserver.sendall(bytes(data.encode('ascii')))
            counter += 1
            print('counter = ', counter)

        if counter > 5:
            counter = 0
            print('counter = ', counter)
        counter += 1

    elif len(rects_light) > 0:

        text = "{} sign !!".format(len(rects_light))
        cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 0, 255), 2)
        for rect in rects_light:
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
        p = os.path.sep.join(['/home/pi/cust_func/mask_img', "{}.jpg".format(str(0).zfill(5))])

        if counter % photo_step == 0:     
            cv2.imwrite(p, cropped)
            os.system(scp_command)

            data = 'gogogo'
            sserver.sendall(bytes(data, encoding='utf-8'))
            counter += 1
            print('counter01 = ', counter)

        if counter > 5:
            counter = 0
            print('counter02 = ', counter)
        counter += 1

    else:
        cv2.imshow("Frame", frame)
        # cdky.command_to_car(["/home/pi/jay_project/donkey_PWM.py {}".format('STOP')])

    key = cv2.waitKey(1)
    if key == ord("q"):
       break

cv2.destroyAllWindows()
vs.stop()
sserver.close()
