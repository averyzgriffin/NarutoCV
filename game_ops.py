import pygame
import numpy as np
import global_variables as glob_var
import visual_ops
import jutsu_signs_damage
import jutsu_videos
import camera_ops
from game_manager import GameManager
import time


# --------------------------------------------------------------------------------------------------------------
# GAME FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def change_music(song):
    pygame.mixer_music.stop()
    pygame.mixer_music.load(song)
    pygame.mixer_music.play(-1)


def change_turn():
    GameManager.change_turn()


def start_jutsu_phase(jutsu_icon, character_icon):
    glob_var.win.fill(glob_var.white)

    selected_jutsu = get_jutsu(jutsu_queued=jutsu_icon.queued_for_attack)
    attacked_character = character_icon.queued_to_be_attacked
    procedure = visual_ops.get_selected_jutsu_prompt(selected_jutsu)

    glob_var.win.fill(glob_var.white)

    camera = camera_ops.setup_camera()
    change_music("Sound/Naruto OST 1 - Need To Be Strong.mp3")

    # rtn  gamephase, jutsuphase, attack
    return False, True, False, selected_jutsu, attacked_character, procedure, camera


def start_game_phase():
    pygame.display.update()

    visual_ops.CharacterIcon.queued_to_be_attacked = None
    visual_ops.Jutsu_Icon.queued_for_attack = None

    num_frames, count = 0, 0
    accumulated_predictions = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='float64')
    sequence, top_signs, select, selected_jutsu, visual_ops.Jutsu_Icon.jutsu_que = [], [], [], [], []

    change_turn()
    change_music("Sound/Naruto OST 2 - Afternoon of Konoha.mp3")

    # rtn gamephase, attack phase
    return True, False, sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu


def end_game(winner):
    game_phase = False
    jutsu_phase = False
    GameManager.end_game = True

    glob_var.win.fill(glob_var.white)
    winner_text1 = visual_ops.TextCue(f"PLAYER {winner}", glob_var.black, 100,
                                      glob_var.display_width//2, (glob_var.display_height//2) - 200)
    winner_text2 = visual_ops.TextCue("YOU WIN", glob_var.black, 150,
                                      glob_var.display_width // 2, (glob_var.display_height // 2))
    winner_text1.display_text()
    winner_text2.display_text()
    pygame.display.update()




# --------------------------------------------------------------------------------------------------------------
# JUTSU FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def get_jutsu(jutsu_queued):
    jutsu = Jutsu(jutsu_icon=jutsu_queued, parent_character_icon=jutsu_queued.parent_icon)
    return jutsu


def apply_damage(health, damage):
    health -= damage
    return health


def activate_jutsu(selected_jutsu):
    pygame.mixer_music.stop()  # TODO PUT THIS ELSEWHERE TOGETHER WITH THE SKIP_JUTSU ONE. Not sure what to do.

    jutsu_video = selected_jutsu.get_video_string()
    jutsu_videos.play_video(jutsu_video)


def skip_jutsu():
    pygame.mixer_music.stop()  # TODO PUT THIS ELSEWHERE TOGETHER WITH THE ACTIVATE_JUTSU ONE. Not sure what to do.

    glob_var.win.fill(glob_var.black)
    fail_jutsu_cue = visual_ops.HeaderText('FAILURE', glob_var.red, 100, None, None)
    fail_jutsu_cue.display_text()
    pygame.display.update()
    time.sleep(2)


# ---------------------------------------------------------------
# GAME CLASSES
# ---------------------------------------------------------------
class Jutsu:

    def __init__(self, jutsu_icon, parent_character_icon):

        self.jutsu_icon_name = jutsu_icon.icon_name
        self.parent_character_icon_name = parent_character_icon.icon_name

    def get_jutsu_signs(self):
        for character in jutsu_signs_damage.names_of_characters:
            character_name = list(character.values())[0]
            if character_name == self.parent_character_icon_name:
                the_jutsu_signs = character[self.jutsu_icon_name][0]
                return the_jutsu_signs
        else:
            return "Character not found in chars list from jutsu_signs"

    def get_video_string(self):
        for character in jutsu_videos.names_of_characters:
            character_name = list(character.values())[0]
            if character_name == self.parent_character_icon_name:
                the_video_name = character[self.jutsu_icon_name]
                return the_video_name
        else:
            return "Character not found in chars dictionary from jutsu_videos"

    def get_damage(self):
        for character in jutsu_signs_damage.names_of_characters:
            character_name = list(character.values())[0]
            if character_name == self.parent_character_icon_name:
                the_jutsu_damage = character[self.jutsu_icon_name][1]
                return the_jutsu_damage
        else:
            return "Character not found in chars list from jutsu_signs ---- regarding get_damage function"

