import cv2 as cv
import numpy as np
import time
from imutils.video import VideoStream
import imutils
import pickle
import dlib

#標準霍夫線變換
def line_detection(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    edges = cv.Canny(gray, 50, 150, apertureSize=3)  #apertureSize參數默認其實就是3
    cv.imshow("edges", edges)
    lines = cv.HoughLines(edges, 1, np.pi/180, 80)
    for line in lines:
        rho, theta = line[0]  #line[0]存儲的是點到直線的極徑和極角，其中極角是弧度表示的。
        a = np.cos(theta)   #theta是弧度
        b = np.sin(theta)
        x0 = a * rho    #代表x = r * cos（theta）
        y0 = b * rho    #代表y = r * sin（theta）
        x1 = int(x0 + 1000 * (-b)) #計算直線起點橫坐標
        y1 = int(y0 + 1000 * a)    #計算起始起點縱坐標
        x2 = int(x0 - 1000 * (-b)) #計算直線終點橫坐標
        y2 = int(y0 - 1000 * a)    #計算直線終點縱坐標    註：這裏的數值1000給出了畫出的線段長度範圍大小，數值越小，畫出的線段越短，數值越大，畫出的線段越長
        cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)    #點的坐標必須是元組，不能是列表。
    cv.imshow("image-lines", image)

#統計概率霍夫線變換
def line_detect_possible_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    edges = cv.Canny(gray, 50, 150, apertureSize=3)  # apertureSize參數默認其實就是3
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 60, minLineLength=30, maxLineGap=5)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    cv.imshow("line_detect_possible_demo",image)

def detector(image):
    frame = image 
    detector = dlib.fhog_object_detector('mysign.svm')
    detector_light = dlib.fhog_object_detector('mytraffic_light.svm')
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    rects_light = detector_light(gray, 0) 

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

            cv.rectangle(frame, (bX, bY), (bW, bH),(0, 255, 0), 5)

# src = cv.imread(‘E:/imageload/louti.jpg‘)
# print(src.shape)
# cv.namedWindow(‘input_image‘, cv.WINDOW_AUTOSIZE) 
# cv.imshow(‘input_image‘, src)

# line_detection(src)
# src = cv.imread(‘E:/imageload/louti.jpg‘) #調用上一個函數後，會把傳入的src數組改變，所以調用下一個函數時，要重新讀取圖片
# line_detect_possible_demo(src)
# cv.waitKey(0)
# cv.destroyAllWindows()



#vs = VideoStream(usePiCamera=True).start()
vs = VideoStream(src=0).start()
time.sleep(2)
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=750)

    # line_detection(frame)
    # frame = vs.read()
    detector(frame)
    line_detect_possible_demo(frame)
    #rgb = cv.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # cv.imshow("Frame", frame)
    key = cv.waitKey(5)
    if key == ord("q"):
        break
cv.destroyAllWindows()
vs.stop()