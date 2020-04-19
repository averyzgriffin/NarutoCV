import pygame
from pygame.locals import *
import numpy as np
import ctypes


pygame.init()
ctypes.windll.user32.SetProcessDPIAware()

# Display variables
infoObject = pygame.display.Info()

# display_width =  1550
# display_height =  835
display_width = infoObject.current_w
display_height = infoObject.current_h

display_area = display_width * display_height

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
orange = (255,165,0)
gray = (127,127,127)

# Camera Variables
bg = None
calibrate_frames = 30
top, right, bottom, left = 195, 255, 430, 420
aWeight = 0.5

# PyGame variables
flags = DOUBLEBUF
win = pygame.display.set_mode((display_width, display_height), flags)
pygame.display.set_caption('NARUTO: THE COMPUTER-VISION GAME')

player_turn = True
active_health = 0
active_damage = 0

# Model Variables
num_frames = 0
count = 0
mean_cutoff = 6
accumulated_predictions = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='float64')
top_signs = []
sequence = []
signs = ['bird', 'boar', 'dog', 'dragon', 'hare', 'horse', 'monkey', 'ox', 'ram', 'rat', 'serpent', 'tiger']

# Options
easymode = False
hardmode = True
showsigns = True
