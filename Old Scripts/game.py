import pygame
import time

pygame.init()

# -----------------
# GLOBAL VARIABLES
# -----------------
display_width = 1400
display_height = 950
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
orange = (255,165,0)
tracking = False


win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('NINJUTSUUUU')


def text_objects(text, font):
    textsurface = font.render(text, True, blue)
    return textsurface, textsurface.get_rect()


def message_display(text, location, size):
    font_text = pygame.font.Font('freesansbold.ttf', size)
    textsurf, textrect = text_objects(text, font_text)
    textrect.center = location
    win.blit(textsurf, textrect)

    pygame.display.update()
    # game_loop()


def track(text, location, size):
    message_display(text, location, size)


# MAIN LOOP
def game_loop(sequence=0, prediction=None):
    run = True

    while run:
        # print('PyGame Run ')
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.fill(orange)

        if tracking:
            track('TRACKING ON', (display_width/2, 30), 20)

            track(text=f'SIGN #{str(sequence+1)}', location=((display_width / 2), 100), size=50)

        if sequence > 0 and prediction is not None:
            track(text=f"Sign #{sequence}: " + str(prediction), location=(display_width * (sequence/10), 200), size=20)

        pygame.display.update()
        run = False


