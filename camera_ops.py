import cv2
import global_variables as glob_var
import imutils
from global_variables import top, right, bottom, left


def setup_camera():
    return cv2.VideoCapture(0)


def background_run_avg(image, aWeight):

    # initialize the background
    if glob_var.bg is None:
        glob_var.bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, glob_var.bg, aWeight)


def segment_hand_region(image, threshold=25):

    # find absolute difference between background and current frame
    diff = cv2.absdiff(glob_var.bg.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get the contours in the threshold image
    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return thresholded


def process_frame(frame):
    resize_frame = imutils.resize(frame, width=700)
    flip_frame = cv2.flip(resize_frame, 1)
    color_frame = flip_frame.copy()
    roi_frame = flip_frame[top:bottom, right:left]
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    blur_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)
    return blur_frame, color_frame
