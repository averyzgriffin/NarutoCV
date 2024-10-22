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
import game_manager
from game_manager import GameManager
from game_manager import CharacterManager
from game_manager import JutsuManager
import global_variables as glob_var
from global_variables import calibrate_frames, aWeight, mean_cutoff, signs


model = models.load_model(saved_model)
clock = pygame.time.Clock()
pygame.mixer.init()

pygame.mixer_music.set_volume(.2)


if __name__ == "__main__":

    def main_menu():
        
        w = glob_var.display_width
        h = glob_var.display_height  

        title = visual_ops.TextCue("NARUTO CV", glob_var.blue, w/20, w/2, h/5, font="extras/font_ninja_naruto/njnaruto.ttf")
        title2 = visual_ops.TextCue("A COMPUTER VISION + MACHINE LEARNING SPOOF GAME", glob_var.blue, w/60, w/2, h/5*1.4,
                                    font="extras/font_ninja_naruto/njnaruto.ttf")

        play_button = Button((w//5), (h//2), w/7.75, h/8.35, "ENTER DOJO", construct_characters)
        test_button = Button((w//5*2), (h//2), w/7.75, h/8.35, "PRACTICE", test_mode)
        option_button = Button((w//5*3), (h//2), w/7.75, h/8.35, "OPTIONS", options_menu)
        quit_button = Button((w//5*4), (h//2), w/7.75, h/8.35, "WALK AWAY", quit)

        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (w, h))

        game_ops.change_music("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")

        GameManager.active_game = False


        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glob_var.win.blit(background, (0,0))

            pygame.draw.rect(glob_var.win, glob_var.black,[w/2 - w/1.75/2 - 2, h/5 - h/5/2 - 2, w/1.75 + 4, h/5 + 4])
            pygame.draw.rect(glob_var.win, glob_var.orange,[w/2 - w/1.75/2, h/5 - h/5/2, w/1.75, h/5])

            title.display_text()
            title2.display_text()

            play_button.display_button()
            test_button.display_button()
            option_button.display_button()
            quit_button.display_button()

            pygame.display.update()


    def options_menu():
        
        w = glob_var.display_width
        h = glob_var.display_height  

        home_button = Button((w//10 * 1), (h//12 * 1), w/22.1, h/23.8, "HOME", main_menu)
        game_button = Button((w//10 * 1), (h//12 * 1), w/22.1, h/23.8, "EXIT", pause_menu)

        difficulty_button = Button(w // 8, (h // 3), w/6, h/8, "DIFFICULTY", highlight=False)
        sign_option_button = Button(w // 8, (h // 3 * 2), w/6, h/9, "HAND-SIGNS", highlight=False)

        easy_button = Button(w // 5*2 - w/15.5, (h // 3), w/7.8, h/8.8, "EASY", game_manager.easy_difficulty)
        hard_button = Button(w // 5*2 + w/15.5, (h // 3), w/7.8, h/8.8, "HARD", game_manager.hard_difficulty)
        showsigns_button = Button((w // 5*2 - w/15.5), (h // 3 * 2), w/7.8, h/8.8, "SHOW SIGNS", game_manager.show_signs)
        hidesigns_button = Button((w // 5*2 + w/15.5), (h // 3 * 2), w/7.8, h/8.8, "HIDE SIGNS", game_manager.hide_signs)

        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glob_var.win.blit(background, (0,0))

            if GameManager.active_game:
                game_button.display_button()
            else:
                home_button.display_button()

            difficulty_button.display_button()
            sign_option_button.display_button()

            easy_button.display_button()
            hard_button.display_button()
            showsigns_button.display_button()
            hidesigns_button.display_button()

            if glob_var.easymode:
                easy_button.boxcolor = (255,207,158)
                hard_button.boxcolor = glob_var.orange
            else:
                easy_button.boxcolor = glob_var.orange
                hard_button.boxcolor = (255,207,158)
            if glob_var.showsigns:
                showsigns_button.boxcolor = (255,207,158)
                hidesigns_button.boxcolor = glob_var.orange
            else:
                showsigns_button.boxcolor = glob_var.orange
                hidesigns_button.boxcolor = (255,207,158)

            pygame.display.update()


    def construct_characters():
        GameManager.player1_turn = True
        GameManager.active_game = True

        player1_character1_icon = CharacterIcon('kakashi', player_num=1, icon_num=1)
        player1_character2_icon = CharacterIcon('hiruzen', 1, 2)
        player1_character3_icon = CharacterIcon('darui', 1, 3)
        player2_character1_icon = CharacterIcon('sasuke', 2, 1)
        player2_character2_icon = CharacterIcon('madara', 2, 2)
        player2_character3_icon = CharacterIcon('itachi', 2, 3)

        all_characters = [player1_character1_icon, player1_character2_icon, player1_character3_icon,
                          player2_character1_icon, player2_character2_icon, player2_character3_icon]

        player1_character1_jutsu1_icon = Jutsu_Icon(icon_name='Fire Ball Jutsu', player_num=1, icon_num=1,
                                                    parent_icon=player1_character1_icon)
        player1_character1_jutsu2_icon = Jutsu_Icon('Fanged Pursuit Jutsu', 1, 2, player1_character1_icon)
        player1_character1_jutsu3_icon = Jutsu_Icon('Lightning Blade', 1, 3, player1_character1_icon)
        player1_character1_jutsu4_icon = Jutsu_Icon('Water Wall', 1, 4, player1_character1_icon)

        player1_character2_jutsu1_icon = Jutsu_Icon(icon_name='Tile Shuriken', player_num=1, icon_num=1,
                                                    parent_icon=player1_character2_icon)
        player1_character2_jutsu2_icon = Jutsu_Icon('Fire Dragon Flame Bombs', 1, 2, player1_character2_icon)
        player1_character2_jutsu3_icon = Jutsu_Icon('Reaper Death Seal', 1, 3, player1_character2_icon)
        player1_character2_jutsu4_icon = Jutsu_Icon('Earth Style Mud Wall', 1, 4, player1_character2_icon)

        player1_character3_jutsu1_icon = Jutsu_Icon(icon_name='Darui Water Wall', player_num=1, icon_num=1,
                                                    parent_icon=player1_character3_icon)
        player1_character3_jutsu2_icon = Jutsu_Icon('Emotion Wave', 1, 2, player1_character3_icon)
        player1_character3_jutsu3_icon = Jutsu_Icon('Laser Circus', 1, 3, player1_character3_icon)
        player1_character3_jutsu4_icon = Jutsu_Icon('Sword Defense', 1, 4, player1_character3_icon)

        player2_character1_jutsu1_icon = Jutsu_Icon(icon_name='Fireball Jutsu', player_num=2, icon_num=1,
                                                    parent_icon=player2_character1_icon)
        player2_character1_jutsu2_icon = Jutsu_Icon('Dragon Flame Jutsu', 2, 2, player2_character1_icon)
        player2_character1_jutsu3_icon = Jutsu_Icon('Chidori', 2, 3, player2_character1_icon)
        player2_character1_jutsu4_icon = Jutsu_Icon('Sasuke Block', 2, 4, player2_character1_icon)

        player2_character2_jutsu1_icon = Jutsu_Icon(icon_name='Majestic Destroyer Flame', player_num=2, icon_num=1,
                                                    parent_icon=player2_character2_icon)
        player2_character2_jutsu2_icon = Jutsu_Icon('Majestic Demolisher', 2, 2, player2_character2_icon)
        player2_character2_jutsu3_icon = Jutsu_Icon('Summoning Nine Tails', 2, 3, player2_character2_icon)
        player2_character2_jutsu4_icon = Jutsu_Icon('Hiding in Ash', 2, 4, player2_character2_icon)

        player2_character3_jutsu1_icon = Jutsu_Icon(icon_name='Exploding Clone', player_num=2, icon_num=1,
                                                    parent_icon=player2_character3_icon)
        player2_character3_jutsu2_icon = Jutsu_Icon('Shuriken Phoenix Flower', 2, 2, player2_character3_icon)
        player2_character3_jutsu3_icon = Jutsu_Icon('Grand Fireball Jutsu', 2, 3, player2_character3_icon)
        player2_character3_jutsu4_icon = Jutsu_Icon('Summoning Crows', 2, 4, player2_character3_icon)

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

        GameManager.end_game = False
        game_ops.change_music("Sound/Naruto Main Theme [Extended].mp3")

        game()


    def pause_menu():

        w, h = glob_var.display_width, glob_var.display_height

        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (w, h))

        unpause_button = Button(w/2, h/8*2,   w/7, h/9, "BACK TO GAME", game, customfont=w/60)
        options_button = Button(w/2, h/8*3, w/7, h/9, "OPTIONS", options_menu, customfont=w/60)
        home_button =    Button(w/2, h/8*4, w/7, h/9, "MAIN MENU", main_menu, customfont=w/60)
        quit_button =    Button(w/2, h/8*5, w/7, h/9, "QUIT GAME", quit, customfont=w/60)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glob_var.win.blit(background, (0,0))

            unpause_button.display_button()
            options_button.display_button()
            home_button.display_button()
            quit_button.display_button()

            pygame.display.update()




    def game():
        
        w = glob_var.display_width
        h = glob_var.display_height

        game_manager.CharacterManager.queued_to_be_attacked = ''
        game_manager.JutsuManager.queued_for_attack = ''

        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (w, h))

        attack_button = Button((w//2), (h//8), w/9.5, h/11, "ATTACK")
        pause_button = Button((w//12 * 1), (h//12 * 1), w/22.1, h/23.8, "PAUSE", pause_menu)

        if GameManager.player1_turn:
            turn_int = 1
        else:
            turn_int = 2

        turn_cue = visual_ops.TextCue(f"PLAYER {turn_int}'S TURN", glob_var.white, w/60, w/2, h/20*16.7)
        jutsu_cue = visual_ops.TextCue(f"{game_manager.JutsuManager.queued_for_attack}", glob_var.white, w/60, w//2, h/20*17.7)
        character_cue = visual_ops.TextCue(f"{game_manager.CharacterManager.queued_to_be_attacked}", glob_var.white, w/60, w//2, h/20*18.7)

        game_phase = True
        while game_phase:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_t:
                        GameManager.change_turn()

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


            glob_var.win.blit(background, (0,0))

            CharacterManager.player1_character1_icon.display_image()
            CharacterManager.player1_character2_icon.display_image()
            CharacterManager.player1_character3_icon.display_image()
            CharacterManager.player2_character1_icon.display_image()
            CharacterManager.player2_character2_icon.display_image()
            CharacterManager.player2_character3_icon.display_image()

            if GameManager.player1_turn:
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
            else:
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

            attack_button.display_button()
            pause_button.display_button()

            pygame.draw.rect(glob_var.win, glob_var.black, [w/2-w/7.75-2, h/1.133-h/13.9-2, w/3.87+4, h/6.958+4])
            pygame.draw.rect(glob_var.win, glob_var.orange, [w/2-w/7.75, h/1.133-h/13.9, w/3.87, h/6.958])

            turn_cue.display_text()
            jutsu_cue.display_text()
            character_cue.display_text()

            if game_manager.CharacterManager.queued_to_be_attacked == '' or game_manager.JutsuManager.queued_for_attack == '':
                attack_button.boxcolor = glob_var.gray
            else:
                attack_button.boxcolor = glob_var.orange

            if attack_button.click_status():
                game_manager.CharacterManager.mouse_cleared = False
                game_manager.JutsuManager.mouse_cleared = False

            click = pygame.mouse.get_pressed()
            if click[0] == 1 and game_manager.CharacterManager.mouse_cleared and game_manager.JutsuManager.mouse_cleared:
                game_manager.CharacterManager.queued_to_be_attacked = ''
                game_manager.JutsuManager.queued_for_attack = ''

            if click[0] == 1 and attack_button.click_status():
                if game_manager.CharacterManager.queued_to_be_attacked != '' and game_manager.JutsuManager.queued_for_attack != '':
                    jutsu()

            if click[0] == 1 and game_manager.JutsuManager.queued_for_attack != jutsu_cue.msg:
                if game_manager.JutsuManager.queued_for_attack != '':
                    jutsu_cue.msg = f"{game_manager.JutsuManager.queued_for_attack.icon_name}".upper()
                else:
                    jutsu_cue.msg = ""
                jutsu_cue.text, jutsu_cue.rect = jutsu_cue.create_text()

            if click[0] == 1 and game_manager.CharacterManager.queued_to_be_attacked != character_cue.msg:
                if game_manager.CharacterManager.queued_to_be_attacked != '':
                    character_cue.msg = f"{game_manager.CharacterManager.queued_to_be_attacked.icon_name}".upper()
                else:
                    character_cue.msg = ""
                character_cue.text, character_cue.rect = character_cue.create_text()

            # Reset in-game variables - these need to be reset at the end of every loop.
            game_manager.CharacterManager.mouse_cleared = True
            game_manager.JutsuManager.mouse_cleared = True

            pygame.display.update()




    def jutsu():
        w = glob_var.display_width
        h = glob_var.display_height

        background = pygame.image.load("env_icons/naruto_background_5_by_pungpp_dcsgik3-fullview.jpg").convert()
        background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))
        glob_var.win.blit(background, (0, 0))

        selected_jutsu = game_ops.get_jutsu(jutsu_queued=game_manager.JutsuManager.queued_for_attack)
        attacked_character = game_manager.CharacterManager.queued_to_be_attacked

        num_frames, count = 0, 0
        accumulated_predictions = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='float64')
        correct_predictions = np.zeros((len(selected_jutsu.get_jutsu_signs())), dtype='O')
        average_prediction = None
        top_predictions = None

        game_ops.change_music("Sound/Naruto OST 1 - Need To Be Strong.mp3")
        visual_ops.get_selected_jutsu_prompt(selected_jutsu)
        camera = camera_ops.setup_camera()

        correct_image = visual_ops.Picture("extras/mightguythumbsup.jpg", 0, int(h/1.85), int(w/9.69), int(w/9.69), 'border')
        if glob_var.showsigns:
            bird_picture = visual_ops.Picture("extras/bird.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            boar_picture = visual_ops.Picture("extras/boar.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            dog_picture = visual_ops.Picture("extras/dog.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            dragon_picture = visual_ops.Picture("extras/dragon.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            hare_picture = visual_ops.Picture("extras/hare.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            horse_picture = visual_ops.Picture("extras/horse.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            monkey_picture = visual_ops.Picture("extras/monkey.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            ox_picture = visual_ops.Picture("extras/ox.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            ram_picture = visual_ops.Picture("extras/ram.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            rat_picture = visual_ops.Picture("extras/rat.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            serpent_picture = visual_ops.Picture("extras/serpent.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')
            tiger_picture = visual_ops.Picture("extras/tiger.jpg", 0, int(h/1.28), int(w/12.9), int(w/12.9), 'border')

            sign_pics_dict = {"bird": bird_picture, "boar": boar_picture, "dog": dog_picture, "dragon": dragon_picture,
                              "hare": hare_picture, "horse": horse_picture, "monkey": monkey_picture, "ox": ox_picture,
                              "ram": ram_picture, "rat": rat_picture, "serpent": serpent_picture, "tiger": tiger_picture}

        start = pygame.time.get_ticks()

        # ---------------------------------------------------START--------------------------------------
        jutsu_phase = True
        while jutsu_phase:

            glob_var.win.blit(background, (0, 0))

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

            if num_frames < calibrate_frames:
                camera_ops.background_run_avg(processed_frame, aWeight)
            else:
                threshold = camera_ops.segment_hand_region(processed_frame)

                if threshold is not None:
                    cv2.imshow("Threshold", threshold)
                    cv2.moveWindow("Threshold", glob_var.display_width // 10*9, glob_var.display_height//20)
                    threshold = np.stack((threshold,) * 3, axis=-1)

                    # TIMER - COUNTDOWN
                    elapsed = (pygame.time.get_ticks() - start - 2500) / 1000

                    timer_bar = Button(0, glob_var.display_height, (glob_var.display_width * ((20-elapsed)/20) * 2), glob_var.display_height/10, highlight=False)
                    timer_bar.boxcolor = glob_var.orange
                    timer_bar.display_button()


                    if timer_bar.w <= 0:
                        game_ops.skip_jutsu()
                        GameManager.change_turn()
                        game_ops.release_camera(camera)
                        game_ops.change_music("Sound/Naruto Main Theme [Extended].mp3")
                        game()

                    # ---- PREDICTION FUNCTIONALITY ----
                    count += 1
                    prediction = model.predict([np.reshape(threshold, (1, height, width, 3))])
                    accumulated_predictions += prediction

                    if count % mean_cutoff == 0:
                        average_prediction, accumulated_predictions = predict_ops.get_avererage_prediction(accumulated_predictions)
                        top_predictions = predict_ops.get_top_signs(signs, average_prediction)

                    if average_prediction is not None:

                        for n in range(len(selected_jutsu.get_jutsu_signs())):

                            if correct_predictions[n-1] != 0 or n == 0:

                                if correct_predictions[n] == selected_jutsu.get_jutsu_signs()[n]:
                                    correct_image.x = ((1 / (len(selected_jutsu.get_jutsu_signs()) + 1)) * (n + 1) * glob_var.display_width)
                                    correct_image.display_image()

                                    if n + 1 == len(selected_jutsu.get_jutsu_signs()):
                                        attacked_character.health = game_ops.apply_damage(attacked_character.health,
                                                                                          selected_jutsu.get_damage())
                                        attacked_character.check_health()
                                        attacked_character.bar, attacked_character.bar_x, attacked_character.bar_y, \
                                        attacked_character.bar_message = attacked_character.create_bar()

                                        game_ops.activate_jutsu(selected_jutsu)

                                        game_ops.release_camera(camera)

                                        GameManager.check_characters()
                                        if GameManager.end_game:
                                            end_game(GameManager.winner)

                                        GameManager.change_turn()
                                        game_ops.change_music("Sound/Naruto Main Theme [Extended].mp3")
                                        game()

                                elif signs[np.argmax(average_prediction)] == selected_jutsu.get_jutsu_signs()[n] and glob_var.hardmode:
                                    correct_image.x = ((1 / (len(selected_jutsu.get_jutsu_signs()) + 1)) * (n + 1) * glob_var.display_width)
                                    correct_image.display_image()

                                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sound/sound_effect_1.wav'))

                                    correct_predictions[n] = signs[np.argmax(average_prediction)]

                                elif selected_jutsu.get_jutsu_signs()[n] in top_predictions and glob_var.easymode:
                                    correct_image.x = ((1 / (len(selected_jutsu.get_jutsu_signs()) + 1)) * (n + 1) * glob_var.display_width)
                                    correct_image.display_image()

                                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sound/sound_effect_1.wav'))

                                    correct_predictions[n] = selected_jutsu.get_jutsu_signs()[n]


                    begin_button = Button((w // 2),(h // 10), w/3.1, h/8.35, "GO!", highlight=False)
                    begin_button.display_button()

                    for n in range(len(selected_jutsu.get_jutsu_signs())):
                        sign_cue = Button(((1 / (len(selected_jutsu.get_jutsu_signs()) + 1)) * (n+1) * w), h/3, w/11.07, h/11.9, (str(selected_jutsu.get_jutsu_signs()[n]).upper()), highlight=False)
                        sign_cue1 = Button(((1 / (len(selected_jutsu.get_jutsu_signs()) + 1)) * (n+1) * w), h/4.175, w/19.38, h/20.9, f"SIGN #{n+1}", highlight=False)
                        if glob_var.showsigns:
                            sign_picture = sign_pics_dict[selected_jutsu.get_jutsu_signs()[n]]
                            sign_picture.x = (1 / (len(selected_jutsu.get_jutsu_signs()) + 1)) * (n+1) * w
                            sign_picture.display_image()

                        sign_cue1.display_button()
                        sign_cue.display_button()

                    pygame.display.update()

            num_frames += 1


    def test_mode():

        game_ops.change_music("Sound/Naruto - Bad Situation (Extended).mp3")

        background = pygame.image.load("env_icons/Chunin_Examination_Arena.png").convert()
        background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))

        camera = camera_ops.setup_camera()
        num_frames, count = 0, 0
        accumulated_predictions = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='float64')
        average_prediction = None

        font_size = glob_var.display_width//15.5
        x = glob_var.display_width//2
        y = glob_var.display_height//2
        w = glob_var.display_width / 3.2
        h = glob_var.display_height / 3.4
        sign_text = visual_ops.TextCue('TEST', glob_var.white, font_size, x, y)

        home_button = Button((glob_var.display_width//12 * 1), (glob_var.display_height//10 * 1), glob_var.display_width/22.1, glob_var.display_height/23.8, "HOME", main_menu)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            if home_button.click_status():
                click = pygame.mouse.get_pressed()
                if click[0] == 1:
                    game_ops.release_camera(camera)

            glob_var.win.blit(background, (0,0))

            pygame.draw.rect(glob_var.win, glob_var.orange, (x - (w/2+2),  y - (h/2+2), w + 4, h + 4), 0)
            pygame.draw.rect(glob_var.win, glob_var.black, (x - w/2,  y - h/2, w, h), 0)

            home_button.display_button()

            (grabbed, frame) = camera.read()

            # COMPUTER VISION OPERATIONS ON FRAME
            processed_frame, color_frame = camera_ops.process_frame(frame)
            (height, width) = processed_frame.shape[:2]

            if num_frames < calibrate_frames:
                camera_ops.background_run_avg(processed_frame, aWeight)
            else:
                threshold = camera_ops.segment_hand_region(processed_frame)

                if threshold is not None:
                    cv2.imshow("Threshold", threshold)
                    cv2.moveWindow("Threshold", glob_var.display_width // 2 - glob_var.display_width // 20, glob_var.display_height//10)
                    threshold = np.stack((threshold,) * 3, axis=-1)

                    # ---- PREDICTION FUNCTIONALITY ----
                    count += 1
                    prediction = model.predict([np.reshape(threshold, (1, height, width, 3))])
                    accumulated_predictions += prediction

                    if count % mean_cutoff == 0:
                        average_prediction, accumulated_predictions = predict_ops.get_avererage_prediction(
                            accumulated_predictions)

                    if average_prediction is not None:
                        sign_text.msg = str(signs[np.argmax(prediction)]).upper()
                        sign_text.text, sign_text.rect = sign_text.create_text()
                        sign_text.display_text()

            pygame.display.update()
            num_frames += 1



    def end_game(winner):

        background = pygame.image.load("env_icons/background2.jpg").convert()
        background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))
        game_ops.change_music("Sound/Naruto - Morning [EXTENDED].mp3")

        GameManager.active_game = False


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

        playagain_button = Button((glob_var.display_width//3), (glob_var.display_height//2), 200, 100, "PLAY AGAIN", construct_characters)
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
