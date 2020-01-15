import cv2
import time
import numpy as np
from keras import models
import imutils
import itertools
from jutsu_videos import jutsu
import pygame


# -------------------------
# Global Variables Testing
# -------------------------
saved_model = "./VGG16_LR_0.0003_EPOCHS1_1571499473.7668839"
model = models.load_model(saved_model)
bg = None
calibrate = 30
WIDTH = 165
HEIGHT = 235
top, right, bottom, left = 195, 255, 430, 420  # far away
sequence = []

# ------------------------
# GLOBAL VARIABLES PYGAME
# ------------------------
display_width = 1500
display_height = 800
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
orange = (255,165,0)
headersize = 50
jutsusize = 30

tracking = False

pygame.init()
win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('NINJUTSUUUU')


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

# --------------------------------------------------------------------------------------------------------------
# PYGAME FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def display_images(location, image):
    img = pygame.image.load(image)
    win.blit(img, location)
    pygame.display.update()


def text_objects(text, font):
    textsurface = font.render(text, True, blue)
    return textsurface, textsurface.get_rect()


def message_display(text, location, size):
    font_text = pygame.font.Font('freesansbold.ttf', size)
    textsurf, textrect = text_objects(text, font_text)
    textrect.center = location
    win.blit(textsurf, textrect)

    pygame.display.update()
    # game_loop()


def track(text, location, size):
    message_display(text, location, size)


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


print('---CAMERA STARTING UP. DONT MOVE---')
for i in list(range(3))[::-1]:
    print(i+1)
    time.sleep(1)


# -----
# MAIN
# -----
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
    predict = False
    game_count = 0
    top_signs = []

    # ----------------------------
    # ----- MAIN WHILE LOOP -----
    # ----------------------------
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
                win.fill(orange)
                track(text='GET READY.', location=((display_width / 2), 30), size=headersize)
                for i in list(range(3))[::-1]:
                    print(i + 1)
                    time.sleep(1)

                win.fill(orange)
                # track(text='---GO!---.', location=((display_width / 2), 30), size=30)
                tracking = True
                # game.game_loop(sequence=len(sequence))

            if not predict:
                win.fill(orange)
                track(text='PAUSED', location=((display_width / 2), 30), size=headersize)
                tracking = False
                # game.game_loop()

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

        # For the first "calibrate" # of frames, obtain background via a running average
        if num_frames < calibrate:  # 30 = 1 seconds
            run_avg(gray, aWeight)
        # After a background is obtained, threshold/segment the hand/foreground
        else:
            # segment the hand region
            hand = segment(gray)

            # --------------------------------
            # THRESHOLD AND PREDICTION PART
            # --------------------------------
            if hand is not None:
                # if yes, unpack the thresholded image and segmented region
                (thresholded, segmented) = hand

                # display the threshold frame
                cv2.imshow("Threshold", thresholded)

                thresholded = np.stack((thresholded,) * 3, axis=-1)  # Give the binary frame 3 channels for the model

                # -------------------------
                # IF TRACKING IS HAPPENING
                # -------------------------
                if predict:
                    track('Lightning Blade: ' + str(chidori), location=(200,600), size=jutsusize-10)
                    track('Fire Style Jutsu: '+ str(fireball), location=(368,630), size=jutsusize-10)

                    # if game_count % 9 == 0:
                    #     game.game_loop(sequence=len(sequence), prediction=top_signs)

                    # -----------------------------------------------------------
                    # OBTAINING AVERAGE PREDICTIONS, SEQUENCES, AND PERMUTATIONS
                    # -----------------------------------------------------------
                    prediction = model.predict([np.reshape(thresholded, (1,HEIGHT,WIDTH,3))])
                    count += 1
                    accumulated_predictions += prediction

                    # Every 'mean_cutoff' # of frames, stop and compute the average prediction
                    if count % mean_cutoff == 0:
                        average_prediction = accumulated_predictions / mean_cutoff
                        accumulated_predictions = np.zeros_like(prediction)

                        # Grab the ordered list of predictions as well as top 3 signs and percents specifically
                        ordered, top_signs, percents = top_three(signs, average_prediction)

                        sequence = create_sequence(sequence, top_signs)
                        # print("Sequence: ", sequence)

                    perm = permutations(sequence)

                    # ----------------------------------
                    # MATCHING PERMUTATIONS WITH JUTSUS
                    # ----------------------------------
                    if chidori in perm:
                        jutsu("jutsu_videos_original/Kakashi Raikiri's.mp4")
                        predict = False
                        sequence = []

                    if fireball in perm:
                        jutsu("jutsu_videos_original/fire style fire ball jutsu.mp4")
                        predict = False
                        sequence = []

                    # --------------------------
                    # PYGAME MAIN LOOP SECTION
                    # --------------------------

                    header_position = ((display_width / 2), 30)
                    prompt_position = (display_width * ((len(sequence) + 1) / 6) - 150, 100)
                    jutsu_position = (display_width * (len(sequence) / 6) - 150, 200)
                    image_position = (display_width * (len(sequence) / 6) - 210, 250)

                    # PyGame Events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

                    if tracking:
                        print("Prompt P", prompt_position)
                        # Indicate to player to start weaving signs
                        track('---GO!---', location=header_position, size=headersize)

                        # Visual cue for which sign is being tracked currently. Stationary Cue.
                        # track(text=f'SIGN #{str(len(sequence) + 1)}', location=((display_width / 2), 100), size=30)
                        track(text=f'SIGN #{str(len(sequence) + 1)}',
                              location=prompt_position, size=jutsusize)  # Mobile Cue.

                        # Visual printing of top signs so far
                        if len(sequence) > 0 and top_signs is not None:
                            track(text=str(top_signs[0]), location=jutsu_position, size=jutsusize)

                            for s in top_signs:
                                try:
                                    if s == chidori[len(sequence)-1] or s == fireball[len(sequence)-1]:
                                        display_images(location=image_position, image='mightguythumbsup.jpg')
                                    # else:
                                    #     display_images((display_width * (len(sequence) / 8), 300), image='narutobadclone.jpg')
                                except Exception as e:
                                    pass

                            # display_images(((display_width / 2), (display_height / 2)), image='lightningblade1.png')

                    else:
                        track(text='PAUSED', location=header_position, size=headersize)

                    pygame.display.update()


                    # Reset sequence if it becomes too long or if the n key is pressed
                    if len(sequence) > 6 or keypress == ord("n"):
                        sequence = []
                        win.fill(orange)
                        # game.game_loop(sequence=len(sequence), prediction=top_signs)
                        if tracking:
                            track(text='SEQUENCE RESET. GET READY.', location=header_position, size=headersize)

                        for i in list(range(2))[::-1]:
                            time.sleep(1)
                        win.fill(orange)

                        track('---GO!---', location=header_position, size=headersize)
                        pygame.time.delay(100)

                        # Display a moving sign # prompt
                        track(text=f'SIGN #{str(len(sequence) + 1)}',
                              location=prompt_position, size=jutsusize)

                    game_count += 1

        # ----------------------------------
        # AFTER THRESHOLD-PREDICTION PART
        # ----------------------------------
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)  # draws the box

        num_frames += 1

        # display the original camera frame (with red outline if applicable)
        cv2.imshow("Video Feed", clone)

    camera.release()
    cv2.destroyAllWindows()


