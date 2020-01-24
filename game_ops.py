import pygame
import numpy as np
import global_variables as gb
import visual_ops
import jutsu_signs
import jutsu_videos


# --------------------------------------------------------------------------------------------------------------
# JUTSU FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def apply_damage(health, damage):
    health -= damage
    return health


def activate_jutsu(selected_jutsu):
    pygame.mixer_music.stop()
    jutsu_video = selected_jutsu.get_video_string()
    jutsu_videos.play_video(jutsu_video)


def skip_jutsu():
    pygame.mixer_music.stop()
    gb.win.fill(gb.black)
    fail_jutsu_cue = visual_ops.VisualCue('WRONG JUTSU', (gb.display_width*.5), (gb.display_height*.25), gb.red,
                                    'header', [], win=gb.win)
    fail_jutsu_cue.create_cue()


def reset_game():
    pygame.display.update()
    num_frames, count = 0, 0
    accumulated_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    accumulated_predictions = np.array([accumulated_predictions], dtype='float64')
    sequence, top_signs, select, selected_jutsu, visual_ops.Jutsu_Icon.jutsu_que = [], [], [], [], []
    game_phase = True
    jutsu_phase = False

    return sequence, num_frames, count, accumulated_predictions, top_signs, select, selected_jutsu, game_phase, jutsu_phase


# ---------------------------------------------------------------
# GAME CLASSES
# ---------------------------------------------------------------
class Jutsu:

    def __init__(self, jutsu_icon, parent_character_icon, attacking_player):
        self.jutsu_icon = jutsu_icon
        self.parent_character_icon = parent_character_icon
        
        self.attacking_player = attacking_player
        
        self.jutsu_icon_name = jutsu_icon.icon_name
        self.parent_character_icon_name = parent_character_icon.icon_name

    def get_jutsu_signs(self):
        attacking_character_name = self.parent_character_icon_name
        for character in jutsu_signs.names_of_characters:
            character_name = list(character.values())[0]
            if character_name == attacking_character_name:
                the_jutsu_signs = character[self.jutsu_icon_name][0]
                return the_jutsu_signs
        else:
            return "Character not found in chars list from jutsu_signs"

    def get_video_string(self):
        attacking_character_name = self.parent_character_icon_name
        for character in jutsu_videos.names_of_characters:
            character_name = list(character.values())[0]
            if character_name == attacking_character_name:
                the_video_name = character[self.jutsu_icon_name]
                return the_video_name
        else:
            return "Character not found in chars dictionary from jutsu_videos"

    def get_damage(self):
        attacking_character_name = self.parent_character_icon_name
        for character in jutsu_signs.names_of_characters:
            character_name = list(character.values())[0]
            if character_name == attacking_character_name:
                the_jutsu_damage = character[self.jutsu_icon_name][1]
                return the_jutsu_damage
        else:
            return "Character not found in chars list from jutsu_signs ---- regarding get_damage function"

