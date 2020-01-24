import pygame
import numpy as np
import time
import global_variables as gb
import visual_ops
import jutsu_signs
import jutsu_videos


sequence = []


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
                                    'header', sequence, win=gb.win)
    fail_jutsu_cue.create_cue()
    # jt(failure.video)


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

    def __init__(self, icon, parent_icon, attacking_player):
        self.icon = icon
        self.parent_icon = parent_icon
        self.attacking_player = attacking_player
        self.icon_name = icon.icon_name
        self.parent_name = parent_icon.icon_name

    def get_sequence(self):
        for item in jutsu_signs.chars_signs:
            if list(item.values())[0] == self.parent_name:  # Take note of the list(items.values())[0]
                return item[self.icon_name][0]
        else:
            return "Character not found in chars list from jutsu_signs"

    def get_video_string(self):
        for item in jutsu_videos.chars_vids:
            print("char", str(list(item.values())[0]))
            print("parent", self.parent_name)
            if list(item.values())[0] == self.parent_name:
                return item[self.icon_name]
        else:
            return "Character not found in chars dictionary from jutsu_videos"

    def get_damage(self):
        for item in jutsu_signs.chars_signs:
            if list(item.values())[0] == self.parent_name:
                return item[self.icon_name][1]
        else:
            return "Character not found in chars list from damage signs"

