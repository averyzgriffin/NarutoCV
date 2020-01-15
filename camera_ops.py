import cv2
import global_variables as gb


# --------------------------------------------------
# OPENCV FUNCTIONS USED TO PROCESS IMAGES
# --------------------------------------------------
def setup_camera():
    return cv2.VideoCapture(0)


def run_avg(image, aWeight):  # Find the running average over the background
    # global gb.bg

    # initialize the background
    if gb.bg is None:
        gb.bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, gb.bg, aWeight)


def segment(image, threshold=25):  # Segment the region of hand in the image
    # global gb.bg

    diff = cv2.absdiff(gb.bg.astype("uint8"), image)  # find absolute difference between background and current frame
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
