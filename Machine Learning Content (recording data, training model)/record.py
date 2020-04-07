import cv2
import imutils
import numpy as np
import os
import time


count = 900   # where we left off training
# count = 120   # where we left off testing
sign = 'tiger'   # TODO
user = 'avery'  # TODO
folder_avery = 'E:/Artificial Intelligence/naruto/testing_data/testing_data_noisy_short/'  # TODO

sign_path = sign + r'/'
if user.lower() == 'avery':
    dir_output = folder_avery + sign_path

bg = None
record = False
calibrate = 300

# ROI coordinates
# top, right, bottom, left = 125, 175, 450, 425  # close up
# top, right, bottom, left = 235, 255, 470, 420  # far away
top, right, bottom, left = 195, 255, 430, 420  # far away

print('---CAMERA STARTING UP---')
for i in list(range(3))[::-1]:
    print(i+1)
    time.sleep(1)


def output(sign):
    signs = ['bird', 'boar', 'dog', 'dragon', 'hare', 'horse', 'monkey', 'ox', 'ram', 'rat', 'serpent', 'tiger']
    label = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    label[signs.index(sign)] = 1
    return label


# --------------------------------------------------
# To find the running average over the background
# --------------------------------------------------
def run_avg(image, aWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)


# ---------------------------------------------
# To segment the region of hand in the image
# ---------------------------------------------
def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get the contours in the threshold image
    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # (_, cnts, _) = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return thresholded, segmented


# -----------------
# MAIN FUNCTION
# -----------------
if __name__ == "__main__":
    # ------------
    # FILE PATH
    # ------------
    while True:
        if os.path.isfile(dir_output + 'handsign_' + str(count) + '.npy'):
            print("File exists, let's start a new file number!")
            count += 1
        else:
            print('File does not exist, starting fresh!')
            print("COUNT ", count)
            break

    # initialize weight for running average
    aWeight = 0.5

    camera = cv2.VideoCapture(0)
    num_frames = 0
    data = []

    while True:
        # get the current frame
        (grabbed, frame) = camera.read()

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break

        if keypress == ord("r"):
            print('---RECORDING STARTING---')
            for i in list(range(3))[::-1]:
                print(i+1)
                time.sleep(1)

            print("---Recording Started---")
            record = True

        # resize the frame
        frame = imutils.resize(frame, width=700)

        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < calibrate:  # 30 = 1 seconds
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the threshold image and
                # segmented region
                (thresholded, segmented) = hand

                # ----------------------
                # COLLECT AND SAVE DATA
                # ----------------------
                if record:
                    if keypress == ord("p"):
                        record = False
                        print("---Paused---")

                    label_ = output(sign=sign)
                    data.append([thresholded, label_])

                    if len(data) >= 100:
                        np.save(dir_output + 'handsign_' + str(count) + '.npy', data, allow_pickle=True)
                        print('FILE ', count, ' SAVED')
                        data = []
                        count += 1

                    if len(os.listdir(dir_output)) >= 5:
                        record = False
                        print("---Limit reached. Shutting down.---")
                        break


                # draw the segmented region and display the frame
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)

        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

    camera.release()
    cv2.destroyAllWindows()
