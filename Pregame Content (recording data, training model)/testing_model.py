import cv2
import time
import numpy as np
from keras import models
import imutils
import itertools
from jutsu_videos import jutsu
import game


# --------------------------------------------------
# Global Variables
# --------------------------------------------------
saved_model = "./VGG16_LR_0.0003_EPOCHS1_1571499473.7668839"
model = models.load_model(saved_model)
bg = None
calibrate = 30
WIDTH = 165
HEIGHT = 235
top, right, bottom, left = 195, 255, 430, 420  # far away


# ------
# Signs
# ------
bird = [1,0,0,0,0,0,0,0,0,0,0,0]
boar = [0,1,0,0,0,0,0,0,0,0,0,0]
dog = [0,0,1,0,0,0,0,0,0,0,0,0]
dragon = [0,0,0,1,0,0,0,0,0,0,0,0]
hare = [0,0,0,0,1,0,0,0,0,0,0,0]
horse = [0,0,0,0,0,1,0,0,0,0,0,0]
monkey = [0,0,0,0,0,0,1,0,0,0,0,0]
ox = [0,0,0,0,0,0,0,1,0,0,0,0]
ram = [0,0,0,0,0,0,0,0,1,0,0,0]
rat = [0,0,0,0,0,0,0,0,0,1,0,0]
serpent = [0,0,0,0,0,0,0,0,0,0,1,0]
tiger = [0,0,0,0,0,0,0,0,0,0,0,1]
signs = ['bird', 'boar', 'dog', 'dragon', 'hare', 'horse', 'monkey', 'ox', 'ram', 'rat', 'serpent', 'tiger']

# -----------------
# Jutsu Sequences
# -----------------
chidori = ('ox', 'hare', 'monkey')
fireball = ('horse', 'serpent', 'ram', 'monkey', 'boar', 'horse', 'tiger')


print('---CAMERA STARTING. DONT MOVE---')
for i in list(range(3))[::-1]:
    print(i+1)
    time.sleep(1)


# --------------------------------------------------------------------------------------------------------------
# Return all the permuatations of a list of lists
# --------------------------------------------------------------------------------------------------------------
def permutations(current_sequence):
    seq = current_sequence
    perm = list(itertools.product(*seq))

    return perm


# --------------------------------------------------------------------------------------------------------------
# Create the sequence of signs being made
# --------------------------------------------------------------------------------------------------------------
def create_sequence(current_sequence, predictions):
    seq = current_sequence
    pred = predictions
    seq.append(pred)

    return seq


# --------------------------------------------------------------------------------------------------------------
# After making a prediction, get the order list of predictions along with name and percent of top 3 predictions
# --------------------------------------------------------------------------------------------------------------
def top_three(labels, predictions):
    dict_pred = dict(zip(labels, predictions[0]))
    order_dict = {}
    top_signs = []
    top_percents = []
    for key, value in sorted(dict_pred.items(), key=lambda item: item[1]):
        order_dict.update({key: value})
    for i in range(3):
        top_signs.append(list(order_dict)[-(i+1)])
        top_percents.append(list(order_dict.values())[-(i+1)])

    return order_dict, top_signs, top_percents


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
    diff = cv2.absdiff(bg.astype("uint8"), image)  # find absolute difference between background and current frame
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


# -----------------
# MAIN FUNCTION
# -----------------
if __name__ == "__main__":
    # initialize weight for running average
    aWeight = 0.5

    camera = cv2.VideoCapture(0)
    num_frames = 0
    count = 0
    mean_cutoff = 70
    accumulated_predictions = [0,0,0,0,0,0,0,0,0,0,0,0]
    accumulated_predictions = np.array([accumulated_predictions], dtype='float64')
    data = []
    sequence = []
    predict = False
    game_count = 0
    top_signs = []

    while True:
        # get the current frame
        (grabbed, frame) = camera.read()

        # -------------------------
        # BUTTON CONTROLS (MOSTLY)
        # -------------------------
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break

        # If P is pressed, start or stop the tracking
        if keypress == ord("p"):
            predict = not predict

            if predict:
                print('---TRACKING STARTED. GET READY TO JUTSU---')
                for i in list(range(3))[::-1]:
                    print(i + 1)
                    time.sleep(1)

                game.tracking = True
                game.game_loop(sequence=len(sequence))
                print('---GO!---')

            if not predict:
                print('---PAUSED---')
                game.tracking = False
                game.game_loop()

        # ------------------------------------
        # COMPUTER VISION OPERATIONS ON FRAME
        # ------------------------------------
        frame = imutils.resize(frame, width=700)  # resize the frame
        frame = cv2.flip(frame, 1)  # flip the frame so that it is not the mirror view
        clone = frame.copy()  # clone the frame
        (height, width) = frame.shape[:2]  # get the height and width of the frame
        roi = frame[top:bottom, right:left]  # get the ROI
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  # convert the roi to grayscale
        gray = cv2.GaussianBlur(gray, (7, 7), 0)  # blur it

        # For the first "calibrate_frames" # of frames, obtain background via a running average
        if num_frames < calibrate:  # 30 = 1 seconds
            run_avg(gray, aWeight)
        # After a background is obtained, threshold/segment the hand/foreground
        else:
            # segment the hand region
            hand = segment(gray)

            # ------------------------------------
            # MAIN THRESHOLD AND PREDICTION PART
            # ------------------------------------
            if hand is not None:
                # if yes, unpack the thresholded image and segmented region
                (thresholded, segmented) = hand

                # display the threshold frame
                cv2.imshow("Threshold", thresholded)

                thresholded = np.stack((thresholded,) * 3, axis=-1)  # Give the binary frame 3 channels for the model

                # If the predict boolean if set to true
                if predict:

                    if game_count % 9 == 0:
                        game.game_loop(sequence=len(sequence), prediction=top_signs)

                    # -------------------------------------
                    # METHOD 1: PREDICTION EVERY 35 FRAMES
                    # -------------------------------------
                    # if num_frames % 35 == 0:  # 35ish frames per second
                    #     prediction = model.predict([np.reshape(thresholded, (1,HEIGHT,WIDTH,3))])
                    #     print("Prediction: ", prediction)

                    if len(sequence) > 10 or keypress == ord("n"):  # Reset sequence if too long or if n key is pressed
                        sequence = []
                        print('---SEQUENCE RESET---')
                        game.game_loop(sequence=len(sequence), prediction=top_signs)

                        for i in list(range(1))[::-1]:
                            time.sleep(1)
                        print('---GET READY---')
                        for i in list(range(1))[::-1]:
                            time.sleep(1)
                        print('---GO!---')

                    # ---------------------------------------
                    # METHOD 2: AVERAGE EVERY 50 PREDICTIONS
                    # ---------------------------------------
                    prediction = model.predict([np.reshape(thresholded, (1,HEIGHT,WIDTH,3))])
                    count += 1
                    accumulated_predictions += prediction

                    # When 'mean_cutoff' frames happens, compute the average prediction
                    if count % mean_cutoff == 0:
                        average_prediction = accumulated_predictions / mean_cutoff
                        accumulated_predictions = np.zeros_like(prediction)

                        # Grab the ordered list of predictions as well as top 3 signs and percents specifically
                        ordered, top_signs, percents = top_three(signs, average_prediction)
                        # print("Top 3 Signs: ", top_signs)

                        sequence = create_sequence(sequence, top_signs)
                        print("Sequence: ", sequence)
                        # print("Length: ", len(sequence))

                    perm = permutations(sequence)
                    # print("Permutation of Lists: ", perm)

                    if chidori in perm:
                        jutsu("jutsu_videos_original/Kakashi Raikiri's.mp4")
                        predict = False
                        sequence = []

                    if fireball in perm:
                        jutsu("jutsu_videos_original/fire style fire ball jutsu.mp4")
                        predict = False
                        sequence = []

                    game_count += 1

                        # # If we decide to use np.argmax again
                        #
                        #  if np.argmax(average_prediction) == np.argmax(bird):
                        #     print(signs[0])
                        # elif np.argmax(average_prediction) == np.argmax(boar):
                        #     print(signs[1])
                        # elif np.argmax(average_prediction) == np.argmax(dog):
                        #     print(signs[2])
                        # elif np.argmax(average_prediction) == np.argmax(dragon):
                        #     print(signs[3])
                        # elif np.argmax(average_prediction) == np.argmax(hare):
                        #     print(signs[4])
                        # elif np.argmax(average_prediction) == np.argmax(horse):
                        #     print(signs[5])
                        # elif np.argmax(average_prediction) == np.argmax(monkey):
                        #     print(signs[6])
                        # elif np.argmax(average_prediction) == np.argmax(ox):
                        #     print(signs[7])
                        # elif np.argmax(average_prediction) == np.argmax(ram):
                        #     print(signs[8])
                        # elif np.argmax(average_prediction) == np.argmax(rat):
                        #     print(signs[9])
                        # elif np.argmax(average_prediction) == np.argmax(serpent):
                        #     print(signs[10])
                        # elif np.argmax(average_prediction) == np.argmax(tiger):
                        #     print(signs[11])

        # ----------------------------------
        # AFTER THRESHOLD-PREDICTION PART
        # ----------------------------------
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)  # draws the box

        num_frames += 1

        # display the original camera frame (with red outline if applicable)
        cv2.imshow("Video Feed", clone)

    camera.release()
    cv2.destroyAllWindows()



# if np.argmax(prediction) == np.argmax(bird):
#     print(signs[0])
# elif np.argmax(prediction) == np.argmax(boar):
#     print(signs[1])
# elif np.argmax(prediction) == np.argmax(dog):
#     print(signs[2])
# elif np.argmax(prediction) == np.argmax(dragon):
#     print(signs[3])
# elif np.argmax(prediction) == np.argmax(hare):
#     print(signs[4])
# elif np.argmax(prediction) == np.argmax(horse):
#     print(signs[5])
# elif np.argmax(prediction) == np.argmax(monkey):
#     print(signs[6])
# elif np.argmax(prediction) == np.argmax(ox):
#     print(signs[7])
# elif np.argmax(prediction) == np.argmax(ram):
#     print(signs[8])
# elif np.argmax(prediction) == np.argmax(rat):
#     print(signs[9])
# elif np.argmax(prediction) == np.argmax(serpent):
#     print(signs[10])
# elif np.argmax(prediction) == np.argmax(tiger):
#     print(signs[11])

