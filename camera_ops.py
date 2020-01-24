import cv2
import global_variables as glob_var


# --------------------------------------------------
# OPENCV FUNCTIONS USED TO PROCESS IMAGES
# --------------------------------------------------
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

    # get the contours in the thresholded image
    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return thresholded, segmented
