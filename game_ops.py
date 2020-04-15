import pygame
import numpy as np
import global_variables as glob_var
import visual_ops
import jutsu_signs_damage
import jutsu_videos
import camera_ops
from game_manager import GameManager
import time
import cv2

# --------------------------------------------------------------------------------------------------------------
# GAME FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def release_camera(cam):
    cam.release()
    cv2.destroyAllWindows()


def change_music(song):
    pygame.mixer_music.stop()
    pygame.mixer_music.load(song)
    pygame.mixer_music.play(-1)


def change_turn():
    GameManager.change_turn()


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
    pygame.mixer_music.stop()

    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sound/jutsu_start.wav'))
    jutsu_video = selected_jutsu.get_video_string()
    jutsu_videos.play_video(jutsu_video)


def skip_jutsu():
    pygame.mixer_music.stop()

    background = pygame.image.load("env_icons/failed_jutsu.jpeg").convert()
    background = pygame.transform.scale(background, (glob_var.display_width, glob_var.display_height))
    glob_var.win.blit(background, (0, 0))

    pygame.display.update()

    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Sound/failed_jutsu.wav'))

    time.sleep(3)


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

