import numpy as np
import imutils
import pygame
import cv2
import game_ops
from game_ops import Jutsu
import visual_ops
from visual_ops import CharacterIcon, Button, VisualCue, Jutsu_Icon 
import predict_ops
import camera_ops
from keras import models
from model import saved_model
import global_variables as glob_var
from global_variables import calibrate, WIDTH, HEIGHT, top, right, bottom, left, aWeight,\
    num_frames, count,mean_cutoff, accumulated_predictions, top_signs, sequence, signs,\
    player_turn, attack, active_health, active_damage


model = models.load_model(saved_model)

pygame.init()

# ----------------------------------------------------------------------------------------
# GAME OBJECTS INSTANTIATION
# ----------------------------------------------------------------------------------------
player1_character1_icon = CharacterIcon('kakashi', 1, 1, win=glob_var.win)
player1_character2_icon = CharacterIcon('obito', 1, 2, win=glob_var.win)
player1_character3_icon = CharacterIcon('guy', 1, 3, win=glob_var.win)
player2_character1_icon = CharacterIcon('crow', 2, 1, win=glob_var.win)
player2_character2_icon = CharacterIcon('akamaru', 2, 2, win=glob_var.win)
player2_character3_icon = CharacterIcon('naruto', 2, 3, win=glob_var.win)

player1_character1_jutsu1_icon = Jutsu_Icon(icon_name='Kakashi Sharingan', player_num=1, icon_num=1, parent_icon=player1_character1_icon, win=glob_var.win)
player1_character1_jutsu2_icon = Jutsu_Icon('Ninja Hounds', 1, 2, player1_character1_icon, win=glob_var.win)
player1_character1_jutsu3_icon = Jutsu_Icon('Lightning Blade', 1, 3, player1_character1_icon, win=glob_var.win)
player1_character1_jutsu4_icon = Jutsu_Icon('Hiding', 1, 4, player1_character1_icon, win=glob_var.win)

player1_character2_jutsu1_icon = Jutsu_Icon(icon_name='Tobi Chains', player_num=1, icon_num=1, parent_icon=player1_character2_icon, win=glob_var.win)
player1_character2_jutsu2_icon = Jutsu_Icon('Tobi Kamui', 1, 2, player1_character2_icon, win=glob_var.win)
player1_character2_jutsu3_icon = Jutsu_Icon('Summoning Nine Tails', 1, 3, player1_character2_icon, win=glob_var.win)
player1_character2_jutsu4_icon = Jutsu_Icon('Rin', 1, 4, player1_character2_icon, win=glob_var.win)

player1_character3_jutsu1_icon = Jutsu_Icon(icon_name='Guy Leaf Whirl Wind', player_num=1, icon_num=1, parent_icon=player1_character3_icon, win=glob_var.win)
player1_character3_jutsu2_icon = Jutsu_Icon('Counter Punch', 1, 2, player1_character3_icon, win=glob_var.win)
player1_character3_jutsu3_icon = Jutsu_Icon('6th Gate of Joy', 1, 3, player1_character3_icon, win=glob_var.win)
player1_character3_jutsu4_icon = Jutsu_Icon('Guy Dodge', 1, 4, player1_character3_icon, win=glob_var.win)
 
player2_character1_jutsu1_icon = Jutsu_Icon(icon_name='Rasengan', player_num=2, icon_num=1, parent_icon=player2_character3_icon, win=glob_var.win)
player2_character1_jutsu2_icon = Jutsu_Icon('Shadow Clone Jutsu', 2, 2, player2_character3_icon, win=glob_var.win)
player2_character1_jutsu3_icon = Jutsu_Icon('Chakra Boost', 2, 3, player2_character3_icon, win=glob_var.win)
player2_character1_jutsu4_icon = Jutsu_Icon('Shadow Save', 2, 4, player2_character3_icon, win=glob_var.win)

player2_character2_jutsu1_icon = Jutsu_Icon(icon_name='Crow Stab', player_num=2, icon_num=1, parent_icon=player2_character1_icon, win=glob_var.win)
player2_character2_jutsu2_icon = Jutsu_Icon('Crow Poison Bomb', 2, 2, player2_character1_icon, win=glob_var.win)
player2_character2_jutsu3_icon = Jutsu_Icon('Crow Black Ant', 2, 3, player2_character1_icon, win=glob_var.win)
player2_character2_jutsu4_icon = Jutsu_Icon('Crow Substitution', 2, 4, player2_character1_icon, win=glob_var.win)

player2_character3_jutsu1_icon = Jutsu_Icon(icon_name='Fang over Fang', player_num=2, icon_num=1, parent_icon=player2_character2_icon, win=glob_var.win)
player2_character3_jutsu2_icon = Jutsu_Icon('Dynamic Marking', 2, 2, player2_character2_icon, win=glob_var.win)
player2_character3_jutsu3_icon = Jutsu_Icon('Double Headed Wolf', 2, 3, player2_character2_icon, win=glob_var.win)
player2_character3_jutsu4_icon = Jutsu_Icon('Puppy mode', 2, 4, player2_character2_icon, win=glob_var.win)

background = pygame.image.load("env_icons/background2.jpg")
background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))

pygame.mixer.init()
pygame.mixer.music.load("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")
pygame.mixer.music.play(-1)


# ----------------------------------------
# MAIN
# -----------------------------------------
if __name__ == "__main__":

    game_phase = True
    jutsu_phase = False

    while True:

        while game_phase:

            # PyGame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # KEY PRESSES
                if event.type == pygame.KEYDOWN:
                    print('keydown')
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_t:
                        player_turn = not player_turn
                        CharacterIcon.class_turn = player_turn
                    if event.key == pygame.K_RETURN:
                        print("Enter")
                        attack = not attack

            # Background
            glob_var.win.fill(glob_var.orange)
            glob_var.win.blit(background, (0,0))

            player1_character1_icon.display_image()
            player1_character2_icon.display_image()
            player1_character3_icon.display_image()
            player2_character1_icon.display_image()
            player2_character2_icon.display_image()
            player2_character3_icon.display_image()

            player1_character1_jutsu1_icon.display_image()
            player1_character1_jutsu2_icon.display_image()
            player1_character1_jutsu3_icon.display_image()
            player1_character1_jutsu4_icon.display_image()
            player1_character2_jutsu1_icon.display_image()
            player1_character2_jutsu2_icon.display_image()
            player1_character2_jutsu3_icon.display_image()
            player1_character2_jutsu4_icon.display_image()
            player1_character3_jutsu1_icon.display_image()
            player1_character3_jutsu2_icon.display_image()
            player1_character3_jutsu3_icon.display_image()
            player1_character3_jutsu4_icon.display_image()

            player2_character1_jutsu1_icon.display_image()
            player2_character1_jutsu2_icon.display_image()
            player2_character1_jutsu3_icon.display_image()
            player2_character1_jutsu4_icon.display_image()
            player2_character2_jutsu1_icon.display_image()
            player2_character2_jutsu2_icon.display_image()
            player2_character2_jutsu3_icon.display_image()
            player2_character2_jutsu4_icon.display_image()
            player2_character3_jutsu1_icon.display_image()
            player2_character3_jutsu2_icon.display_image()
            player2_character3_jutsu3_icon.display_image()
            player2_character3_jutsu4_icon.display_image()

            # If using a button instead of keypress for attack, use attack_button.is_clicked instead of just "attack"
            if attack:
                if Jutsu_Icon.queued_for_attack is not None and CharacterIcon.queued_to_be_attack is not None:
                    glob_var.win.fill((255, 255, 255))

                    select = Jutsu_Icon.queued_for_attack
                    selected_jutsu = Jutsu(jutsu_icon=select, parent_character_icon=select.parent_icon)
                    active_damage = selected_jutsu.get_damage()

                    attacked_character = CharacterIcon.queued_to_be_attack
                    active_health = attacked_character.health
                    # attacked_character.health -= active_damage

                    procedure = visual_ops.get_jutsu_selected_visual(selected_jutsu, glob_var.win)
                    glob_var.win.fill(glob_var.white)

                    camera = camera_ops.setup_camera()

                    jutsu_phase= True
                    game_phase = False
                    attack = False  # attack_button.is_clicked = False

                    pygame.mixer_music.stop()
                    pygame.mixer_music.load("Sound/Naruto OST 1 - Need To Be Strong.mp3")
                    pygame.mixer_music.play(-1)

            print(Jutsu_Icon.queued_for_attack)

            # ----------------------------------------------------
            # Final Update
            pygame.display.update()

            # Reset in-game variables - these all need to happen at the very end as so to reset them every loop. Now, if
            # we can figure out a way to not need to do it every loop, perhaps we can speed things up.
            # attack_button.is_clicked = False
            Button.class_clickable = False
            Jutsu_Icon.class_clickable = False
            CharacterIcon.char_highlighted = False

        # -----------------------------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------
        # COMPUTER VISION & HAND SIGNS SECTION
        # -----------------------------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------
        while jutsu_phase:

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
                camera_ops.background_run_avg(gray, aWeight)
            else:  # After a background is obtained, threshold/segment the hand/foreground
                hand = camera_ops.segment_hand_region(gray)

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
                        ordered, top_signs, percents = predict_ops.get_top3_sign_predictions(signs, average_prediction)
                        sequence = predict_ops.get_sequence_of_predictions(sequence, top_signs)

                    perm = predict_ops.get_permutations_of_predictions(sequence)

                    # -----------------------------
                    # PYGAME VISUAL CUES FOR USER
                    # -----------------------------
                    begin_attack_visual_cue = VisualCue("GO!", w=glob_var.display_width*0.166666, h=glob_var.display_height*0.125,
                                      text_color=glob_var.green, typ='header', seq=sequence, win=glob_var.win)
                    begin_attack_visual_cue.create_cue()

                    current_sign_number_visual_cue = VisualCue(f'SIGN #{str(len(sequence)+1)}', glob_var.display_width*0.14583334,
                                         glob_var.display_height*0.125, glob_var.green, 'prompt', sequence, glob_var.win)
                    current_sign_number_visual_cue.create_cue()

                    # Visual printing of top signs so far
                    if len(sequence) > 0 and top_signs is not None:
                        predicted_sign_visual_cue = VisualCue(str(top_signs[0]), glob_var.display_width*0.06666667,
                                                   glob_var.display_height*0.05, glob_var.green, 'jutsu', sequence, glob_var.win)
                        predicted_sign_visual_cue.create_cue()
                        for s in top_signs:
                            try:
                                if s == selected_jutsu.get_jutsu_signs()[len(sequence)-1]:
                                    correct_sign_visual_cue = VisualCue(msg=[], w=[], h=[], text_color=(0, 0, 0), typ='image',
                                                         seq=sequence, image_str='character_icons/mightguythumbsup.jpg', win=glob_var.win)
                                    correct_sign_visual_cue.display_image()
                                    pygame.display.update()
                            except Exception as e:
                                print("exception: ", e)

                    # RESET / FINISHED
                    if selected_jutsu.get_jutsu_signs() in perm:
                        attacked_character.health = game_ops.apply_damage(active_health, active_damage)
                        attacked_character.check_health()
                        game_ops.activate_jutsu(selected_jutsu)

                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu, \
                        game_phase, jutsu_phase = game_ops.reset_game()
                        player_turn = not player_turn
                        pygame.mixer.music.load("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")
                        pygame.mixer_music.play()
                        break

                    elif len(sequence) >= len(selected_jutsu.get_jutsu_signs()) and selected_jutsu.get_jutsu_signs() not in perm:
                        game_ops.skip_jutsu()

                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu, \
                        game_phase, jutsu_phase = game_ops.reset_game()
                        player_turn = not player_turn
                        pygame.mixer.music.load("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")
                        pygame.mixer_music.play()
                        break

                    elif keypress == ord("n"):
                        game_ops.skip_jutsu()

                        sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu, \
                        game_phase, jutsu_phase = game_ops.reset_game()
                        player_turn = not player_turn
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

