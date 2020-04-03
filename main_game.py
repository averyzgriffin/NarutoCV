import numpy as np
import pygame
import cv2
import game_ops
import visual_ops
from visual_ops import CharacterIcon, Jutsu_Icon, Button
import predict_ops
import camera_ops
from keras import models
from model import saved_model
from game_manager import GameManager
from game_manager import CharacterManager
from game_manager import JutsuManager
import global_variables as glob_var
from global_variables import calibrate_frames, aWeight, mean_cutoff, signs, active_health, active_damage


model = models.load_model(saved_model)
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()


# ----------------------------------------
# MAIN
# -----------------------------------------
if __name__ == "__main__":

    def main_menu():

        play_button = Button((glob_var.display_width//3), (glob_var.display_height//2), 200, 100, "ENTER", character_select)
        quit_button = Button((glob_var.display_width//3 * 2), (glob_var.display_height//2), 200, 100, "QUIT", quit)

        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glob_var.win.blit(background, (0,0))

            play_button.display_button()
            quit_button.display_button()



            pygame.display.update()


    def character_select():
        player1_character1_icon = CharacterIcon('kakashi', player_num=1, icon_num=1)
        player1_character2_icon = CharacterIcon('obito', 1, 2)
        player1_character3_icon = CharacterIcon('guy', 1, 3)
        player2_character1_icon = CharacterIcon('crow', 2, 1)
        player2_character2_icon = CharacterIcon('akamaru', 2, 2)
        player2_character3_icon = CharacterIcon('naruto', 2, 3)

        all_characters = [player1_character1_icon, player1_character2_icon, player1_character3_icon,
                          player2_character1_icon, player2_character2_icon, player2_character3_icon]

        player1_character1_jutsu1_icon = Jutsu_Icon(icon_name='Kakashi Sharingan', player_num=1, icon_num=1,
                                                    parent_icon=player1_character1_icon)
        player1_character1_jutsu2_icon = Jutsu_Icon('Ninja Hounds', 1, 2, player1_character1_icon)
        player1_character1_jutsu3_icon = Jutsu_Icon('Lightning Blade', 1, 3, player1_character1_icon)
        player1_character1_jutsu4_icon = Jutsu_Icon('Hiding', 1, 4, player1_character1_icon)

        player1_character2_jutsu1_icon = Jutsu_Icon(icon_name='Tobi Chains', player_num=1, icon_num=1,
                                                    parent_icon=player1_character2_icon)
        player1_character2_jutsu2_icon = Jutsu_Icon('Tobi Kamui', 1, 2, player1_character2_icon)
        player1_character2_jutsu3_icon = Jutsu_Icon('Summoning Nine Tails', 1, 3, player1_character2_icon)
        player1_character2_jutsu4_icon = Jutsu_Icon('Rin', 1, 4, player1_character2_icon)

        player1_character3_jutsu1_icon = Jutsu_Icon(icon_name='Guy Leaf Whirl Wind', player_num=1, icon_num=1,
                                                    parent_icon=player1_character3_icon)
        player1_character3_jutsu2_icon = Jutsu_Icon('Counter Punch', 1, 2, player1_character3_icon)
        player1_character3_jutsu3_icon = Jutsu_Icon('6th Gate of Joy', 1, 3, player1_character3_icon)
        player1_character3_jutsu4_icon = Jutsu_Icon('Guy Dodge', 1, 4, player1_character3_icon)

        player2_character1_jutsu1_icon = Jutsu_Icon(icon_name='Crow Stab', player_num=2, icon_num=1,
                                                    parent_icon=player2_character1_icon)
        player2_character1_jutsu2_icon = Jutsu_Icon('Crow Poison Bomb', 2, 2, player2_character1_icon)
        player2_character1_jutsu3_icon = Jutsu_Icon('Crow Black Ant', 2, 3, player2_character1_icon)
        player2_character1_jutsu4_icon = Jutsu_Icon('Crow Substitution', 2, 4, player2_character1_icon)

        player2_character2_jutsu1_icon = Jutsu_Icon(icon_name='Fang over Fang', player_num=2, icon_num=1,
                                                    parent_icon=player2_character2_icon)
        player2_character2_jutsu2_icon = Jutsu_Icon('Dynamic Marking', 2, 2, player2_character2_icon)
        player2_character2_jutsu3_icon = Jutsu_Icon('Double Headed Wolf', 2, 3, player2_character2_icon)
        player2_character2_jutsu4_icon = Jutsu_Icon('Puppy mode', 2, 4, player2_character2_icon)

        player2_character3_jutsu1_icon = Jutsu_Icon(icon_name='Rasengan', player_num=2, icon_num=1,
                                                    parent_icon=player2_character3_icon)
        player2_character3_jutsu2_icon = Jutsu_Icon('Shadow Clone Jutsu', 2, 2, player2_character3_icon)
        player2_character3_jutsu3_icon = Jutsu_Icon('Chakra Boost', 2, 3, player2_character3_icon)
        player2_character3_jutsu4_icon = Jutsu_Icon('Shadow Save', 2, 4, player2_character3_icon)

        CharacterManager.player1_character1_icon = player1_character1_icon
        CharacterManager.player1_character2_icon = player1_character2_icon
        CharacterManager.player1_character3_icon = player1_character3_icon
        CharacterManager.player2_character1_icon = player2_character1_icon
        CharacterManager.player2_character2_icon = player2_character2_icon
        CharacterManager.player2_character3_icon = player2_character3_icon

        CharacterManager.all_characters = all_characters

        JutsuManager.player1_character1_jutsu1_icon = player1_character1_jutsu1_icon
        JutsuManager.player1_character1_jutsu2_icon = player1_character1_jutsu2_icon
        JutsuManager.player1_character1_jutsu3_icon = player1_character1_jutsu3_icon
        JutsuManager.player1_character1_jutsu4_icon = player1_character1_jutsu4_icon
        JutsuManager.player1_character2_jutsu1_icon = player1_character2_jutsu1_icon
        JutsuManager.player1_character2_jutsu2_icon = player1_character2_jutsu2_icon
        JutsuManager.player1_character2_jutsu3_icon = player1_character2_jutsu3_icon
        JutsuManager.player1_character2_jutsu4_icon = player1_character2_jutsu4_icon
        JutsuManager.player1_character3_jutsu1_icon = player1_character3_jutsu1_icon
        JutsuManager.player1_character3_jutsu2_icon = player1_character3_jutsu2_icon
        JutsuManager.player1_character3_jutsu3_icon = player1_character3_jutsu3_icon
        JutsuManager.player1_character3_jutsu4_icon = player1_character3_jutsu4_icon
        JutsuManager.player2_character1_jutsu1_icon = player2_character1_jutsu1_icon
        JutsuManager.player2_character1_jutsu2_icon = player2_character1_jutsu2_icon
        JutsuManager.player2_character1_jutsu3_icon = player2_character1_jutsu3_icon
        JutsuManager.player2_character1_jutsu4_icon = player2_character1_jutsu4_icon
        JutsuManager.player2_character2_jutsu1_icon = player2_character2_jutsu1_icon
        JutsuManager.player2_character2_jutsu2_icon = player2_character2_jutsu2_icon
        JutsuManager.player2_character2_jutsu3_icon = player2_character2_jutsu3_icon
        JutsuManager.player2_character2_jutsu4_icon = player2_character2_jutsu4_icon
        JutsuManager.player2_character3_jutsu1_icon = player2_character3_jutsu1_icon
        JutsuManager.player2_character3_jutsu2_icon = player2_character3_jutsu2_icon
        JutsuManager.player2_character3_jutsu3_icon = player2_character3_jutsu3_icon
        JutsuManager.player2_character3_jutsu4_icon = player2_character3_jutsu4_icon

        game()



    def game():

        attack = False
        visual_ops.CharacterIcon.queued_to_be_attacked = None
        visual_ops.Jutsu_Icon.queued_for_attack = None

        game_ops.change_music("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")
        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))

        game_phase = True
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
                        print("T pressed")
                        GameManager.change_turn()
                    if event.key == pygame.K_RETURN:
                        print("Enter")
                        attack = not attack

                    if event.key == pygame.K_1:
                        CharacterManager.all_characters[3].dead = True
                    if event.key == pygame.K_2:
                        CharacterManager.all_characters[4].dead = True
                    if event.key == pygame.K_3:
                        CharacterManager.all_characters[5].dead = True
                    if event.key == pygame.K_g:
                        GameManager.check_characters()
                        if GameManager.end_game:
                            end_game(GameManager.winner)


            # Background
            glob_var.win.blit(background, (0,0))

            CharacterManager.player1_character1_icon.display_image()
            CharacterManager.player1_character2_icon.display_image()
            CharacterManager.player1_character3_icon.display_image()
            CharacterManager.player2_character1_icon.display_image()
            CharacterManager.player2_character2_icon.display_image()
            CharacterManager.player2_character3_icon.display_image()

            JutsuManager.player1_character1_jutsu1_icon.display_image()
            JutsuManager.player1_character1_jutsu2_icon.display_image()
            JutsuManager.player1_character1_jutsu3_icon.display_image()
            JutsuManager.player1_character1_jutsu4_icon.display_image()
            JutsuManager.player1_character2_jutsu1_icon.display_image()
            JutsuManager.player1_character2_jutsu2_icon.display_image()
            JutsuManager.player1_character2_jutsu3_icon.display_image()
            JutsuManager.player1_character2_jutsu4_icon.display_image()
            JutsuManager.player1_character3_jutsu1_icon.display_image()
            JutsuManager.player1_character3_jutsu2_icon.display_image()
            JutsuManager.player1_character3_jutsu3_icon.display_image()
            JutsuManager.player1_character3_jutsu4_icon.display_image()
            JutsuManager.player2_character1_jutsu1_icon.display_image()
            JutsuManager.player2_character1_jutsu2_icon.display_image()
            JutsuManager.player2_character1_jutsu3_icon.display_image()
            JutsuManager.player2_character1_jutsu4_icon.display_image()
            JutsuManager.player2_character2_jutsu1_icon.display_image()
            JutsuManager.player2_character2_jutsu2_icon.display_image()
            JutsuManager.player2_character2_jutsu3_icon.display_image()
            JutsuManager.player2_character2_jutsu4_icon.display_image()
            JutsuManager.player2_character3_jutsu1_icon.display_image()
            JutsuManager.player2_character3_jutsu2_icon.display_image()
            JutsuManager.player2_character3_jutsu3_icon.display_image()
            JutsuManager.player2_character3_jutsu4_icon.display_image()

            # If using a button instead of keypress for attack, use attack_button.is_clicked instead of just "attack"
            if attack:
                if Jutsu_Icon.queued_for_attack is not None and CharacterIcon.queued_to_be_attacked is not None:
                    jutsu(Jutsu_Icon, CharacterIcon)

            # fps = clock.get_fps()
            # clock.tick()
            # print("FPS ", fps)

            # ----------------------------------------------------
            # Final Update
            pygame.display.update()

            # Reset in-game variables - these need to be reset at the end of every loop.
            Jutsu_Icon.class_clickable = False
            CharacterIcon.class_clickable = False




    def jutsu(jutsu_icon, character_icon):
        num_frames, count = 0, 0
        accumulated_predictions = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='float64')
        sequence, top_signs, select, selected_jutsu, visual_ops.Jutsu_Icon.jutsu_que = [], [], [], [], []

        glob_var.win.fill(glob_var.white)

        selected_jutsu = game_ops.get_jutsu(jutsu_queued=jutsu_icon.queued_for_attack)
        attacked_character = character_icon.queued_to_be_attacked
        procedure = visual_ops.get_selected_jutsu_prompt(selected_jutsu)

        glob_var.win.fill(glob_var.white)

        camera = camera_ops.setup_camera()
        game_ops.change_music("Sound/Naruto OST 1 - Need To Be Strong.mp3")

        jutsu_phase = True
        while jutsu_phase:

            procedure.display_text()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            (grabbed, frame) = camera.read()

            # CAMERA BUTTON CONTROLS
            keypress = cv2.waitKey(1) & 0xFF
            if keypress == ord("q"):
                break

            # COMPUTER VISION OPERATIONS ON FRAME
            processed_frame, color_frame = camera_ops.process_frame(frame)
            (height, width) = processed_frame.shape[:2]

            if num_frames < calibrate_frames:  # 30 frames = 1 seconds ..... I think
                camera_ops.background_run_avg(processed_frame, aWeight)
            else:
                threshold = camera_ops.segment_hand_region(processed_frame)

                if threshold is not None:
                    cv2.imshow("Threshold", threshold)
                    threshold = np.stack((threshold,) * 3, axis=-1)  # Expand frame to 3 channels for the model

                    # MODEL PREDICTION - OBTAINING AVERAGE PREDICTIONS, SEQUENCES, AND PERMUTATIONS
                    prediction = model.predict([np.reshape(threshold, (1, height, width, 3))])
                    accumulated_predictions += prediction

                    count += 1
                    if count % mean_cutoff == 0:
                        accumulated_predictions, sequence, top_signs = predict_ops.get_predictions(
                            accumulated_predictions, prediction, sequence)

                    perm = predict_ops.get_permutations_of_predictions(sequence)

                    # -----------------------------
                    # PYGAME VISUAL CUES FOR USER
                    # -----------------------------
                    begin_attack_visual_cue = visual_ops.HeaderText("GO!", glob_var.green, 75, None, None)
                    begin_attack_visual_cue.display_text()

                    sign_num_cue = visual_ops.PromptText(f'SIGN #{str(len(sequence) + 1)}', glob_var.green, 30,
                                                         sequence, None, None)
                    sign_num_cue.display_text()

                    # Visual printing of top signs so far
                    if len(sequence) > 0 and top_signs is not None:

                        predicted_sign_cue = visual_ops.JutsuText(str(top_signs[0]), glob_var.green, 45, sequence, None,
                                                                  None)
                        predicted_sign_cue.display_text()

                        for s in top_signs:
                            try:
                                if s == selected_jutsu.get_jutsu_signs()[len(sequence) - 1]:
                                    pass  # print("GOOD JOB")
                                else:
                                    pass  # print("INCORRECT SIGN")
                            except Exception as e:
                                print("exception: ", e)

                    # RESET / FINISHED
                    if selected_jutsu.get_jutsu_signs() in perm:
                        attacked_character.health = game_ops.apply_damage(attacked_character.health,
                                                                          selected_jutsu.get_damage())
                        attacked_character.check_health()
                        attacked_character.bar, attacked_character.bar_x, attacked_character.bar_y, \
                        attacked_character.bar_message = attacked_character.create_bar()  # TODO this should be reducable

                        game_ops.activate_jutsu(selected_jutsu)

                        game_ops.release_camera(camera)

                        GameManager.check_characters()
                        if GameManager.end_game:
                            end_game(GameManager.winner)

                        GameManager.change_turn()
                        game()


                    elif len(sequence) >= len(
                            selected_jutsu.get_jutsu_signs()) and selected_jutsu.get_jutsu_signs() not in perm:
                        game_ops.skip_jutsu()
                        GameManager.change_turn()
                        game_ops.release_camera(camera)
                        game()

                    elif keypress == ord("n"):
                        game_ops.skip_jutsu()
                        GameManager.change_turn()
                        game_ops.release_camera(camera)
                        game()

                    pygame.display.update()

            num_frames += 1


    def end_game(winner):

        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glob_var.win.blit(background, (0,0))
            winner_text1 = visual_ops.TextCue(f"PLAYER {winner}", glob_var.black, 100,
                                              glob_var.display_width // 2, (glob_var.display_height // 2) - 200)
            winner_text2 = visual_ops.TextCue("YOU WIN", glob_var.black, 150,
                                              glob_var.display_width // 2, (glob_var.display_height // 2))
            winner_text1.display_text()
            winner_text2.display_text()
            pygame.display.update()
            pygame.time.wait(3000)
            end_game2()


    def end_game2():

        playagain_button = Button((glob_var.display_width//3), (glob_var.display_height//2), 200, 100, "PLAY AGAIN", character_select)
        mainmenu_button = Button((glob_var.display_width//2), (glob_var.display_height//2), 200, 100, "MAIN MENU", main_menu)
        quit_button = Button((glob_var.display_width//3 * 2), (glob_var.display_height//2), 200, 100, "EXIT GAME", quit)

        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glob_var.win.blit(background, (0,0))

            playagain_button.display_button()
            mainmenu_button.display_button()
            quit_button.display_button()


            pygame.display.update()







    main_menu()
