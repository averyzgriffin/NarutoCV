import cv2
import time
import numpy as np
import os


def video_frames(duration):

    # print('Ready to begin?')
    # for i in list(range(5))[::-1]:
    #     print(i)
    #     time.sleep(1)

    count = 1
    start = time.time()

    cap = cv2.VideoCapture(0)
    while True:
        current = time.time()
        elapse = round(current-start, 1)

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 2)
        thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 311, 2)
        thresh3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 411, 2)
        thresh4 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 511, 2)
        thresh5 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 611, 2)

        ret, bina = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        # ret1, bina1 = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY) # bad
        # ret2, bina2 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY) # bad
        # ret3, bina3 = cv2.threshold(gray, 127, 50, cv2.THRESH_BINARY) #dark but ok
        # ret4, bina4 = cv2.threshold(gray, 50, 100, cv2.THRESH_BINARY)
        # ret5, bina5 = cv2.threshold(gray, 175, 200, cv2.THRESH_BINARY)
        # canny = cv2.Canny(gray, 0, 100)

        # cv2.imshow('best one with 11,2', thresh)
        cv2.imshow('best one at 311,2', thresh2)
        cv2.imshow('411,2', thresh3)
        cv2.imshow('511,2', thresh4)
        cv2.imshow('611,2', thresh5)

        # print(elapse)
        # if elapse > duration:
        #     print('good bye')
        #     break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


video_frames(20)
