import time
import numpy as np
import imutils
import pygame
import cv2
import global_variables as gb
import game_ops
from game_ops import Jutsu
import visual_ops
from visual_ops import CharacterIcon, Button, VisualCue, Jutsu_Icon 
import predict_ops
import camera_ops
from keras import models


# ------------------------------------------------------------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------------------------------------------------------------

# Camera Variables
# bg = None
calibrate = 30
WIDTH = 165
HEIGHT = 235
top, right, bottom, left = 195, 255, 430, 420  # far away
aWeight = 0.5

# Model Prediction Variables
saved_model = "./VGG16_LR_0.0003_EPOCHS1_1571499473.7668839"
model = models.load_model(saved_model)
num_frames = 0
count = 0
mean_cutoff = 70
accumulated_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
accumulated_predictions = np.array([accumulated_predictions], dtype='float64')
top_signs = []
sequence = []
# gb.display_width = 1200
# gb.display_height = 800

# PyGame Variables
player_turn = True


pygame.init()
# win = pygame.display.set_mode((gb.display_width, gb.display_height))
# pygame.display.set_caption('NINJUTSUUUU')

# Jutsu Sign Variables
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

# # --------------------------------------------------------------------------------------------------------------
# # PYGAME FUNCTIONS
# # --------------------------------------------------------------------------------------------------------------
# def text_objects(text, font):
#     textsurface = font.render(text, True, black)
#     return textsurface, textsurface.get_rect()
#
#
# def message_display(text, location, size):
#     font_text = pygame.font.Font('freesansbold.ttf', size)
#     textsurf, textrect = text_objects(text, font_text)
#     textrect.center = location
#     win.blit(textsurf, textrect)
#
#     # pygame.display.update()
#     # game_loop()
#
#
# def track(text, location, size):
#     message_display(text, location, size)
#
#
# def prepare(jutsu):
#     procedure = VisualCue(msg=str(jutsu.get_sequence()), w=gb.display_width, h=50, text_color=black,
#                           typ=[], seq=sequence, x=0, y=gb.display_height * .75)
#
#     text_ = "You have selected: " + str(jutsu.icon_name)
#     font = pygame.font.Font("freesansbold.ttf", 50)
#
#     textsurf, textRect = text_objects(text_, font)
#     textRect.center = ((gb.display_width/2, 200))
#     win.blit(textsurf, textRect)
#
#     pygame.display.update()
#
#     time.sleep(3)
#     return procedure


# # --------------------------------------------------------------------------------------------------------------
# # JUTSU FUNCTIONS
# # --------------------------------------------------------------------------------------------------------------
# def success():
#     win.fill(orange)
#     success_cue = VisualCue('SUCCESS!', gb.display_width//2, gb.display_height//2, blue, 'header', sequence)
#     success_cue.create_cue()
#     jutsu_video = selected_jutsu.get_video_string()
#     play_video(jutsu_video)
#
#
# def failed():
#     win.fill(black)
#     fail_cue = VisualCue('WRONG JUTSU', 600, 200, red, 'header', sequence)
#     fail_cue.create_cue()
#     # jt(failure.video)
#
#
# def reset_game():
#     pygame.display.update()
#     num_frames, count = 0, 0
#     accumulated_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     accumulated_predictions = np.array([accumulated_predictions], dtype='float64')
#     sequence, top_signs, select, selected_jutsu, Jutsu_Icon.jutsu_que = [], [], [], [], []
#     game = True
#     jutsu = False
#     player_turn = False
#     time.sleep(3)
#
#     return sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu, game, jutsu, player_turn


# # --------------------------------------------------------------------------------------------------------------
# # MODEL + PREDICTION FUNCTIONS
# # --------------------------------------------------------------------------------------------------------------
# def permutations(current_sequence):
#     seq = current_sequence
#     perm = list(itertools.product(*seq))
#
#     return perm
#
#
# def create_sequence(current_sequence, predictions):
#     seq = current_sequence
#     pred = predictions
#     seq.append(pred)
#
#     return seq
#
#
# def top_three(labels, predictions):
#     dict_pred = dict(zip(labels, predictions[0]))
#     order_dict = {}
#     top_signs = []
#     top_percents = []
#     for key, value in sorted(dict_pred.items(), key=lambda item: item[1]):
#         order_dict.update({key: value})
#     for i in range(3):
#         top_signs.append(list(order_dict)[-(i+1)])
#         top_percents.append(list(order_dict.values())[-(i+1)])
#
#     return order_dict, top_signs, top_percents


# # --------------------------------------------------
# # OPENCV FUNCTIONS USED TO PROCESS IMAGES
# # --------------------------------------------------
# def setup_camera():
#     return cv2.VideoCapture(0)
#
#
# def run_avg(image, aWeight):  # Find the running average over the background
#     global bg
#
#     # initialize the background
#     if bg is None:
#         bg = image.copy().astype("float")
#         return
#
#     # compute weighted average, accumulate it and update the background
#     cv2.accumulateWeighted(image, bg, aWeight)
#
#
# def segment(image, threshold=25):  # Segment the region of hand in the image
#     global bg
#     diff = cv2.absdiff(bg.astype("uint8"), image)  # find absolute difference between background and current frame
#     # threshold the diff image so that we get the foreground
#     thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
#     # get the contours in the thresholded image
#     (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     # return None, if no contours detected
#     if len(cnts) == 0:
#         return
#     else:
#         # based on contour area, get the maximum contour which is the hand
#         segmented = max(cnts, key=cv2.contourArea)
#         return thresholded, segmented


# # ------------------------------------------------------------------------------
# # GAME CLASSES
# # ------------------------------------------------------------------------------
# class Button:
# 
#     font = pygame.font.Font("freesansbold.ttf", 20)
#     is_clicked = False
#     clickable = False
# 
#     def __init__(self, msg, x, y, w, h, color, alpha):
#         self.msg = msg
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#         self.r, self.g, self.b = color
#         self.alpha = alpha
# 
#     def create_text(self):
#         textsurf, textRect = text_objects(self.msg, self.font)
#         textRect.center = ( (self.x + (self.w/2)), (self.y +(self.h/2)) )
#         return textsurf, textRect
# 
#     def click_status(self):
#         if len(Jutsu_Icon.jutsu_que) > 0:
#             self.clickable = True
#         else:
#             self.clickable = False
#         return self.clickable
# 
#     def create_button(self):
#         clickable = self.click_status()
#         if clickable:
#             mouse = pygame.mouse.get_pos()
#             click = pygame.mouse.get_pressed()
#             if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
#                 button = pygame.Surface((self.w, self.h), pygame.SRCALPHA)  # per-pixel alpha
#                 button.fill((self.r, self.g, self.b, self.alpha))  # notice the alpha value in the color
#                 win.blit(button, (self.x, self.y))
# 
#                 if click[0] == 1:
#                     print('clicked')
#                     self.is_clicked = True
#             else:
#                 button = pygame.draw.rect(win, (self.r, self.g, self.b), (self.x, self.y, self.w, self.h))
# 
#             text, rect = self.create_text()
#             win.blit(text, rect)
# 
#         else:
#             button = pygame.Surface((self.w, self.h), pygame.SRCALPHA)  # per-pixel alpha
#             button.fill((self.r, self.g, self.b, self.alpha))  # notice the alpha value in the color
#             win.blit(button, (self.x, self.y))
#             text, rect = self.create_text()
#             win.blit(text, rect)
# 
# 
# class CharacterIcon:
# 
#     p1_x = 30
#     p2_x = gb.display_width * (7/8)
#     top_y = gb.display_height / 5
#     middle_y = gb.display_height * (2 / 5)
#     bottom_y = gb.display_height * (3 / 5)
# 
#     icon_size = (120, 120)
# 
#     def __init__(self, icon_name, player_num, icon_num):
#         self.icon_name = icon_name
#         self.player_num = player_num
#         self.icon_num = icon_num
# 
#     def get_x(self):
#         if self.player_num == 1:
#             x_location = self.p1_x
#         elif self.player_num == 2:
#             x_location = self.p2_x
#         else:
#             return "invalid PLAYER number provided to Class Icon get_x method"
#         return x_location
# 
#     def get_y(self):
#         if self.icon_num == 1:
#             y_location = self.top_y
#         elif self.icon_num == 2:
#             y_location = self.middle_y
#         elif self.icon_num == 3:
#             y_location = self.bottom_y
#         else:
#             return "invalid ICON number provided to Class Icon get_y method"
#         return y_location
# 
#     def get_image_from_string(self):
#         try:
#             path = self.icon_name + ".jpg"
#             img = pygame.image.load(path)
#         except Exception as e:
#             try:
#                 path = self.icon_name + ".png"
#                 img = pygame.image.load(path)
#             except Exception as e:
#                 return f"Couldn't find png either for {self.icon_name}."
#         return img
# 
#     def resize_image(self):
#         img = self.get_image_from_string()
#         resized = pygame.transform.scale(img, self.icon_size)
#         return resized
# 
#     def display_image(self):
#         x, y = self.get_x(), self.get_y()
#         img = self.resize_image()
#         win.blit(img, (x, y))
# 
# 
# class Jutsu_Icon(CharacterIcon):
# 
#     icon_size = (80,80)
#     x_offset = gb.display_width // 12
#     jutsu_que =[]
# 
#     def __init__(self, icon_name, player_num, icon_num, parent_icon):
#         super().__init__(icon_name, player_num, icon_num)
#         self.parent_icon = parent_icon
# 
#     def get_x(self):
#         x_p = self.parent_icon.get_x()
#         if self.player_num == 1:
#             x_p += 30
#             x = x_p + (self.x_offset * self.icon_num)
#         elif self.player_num == 2:
#             x = x_p - (self.x_offset * self.icon_num)  # mirror effect
#         else:
#             return "invalid player number provided to jutsu_get_x"
#         return x
# 
#     def get_y(self):
#         y_p = self.parent_icon.get_y()
#         y = y_p + 20
#         return y
# 
#     def display_image(self):
#         x, y = self.get_x(), self.get_y()
#         img = self.resize_image()
# 
#         # Button interactability
#         mouse = pygame.mouse.get_pos()
#         click = pygame.mouse.get_pressed()
#         size = self.icon_size[0]
# 
#         if (x + size) > mouse[0] > x and (y + size) > mouse[1] > y:
#             img = img.convert()
#             img.set_alpha(100)
# 
#             if click[0] == 1:
#                 # que up jutsu
#                 self.jutsu_que.append(self)
#                 print('jutsu icon clicked')
# 
#         win.blit(img, (x, y))
# 
# 
# 
# 
# # ----------------
# # JUTSU CLASSES
# # ----------------
# class VisualCue:
# 
#     box_color = (150, 150, 150)
#     box_outline = (200, 200, 200)
# 
#     def __init__(self, msg, w, h, text_color, typ, seq, x=None, y=None, image_str=None):
#         self.msg = msg
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#         self.r, self.g, self.b = text_color
#         self.typ = typ
#         self.seq = seq
#         self.image_str = image_str
# 
#         if self.typ == 'header':
#             self.font = pygame.font.Font("freesansbold.ttf", 80)
#         elif self.typ == 'prompt':
#             self.font = pygame.font.Font("freesansbold.ttf", 40)
#         elif self.typ == 'jutsu':
#             self.font = pygame.font.Font("freesansbold.ttf", 30)
#         else:
#             self.font = pygame.font.Font("freesansbold.ttf", 50)
# 
#     def get_x(self):
#         if self.typ == 'header':
#             self.x = gb.display_width // 2 - (self.w // 2)
#         elif self.typ == 'prompt':
#             self.x = gb.display_width * ((len(self.seq) + 1) / 6) - 150
#         elif self.typ == 'jutsu':
#             self.x = gb.display_width * (len(self.seq) / 6) - 100
#         elif self.typ == 'image':
#             self.x = gb.display_width * (len(self.seq) / 6) - 120
#         return self.x
# 
#     def get_y(self):
#         if self.typ == 'header':
#             self.y = 20
#         elif self.typ == 'prompt':
#             self.y = 130
#         elif self.typ == 'jutsu':
#             self.y = 240
#         elif self.typ == 'image':
#             self.y = 290
#         return self.y
# 
#     def text_objects(self):
#         textsurface = self.font.render(self.msg, True, (self.r, self.g, self.b))
#         return textsurface, textsurface.get_rect()
# 
#     def create_text(self):
#         if self.x is None:
#             self.x = self.get_x()
#         if self.y is None:
#             self.y = self.get_y()
#         textsurf, textRect = self.text_objects()
#         textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
#         return textsurf, textRect
# 
#     def display_image(self):
#         location = (self.get_x(), self.get_y())
#         img = pygame.image.load(self.image_str)
#         win.blit(img, location)
# 
#     def create_cue(self):
#         if self.x is None:
#             self.x = self.get_x()
#         if self.y is None:
#             self.y = self.get_y()
#         button = pygame.draw.rect(win, self.box_color, (self.x, self.y, self.w, self.h))
#         text, rect = self.create_text()
#         win.blit(text, rect)

# class Jutsu:
#
#     def __init__(self, icon, parent_icon, attacking_player):
#         self.icon = icon
#         self.parent_icon = parent_icon
#         self.attacking_player = attacking_player
#         self.icon_name = icon.icon_name
#         self.parent_name = parent_icon.icon_name
#
#     def get_sequence(self):
#         for item in chars_signs:
#             if list(item.values())[0] == self.parent_name:  # Take note of the list(items.values())[0]
#                 return item[self.icon_name]
#             else:
#                 return "Character not found in chars list from jutsu_signs"
#
#     def get_video_string(self):
#         for item in chars_vids:
#             if list(item.values())[0] == self.parent_name:
#                 return item[self.icon_name]
#             else:
#                 return "Character not found in chars dictionary from jutsu_videos"


# ----------------------------------------------------------------------------------------
# GAME OBJECTS INSTANTIATION
# ----------------------------------------------------------------------------------------
icon_1 = CharacterIcon('kakashi', 1, 1, win=gb.win)
icon_2 = CharacterIcon('obito', 1, 2, win=gb.win)
icon_3 = CharacterIcon('guy', 1, 3, win=gb.win)
icon_4 = CharacterIcon('crow', 2, 1, win=gb.win)
icon_5 = CharacterIcon('ramenguy', 2, 2, win=gb.win)
icon_6 = CharacterIcon('naruto', 2, 3, win=gb.win)

jutsu_icon1 = Jutsu_Icon(icon_name='kakashisharingan', player_num=1, icon_num=1, parent_icon=icon_1, win=gb.win)
jutsu_icon2 = Jutsu_Icon('ninjahounds', 1, 2, icon_1, win=gb.win)
jutsu_icon3 = Jutsu_Icon('lightningblade', 1, 3, icon_1, win=gb.win)
jutsu_icon4 = Jutsu_Icon('hiding', 1, 4, icon_1, win=gb.win)

jutsu_icon5 = Jutsu_Icon(icon_name='tobichains', player_num=1, icon_num=1, parent_icon=icon_2, win=gb.win)
jutsu_icon6 = Jutsu_Icon('tobiabsorb', 1, 2, icon_2, win=gb.win)
jutsu_icon7 = Jutsu_Icon('summoning9tails', 1, 3, icon_2, win=gb.win)
jutsu_icon8 = Jutsu_Icon('rin', 1, 4, icon_2, win=gb.win)

jutsu_icon9 = Jutsu_Icon(icon_name='guyleafwhirlwind', player_num=1, icon_num=1, parent_icon=icon_3, win=gb.win)
jutsu_icon10 = Jutsu_Icon('counterpunch', 1, 2, icon_3, win=gb.win)
jutsu_icon11 = Jutsu_Icon('sixthgate', 1, 3, icon_3, win=gb.win)
jutsu_icon12 = Jutsu_Icon('guydodge', 1, 4, icon_3, win=gb.win)
 
jutsu_icon13 = Jutsu_Icon(icon_name='rasengan', player_num=2, icon_num=1, parent_icon=icon_6, win=gb.win)
jutsu_icon14 = Jutsu_Icon('shadowclones', 2, 2, icon_6, win=gb.win)
jutsu_icon15 = Jutsu_Icon('chakraboost', 2, 3, icon_6, win=gb.win)
jutsu_icon16 = Jutsu_Icon('shadowsave', 2, 4, icon_6, win=gb.win)

attack_button = Button("ATTACK", gb.display_width/2, 50, 150, 75, (150,150,150), 100, win=gb.win)


# ----------------------------------------
# MAIN
# -----------------------------------------
if __name__ == "__main__":

    game = True
    jutsu = False

    # aWeight = 0.5
    # num_frames = 0
    # count = 0
    # mean_cutoff = 70
    # accumulated_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # accumulated_predictions = np.array([accumulated_predictions], dtype='float64')
    # top_signs = []
    while True:

        while game:
            print("Game: ", Jutsu_Icon.jutsu_que)

            # ----------------
            # CONSTANT SECTION
            # ----------------
            # PyGame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # ------------
                # KEY PRESSES
                # ------------
                if event.type == pygame.KEYDOWN:
                    print('keydown')

                    # Change modes
                    if event.key == pygame.K_j:
                        # active_jutsu = get_jutsu(Jutsu_Icon.jutsu_que):
                        Jutsu_Icon.jutsu_que = []
                        game = False
                        jutsu = True

                    # Press enter to end turn
                    if event.key == pygame.K_RETURN and Jutsu_Icon.jutsu_que != None:
                        player_turn = not player_turn

                    # if player_turn:
                    # elif not player_turn:

            # Background
            gb.win.fill(gb.orange)

            icon_1.display_image()
            icon_2.display_image()
            icon_3.display_image()
            icon_4.display_image()
            icon_5.display_image()
            icon_6.display_image()

            jutsu_icon1.display_image()
            jutsu_icon2.display_image()
            jutsu_icon3.display_image()
            jutsu_icon4.display_image()
            jutsu_icon5.display_image()
            jutsu_icon6.display_image()
            jutsu_icon7.display_image()
            jutsu_icon8.display_image()
            jutsu_icon9.display_image()
            jutsu_icon10.display_image()
            jutsu_icon11.display_image()
            jutsu_icon12.display_image()
            jutsu_icon13.display_image()
            jutsu_icon14.display_image()
            jutsu_icon15.display_image()
            jutsu_icon16.display_image()

            attack_button.create_button()

            if attack_button.is_clicked:
                gb.win.fill((255, 255, 255))
                select = Jutsu_Icon.jutsu_que[0]
                selected_jutsu = Jutsu(icon=select, parent_icon=select.parent_icon, attacking_player=player_turn)
                procedure = visual_ops.prepare(selected_jutsu, gb.win)
                gb.win.fill(gb.white)
                attack_button.is_clicked = False
                camera = camera_ops.setup_camera()
                game = False
                jutsu = True

            # ----------------------------------------------------
            # Final Update
            pygame.display.update()





        # -------------------------------------
        # COMPUTER VISION & HAND SIGNS SECTION
        # -------------------------------------
        while jutsu:

            procedure.create_cue()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            (grabbed, frame) = camera.read()

            # -------------------------
            # BUTTON CONTROLS (MOSTLY)
            # -------------------------
            keypress = cv2.waitKey(1) & 0xFF
            if keypress == ord("q"):
                break

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
                camera_ops.run_avg(gray, aWeight)
            else:  # After a background is obtained, threshold/segment the hand/foreground
                hand = camera_ops.segment(gray)

                if hand is not None:
                    (thresholded, segmented) = hand
                    cv2.imshow("Threshold", thresholded)  # display the threshold frame
                    thresholded = np.stack((thresholded,) * 3,
                                           axis=-1)  # Give the binary frame 3 channels for the model

                    # -------------------------
                    # MODEL PREDICTION SECTION
                    # -------------------------

                    # OBTAINING AVERAGE PREDICTIONS, SEQUENCES, AND PERMUTATIONS
                    prediction = model.predict([np.reshape(thresholded, (1, HEIGHT, WIDTH, 3))])
                    count += 1
                    accumulated_predictions += prediction

                    if count % mean_cutoff == 0:
                        average_prediction = accumulated_predictions / mean_cutoff
                        accumulated_predictions = np.zeros_like(prediction)
                        ordered, top_signs, percents = predict_ops.top_three(signs, average_prediction)
                        sequence = predict_ops.create_sequence(sequence, top_signs)

                    perm = predict_ops.permutations(sequence)

                    # -----------------------------
                    # PYGAME VISUAL CUES FOR USER
                    # -----------------------------
                    begin = VisualCue(msg="GO!", w=200, h=100, text_color=gb.green, typ='header', seq=sequence, win=gb.win)
                    begin.create_cue()

                    moving_cue = VisualCue(f"SIGN #{str(len(sequence) + 1)}", 175, 100, gb.green, 'prompt', seq=sequence, win=gb.win)
                    moving_cue.create_cue()

                    # Visual printing of top signs so far
                    if len(sequence) > 0 and top_signs is not None:
                        prediction_cue = VisualCue(str(top_signs[0]), 80, 40, gb.green, typ='jutsu', seq=sequence, win=gb.win)
                        prediction_cue.create_cue()
                        for s in top_signs:
                            try:
                                if s == selected_jutsu.get_sequence()[len(sequence)-1]:
                                    print("Thumbs up")
                                    thumbsup = VisualCue(msg=[], w=[], h=[], text_color=(0,0,0), typ='image',
                                                         seq=sequence, image_str='mightguythumbsup.jpg', win=gb.win)
                                    thumbsup.display_image()
                                    pygame.display.update()
                            except Exception as e:
                                print("exception: ", e)

                    # RESET / FINISHED
                    if selected_jutsu.get_sequence() in perm:
                        game_ops.success(selected_jutsu)
                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu,\
                        game, jutsu, player_turn = game_ops.reset_game()
                        break

                    elif len(sequence) >= len(selected_jutsu.get_sequence()) and selected_jutsu.get_sequence() not in perm:
                        game_ops.failed()
                        player_turn = False
                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu,\
                        game, jutsu, player_turn = game_ops.reset_game()
                        break

                    elif keypress == ord("n"):
                        game_ops.failed()
                        player_turn = False
                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu,\
                        game, jutsu, player_turn = game_ops.reset_game()
                        break

                    pygame.display.update()

            # ----------------------------------
            # AFTER THRESHOLD-PREDICTION PART
            # ----------------------------------
            cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)  # draws the box
            num_frames += 1
            # display the original camera frame (with red outline if applicable)
            # cv2.imshow("Video Feed", clone)

        print("Released")
        camera.release()
        cv2.destroyAllWindows()


