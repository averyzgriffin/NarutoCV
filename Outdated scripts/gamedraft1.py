import time
import numpy as np
import imutils
import itertools
import pygame
import cv2


# ------------------------
# GLOBAL VARIABLES PYGAME
# ------------------------
display_width = 1200
display_height = 800

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
orange = (255,165,0)

tracking = False
player_turn = True

pygame.init()
win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('NINJUTSUUUU')


# --------------------------------------------------------------------------------------------------------------
# PYGAME FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()

def message_display(text, location, size):
    font_text = pygame.font.Font('freesansbold.ttf', size)
    textsurf, textrect = text_objects(text, font_text)
    textrect.center = location
    win.blit(textsurf, textrect)

    # pygame.display.update()
    # game_loop()

def track(text, location, size):
    message_display(text, location, size)

def prepare(jutsu):
    msg = "You have selected: " + str(jutsu)[2:-2]
    font = pygame.font.Font("freesansbold.ttf", 20)

    textsurf, textRect = text_objects(msg, font)
    textRect.center = ((display_width/2, 200))
    win.blit(textsurf, textRect)

    pygame.display.update()

    time.sleep(1)


# ---------
# CLASSES
# ---------
class Button:

    font = pygame.font.Font("freesansbold.ttf", 20)
    is_clicked = False
    clickable = False

    def __init__(self, msg, x, y, w, h, color, alpha):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r, self.g, self.b = color
        self.alpha = alpha

    def create_text(self):
        textsurf, textRect = text_objects(self.msg, self.font)
        textRect.center = ( (self.x + (self.w/2)), (self.y +(self.h/2)) )
        return textsurf, textRect

    def click_status(self):
        if len(Jutsu_Icon.jutsu_que) > 0:
            self.clickable = True
        else:
            self.clickable = False
        return self.clickable

    def create_button(self):
        clickable = self.click_status()
        if clickable:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
                button = pygame.Surface((self.w, self.h), pygame.SRCALPHA)  # per-pixel alpha
                button.fill((self.r, self.g, self.b, self.alpha))  # notice the alpha value in the color
                win.blit(button, (self.x, self.y))

                if click[0] == 1:
                    print('clicked')
                    self.is_clicked = True
            else:
                button = pygame.draw.rect(win, (self.r, self.g, self.b), (self.x, self.y, self.w, self.h))

            text, rect = self.create_text()
            win.blit(text, rect)

        else:
            button = pygame.Surface((self.w, self.h), pygame.SRCALPHA)  # per-pixel alpha
            button.fill((self.r, self.g, self.b, self.alpha))  # notice the alpha value in the color
            win.blit(button, (self.x, self.y))
            text, rect = self.create_text()
            win.blit(text, rect)


class CharacterIcon:

    p1_x = 30
    p2_x = display_width * (7/8)
    top_y = display_height / 5
    middle_y = display_height * (2 / 5)
    bottom_y = display_height * (3 / 5)

    icon_size = (120, 120)

    def __init__(self, icon_name, player_num, icon_num):
        self.icon_name = icon_name
        self.player_num = player_num
        self.icon_num = icon_num

    def get_x(self):
        if self.player_num == 1:
            x_location = self.p1_x
        elif self.player_num == 2:
            x_location = self.p2_x
        else:
            return "invalid PLAYER number provided to Class Icon get_x method"
        return x_location

    def get_y(self):
        if self.icon_num == 1:
            y_location = self.top_y
        elif self.icon_num == 2:
            y_location = self.middle_y
        elif self.icon_num == 3:
            y_location = self.bottom_y
        else:
            return "invalid ICON number provided to Class Icon get_y method"
        return y_location

    def get_image_from_string(self):
        try:
            path = self.icon_name + ".jpg"
            img = pygame.image.load(path)
        except Exception as e:
            try:
                path = self.icon_name + ".png"
                img = pygame.image.load(path)
            except Exception as e:
                return f"Couldn't find png either for {self.icon_name}."
        return img

    def resize_image(self):
        img = self.get_image_from_string()
        resized = pygame.transform.scale(img, self.icon_size)
        return resized

    def display_image(self):
        x, y = self.get_x(), self.get_y()
        img = self.resize_image()
        win.blit(img, (x, y))


class Jutsu_Icon(CharacterIcon):

    icon_size = (80,80)
    x_offset = display_width // 12
    jutsu_que =[]

    def __init__(self, icon_name, player_num, icon_num, parent_icon):
        super().__init__(icon_name, player_num, icon_num)
        self.parent_icon = parent_icon

    def get_x(self):
        x_p = self.parent_icon.get_x()
        if self.player_num == 1:
            x_p += 30
            x = x_p + (self.x_offset * self.icon_num)
        elif self.player_num == 2:
            x = x_p - (self.x_offset * self.icon_num)  # mirror effect
        else:
            return "invalid player number provided to jutsu_get_x"
        return x

    def get_y(self):
        y_p = self.parent_icon.get_y()
        y = y_p + 20
        return y

    def display_image(self):
        x, y = self.get_x(), self.get_y()
        img = self.resize_image()

        # Button interactability
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        size = self.icon_size[0]

        if (x + size) > mouse[0] > x and (y + size) > mouse[1] > y:
            img = img.convert()
            img.set_alpha(100)

            if click[0] == 1:
                # que up jutsu
                self.jutsu_que.append(self.icon_name)
                print('clicked')

        win.blit(img, (x, y))


icon_1 = CharacterIcon('kakashi', 1, 1)
icon_2 = CharacterIcon('obito', 1, 2)
icon_3 = CharacterIcon('guy', 1, 3)
icon_4 = CharacterIcon('crow', 2, 1)
icon_5 = CharacterIcon('ramenguy', 2, 2)
icon_6 = CharacterIcon('naruto', 2, 3)

jutsu_icon1 = Jutsu_Icon(icon_name='kakashisharingan', player_num=1, icon_num=1, parent_icon=icon_1)
jutsu_icon2 = Jutsu_Icon('ninjahounds', 1, 2, icon_1)
jutsu_icon3 = Jutsu_Icon('lightningblade', 1, 3, icon_1)
jutsu_icon4 = Jutsu_Icon('hiding', 1, 4, icon_1)

jutsu_icon5 = Jutsu_Icon(icon_name='tobichains', player_num=1, icon_num=1, parent_icon=icon_2)
jutsu_icon6 = Jutsu_Icon('tobiabsorb', 1, 2, icon_2)
jutsu_icon7 = Jutsu_Icon('summoning9tails', 1, 3, icon_2)
jutsu_icon8 = Jutsu_Icon('rin', 1, 4, icon_2)

jutsu_icon9 = Jutsu_Icon(icon_name='guyleafwhirlwind', player_num=1, icon_num=1, parent_icon=icon_3)
jutsu_icon10 = Jutsu_Icon('counterpunch', 1, 2, icon_3)
jutsu_icon11 = Jutsu_Icon('sixthgate', 1, 3, icon_3)
jutsu_icon12 = Jutsu_Icon('guydodge', 1, 4, icon_3)

jutsu_icon13 = Jutsu_Icon(icon_name='rasengan', player_num=2, icon_num=1, parent_icon=icon_6)
jutsu_icon14 = Jutsu_Icon('shadowclones', 2, 2, icon_6)
jutsu_icon15 = Jutsu_Icon('chakraboost', 2, 3, icon_6)
jutsu_icon16 = Jutsu_Icon('shadowsave', 2, 4, icon_6)

attack_button = Button("ATTACK", display_width/2, 50, 150, 75, (150,150,150), 100)

# --------
# MAIN
# ---------
if __name__ == "__main__":

    x2 = 400
    y2 = 400
    game = True
    jutsu = False
    jutsu_active = []

    while True:
        while game:
            # print("Summary: ", Jutsu_Icon.jutsu_que)

            # ----------------
            # CONSTANT SECTION
            # ----------------
            # PyGame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # ------------
                # KEY PRESSES
                # ------------
                if event.type == pygame.KEYDOWN:
                    print('keydown')

                    # Change modes
                    if event.key == pygame.K_j:
                        # active_jutsu = get_jutsu(Jutsu_Icon.jutsu_que):
                        Jutsu_Icon.jutsu_que = []
                        game = False
                        jutsu = True

                    # Press enter to end turn
                    if event.key == pygame.K_RETURN and Jutsu_Icon.jutsu_que != None:
                        player_turn = not player_turn

                    # if player_turn:
                        # if event.key == pygame.K_LEFT:
                            # x -= 5
                        # if event.key == pygame.K_RIGHT:
                        #     x += 5
                        # if p1 buttons are clicked:
                            # perform p1 actions
                    # elif not player_turn:
                    #     if event.key == pygame.K_LEFT:
                    #         x2 -= 100
                    #     if event.key == pygame.K_RIGHT:
                    #         x2 += 100
                        # if p2 buttonsz are clicked:
                            # perform p2 actions

            # Background
            win.fill(orange)

            icon_1.display_image()
            icon_2.display_image()
            icon_3.display_image()
            icon_4.display_image()
            icon_5.display_image()
            icon_6.display_image()

            jutsu_icon1.display_image()
            jutsu_icon2.display_image()
            jutsu_icon3.display_image()
            jutsu_icon4.display_image()
            jutsu_icon5.display_image()
            jutsu_icon6.display_image()
            jutsu_icon7.display_image()
            jutsu_icon8.display_image()
            jutsu_icon9.display_image()
            jutsu_icon10.display_image()
            jutsu_icon11.display_image()
            jutsu_icon12.display_image()
            jutsu_icon13.display_image()
            jutsu_icon14.display_image()
            jutsu_icon15.display_image()
            jutsu_icon16.display_image()

            attack_button.create_button()

            p1 = pygame.draw.rect(win, (255,0,0), (200,200,50,50))
            p2 = pygame.draw.rect(win, (0,0,255), (x2,y2,50,50))

            if attack_button.is_clicked:
                jutsu_active = Jutsu_Icon.jutsu_que
                win.fill((220, 255, 220))
                prepare(jutsu_active)
                Jutsu_Icon.jutsu_que = []
                game = False
                jutsu = True

            # -------------
            # Final Update
            pygame.display.update()

        # -------------------------------------
        # COMPUTER VISION & HAND SIGNS SECTION
        # -------------------------------------
        while jutsu:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_j:
                #         jutsu = False
                #         game = True

            win.fill((255, 255, 255))


            # Hint of signs
            track('Lightning Blade: ' + '[horse, tigerzzzz]', location=(200, 600), size=30 - 10)
            track('Fire Style Jutsu: ' + '[horse, cat]', location=(368, 630), size=30 - 10)

            header_position = ((display_width / 2), 30)
            prompt_position = (display_width * ((len(range(2)) + 1) / 6) - 150, 100)  # range(2) = sequence
            jutsu_position = (display_width * (len(range(2)) / 6) - 150, 200)
            image_position = (display_width * (len(range(2)) / 6) - 210, 250)

            # Indicate to player to start weaving signs
            track('---GO!---', location=header_position, size=100)

            track(text=f'SIGN #{str(len(range(2)) + 1)}',
                  location=prompt_position, size=20)  # Mobile Cue.

            # Visual printing of top signs so far
            # if len(range(2)) > 0 and top_signs is not None:
            #     track(text=str(top_signs[0]), location=jutsu_position, size=jutsusize)

                # for s in top_signs:
                #     try:
                #         if s == chidori[len(range(2)) - 1] or s == fireball[len(range(2)) - 1]:
                #             display_images(location=image_position, image='mightguythumbsup.jpg')
                #         else:
                #             display_images((display_width * (len(sequence) / 8), 300), image='narutobadclone.jpg')
                    # except Exception as e:
                    #     pass

                # display_images(((display_width / 2), (display_height / 2)), image='lightningblade1.png')


            # -----------------------------
            # COMPUTER VISION + MODEL CODE
            # -----------------------------
            #
            #
            #

            pygame.display.update()


