import pygame

display_width = 1550  # 1200
display_height = 835  # 800
display_area = display_width * display_height
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
orange = (255,165,0)
bg = None

win = pygame.display.set_mode((display_width, display_height))
# win = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('NINJUTSUUUU')
