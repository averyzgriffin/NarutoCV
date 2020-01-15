import cv2
import time
import numpy as np
from keras import models
import imutils
import itertools
from jutsu_videos import jutsu as jt
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
display_width = 800
display_height = 400

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
orange = (255,165,0)
green = (0,255,0)

# tracking = False
player_turn = True
game = False
jutsu = True
Light = ('ox', 'ox')
selected_jutsu = Light


pygame.init()
win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('NINJUTSUUUU')


# ------
# Signs
# ------
signs = ['bird', 'boar', 'dog', 'dragon', 'hare', 'horse', 'monkey', 'ox', 'ram', 'rat', 'serpent', 'tiger']
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

# -----------------
# Jutsu Sequences
# -----------------
chidori = ('ox', 'hare', 'monkey')
fireball = ('horse', 'serpent', 'ram', 'monkey', 'boar', 'horse', 'tiger')






class VisualCue:

    box_color = (150, 150, 150)
    box_outline = (200, 200, 200)

    def __init__(self, msg, w, h, text_color, type, seq, x=None, y=None,):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r, self.g, self.b = text_color
        self.type = type
        self.sequence = sequence

        if self.type == 'header':
            self.font = pygame.font.Font("freesansbold.ttf", 80)
        elif self.type == 'prompt':
            self.font = pygame.font.Font("freesansbold.ttf", 40)
        elif self.type == 'jutsu':
            self.font = pygame.font.Font("freesansbold.ttf", 30)

    def get_x(self):
        if self.type == 'header':
            self.x = display_width // 2
        elif self.type == 'prompt':
            self.x = display_width * ((len(sequence) + 1) / 6) - 150
        elif self.type == 'jutsu':
            self.x = display_width * (len(sequence) / 6) - 150
        elif self.type == 'image':
            self.x = display_width * (len(sequence) / 6) - 210
        return self.x

    def get_y(self):
        if self.type == 'header':
            self.y = 30
        elif self.type == 'prompt':
            self.y = 100
        elif self.type == 'jutsu':
            self.y = 200
        elif self.type == 'image':
            self.y = 250
        return self.y

    def text_objects(self):
        textsurface = self.font.render(self.msg, True, (self.r, self.g, self.b))
        return textsurface, textsurface.get_rect()

    def create_text(self):
        self.x = self.get_x()
        self.y = self.get_y()
        textsurf, textRect = self.text_objects()
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
        return textsurf, textRect

    def create_cue(self):
        self.x = self.get_x()
        self.y = self.get_y()
        button = pygame.draw.rect(win, self.box_color, (self.x, self.y, self.w, self.h))
        text, rect = self.create_text()
        win.blit(text, rect)


# --------------------------------------------------------------------------------------------------------------
# PYGAME FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def display_images(location, image):
    img = pygame.image.load(image)
    win.blit(img, location)
    pygame.display.update()


def success():
    win.fill(orange)
    success_cue = VisualCue('SUCCESS!', display_width//2, display_height//2, blue, 'header', sequence)
    success_cue.create_cue()
    # jt(selected_jutsu.video)
    reset_game()


def failed():
    win.fill(black)
    fail_cue = VisualCue('WRONG JUTSU', 600, 400, red, 'header', sequence)
    fail_cue.create_cue()
    # jt(failure.video)
    reset_game()


def reset_game():
    pygame.display.update()

    sequence = []
    num_frames = 0
    count = 0
    accumulated_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    accumulated_predictions = np.array([accumulated_predictions], dtype='float64')
    predict = False
    top_signs = []
    jutsu_active = []
    selected_jutsu = None

    time.sleep(3)



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
# OPENCV FUNCTIONS USED TO PROCESS IMAGES
# --------------------------------------------------
def run_avg(image, aWeight):  # Find the running average over the background
    global bg

    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)


def segment(image, threshold=25):  # Segment the region of hand in the image
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


# -----------------------
# MAIN FUNCTION AND LOOP
# -----------------------
if __name__ == "__main__":
    # initialize weight for running average
    aWeight = 0.5

    camera = cv2.VideoCapture(0)
    num_frames = 0
    count = 0
    mean_cutoff = 70
    accumulated_predictions = [0,0,0,0,0,0,0,0,0,0,0,0]
    accumulated_predictions = np.array([accumulated_predictions], dtype='float64')
    # predict = False
    top_signs = []

    # ----------------------------
    # ----- MAIN WHILE LOOP -----
    # ----------------------------
    while True:
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            win.fill((150,0,50))
            pygame.display.update()

        while jutsu:

            (grabbed, frame) = camera.read()

            # -------------------------
            # BUTTON CONTROLS (MOSTLY)
            # -------------------------
            keypress = cv2.waitKey(1) & 0xFF
            if keypress == ord("q"):
                break

            # THIS WAS USED TO SWITCH BETWEEN PREDICT AND NON-PREDICT MODES. THIS SHOULD NOT BE NEEDED FOR ACTUAL GAME
            # If P is pressed, start or stop the tracking
            # if keypress == ord("p"):
            #     predict = not predict
            #
            #     if predict:
            #         win.fill(orange)
            #         track(text='GET READY.', location=((display_width / 2), 30), size=headersize)
            #         for i in list(range(3))[::-1]:
            #             print(i + 1)
            #             time.sleep(1)
            #
            #         win.fill(orange)
            #         track(text='---GO!---.', location=((display_width / 2), 30), size=30)
            #         tracking = True
            #         game.game_loop(sequence=len(sequence))

                # if not predict:
                #     win.fill(orange)
                #     track(text='PAUSED', location=((display_width / 2), 30), size=headersize)
                #     tracking = False
                #     game.game_loop()

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

            if num_frames < calibrate:  # Calibrate the background for 'calibrate' # of frames (30 frames = 1 seconds)
                run_avg(gray, aWeight)
            else:  # After a background is obtained, threshold/segment the hand/foreground
                hand = segment(gray)

                if hand is not None:
                    (thresholded, segmented) = hand
                    cv2.imshow("Threshold", thresholded) # display the threshold frame
                    thresholded = np.stack((thresholded,) * 3, axis=-1)  # Give the binary frame 3 channels for the model

                    # -------------------------
                    # MODEL PREDICTION SECTION
                    # -------------------------
                    # PREDICT SHOULD ALWAYS BE ACTIVE SO I COMMENTED IT OUT AND UNINDENTED EVERYTHING BELOW TO 'game_count'
                    # if predict:

                    # track('Lightning Blade: ' + str(chidori), location=(200,600), size=jutsusize-10)
                    # track('Fire Style Jutsu: '+ str(fireball), location=(368,630), size=jutsusize-10)

                    # -----------------------------------------------------------
                    # OBTAINING AVERAGE PREDICTIONS, SEQUENCES, AND PERMUTATIONS
                    # -----------------------------------------------------------
                    prediction = model.predict([np.reshape(thresholded, (1,HEIGHT,WIDTH,3))])
                    count += 1
                    accumulated_predictions += prediction

                    if count % mean_cutoff == 0:
                        average_prediction = accumulated_predictions / mean_cutoff
                        accumulated_predictions = np.zeros_like(prediction)
                        ordered, top_signs, percents = top_three(signs, average_prediction)
                        sequence = create_sequence(sequence, top_signs)

                    perm = permutations(sequence)

                    # ------------------------------------------
                    # MATCHING PERMUTATIONS WITH SELECTED JUTSU
                    # ------------------------------------------
                    # TODO CHIDORI AND FIREBALL NEED TO BE CHANGED TO A VARIABLE DEFINED BY WHAT USER SELECTED
                    # if chidori in perm:
                    #     jutsu("jutsu_videos_original/Kakashi Raikiri's.mp4")
                    #     predict = False
                    #     sequence = []

                    # if fireball in perm:  I'LL KEEP THIS HERE FOR REFERENCE
                    #     jutsu("jutsu_videos_original/fire style fire ball jutsu.mp4")
                    #     predict = False
                    #     sequence = []

                    # -----------------------------
                    # PYGAME VISUAL CUES FOR USER
                    # -----------------------------

                    # PyGame Events # TODO THIS SHOULD GO ON TOP
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

                    # if tracking: # AGAIN, IT SHOULD ALWAYS BE TRACKING SO WE ARE COMMENTING/UN-INDENTING THIS
                    # track('---GO!---', location=header_position, size=headersize)
                    begin = VisualCue(msg="GO!", w=200, h=100, text_color=green, type='header', seq=sequence)
                    begin.create_cue()

                    # Visual cue for which sign is being tracked currently. Stationary Cue.
                    # track(text=f'SIGN #{str(len(sequence) + 1)}', location=((display_width / 2), 100), size=30)
                    # Moving cue version
                    # track(text=f'SIGN #{str(len(sequence) + 1)}', location=prompt_position, size=jutsusize)
                    moving_cue = VisualCue(f"SIGN #{str(len(sequence) + 1)}", 200, 100, green, type='prompt', seq=sequence)
                    moving_cue.create_cue()

                    # Visual printing of top signs so far
                    if len(sequence) > 0 and top_signs is not None:
                        # track(text=str(top_signs[0]), location=jutsu_position, size=jutsusize)
                        prediction_cue = VisualCue(str(top_signs[0]), 80, 50, green, type='jutsu', seq=sequence)
                        prediction_cue.create_cue()

                        for s in top_signs:
                            try:
                                if s == chidori[len(sequence)-1] or s == fireball[len(sequence)-1]:
                                    display_images(location=(300,300), image='mightguythumbsup.jpg')
                                # else:
                                #     display_images((display_width * (len(sequence) / 8), 300), image='narutobadclone.jpg')
                            except Exception as e:
                                pass

                    # else:
                    #     track(text='PAUSED', location=header_position, size=headersize)

                    pygame.display.update()

                    # Reset.
                    # TODO WE DON'T WANT TO RESET THIS MODE ANYMORE. JUST SWITCH BACK TO GAME MODE AND CHANGE TURNS
                    # todo something like if jutsu is complete, show success then switch, if not then show fail then switch
                    # if len(sequence) > 6 or keypress == ord("n"):
                    #     todo reset_jutsumode()
                        # sequence = []
                        # win.fill(orange)
                        # if tracking:
                        #     track(text='SEQUENCE RESET. GET READY.', location=header_position, size=headersize)
                        # track('---GO!---', location=header_position, size=headersize)
                        # Display a moving sign # prompt
                        # track(text=f'SIGN #{str(len(sequence) + 1)}',
                        #       location=prompt_position, size=jutsusize)

                    if selected_jutsu in perm:
                        success()
                        jutsu = False
                        game = True
                        player_turn = False
                        break

                    elif len(sequence) >= len(selected_jutsu) and selected_jutsu not in perm:
                        failed()
                        jutsu = False
                        game = True
                        player_turn = False
                        break

                    elif keypress == ord("n"):
                        failed()
                        jutsu = False
                        game = True
                        player_turn = False
                        break

            # ----------------------------------
            # AFTER THRESHOLD-PREDICTION PART
            # ----------------------------------
            cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)  # draws the box

            num_frames += 1

            # display the original camera frame (with red outline if applicable)
            cv2.imshow("Video Feed", clone)

        print("Camera Release")
        camera.release()
        cv2.destroyAllWindows()


