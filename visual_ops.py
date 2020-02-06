import pygame
import time
import global_variables as glob_var
import jutsu_signs
from game_manager import GameManager


black = (0,0,0)
pygame.init()


# --------------------------------------------------------------------------------------------------------------
# Visual FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def create_textObject(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()
#
#
# def message_display(text, location, size, win):
#     font_text = pygame.font.Font('freesansbold.ttf', size)
#     textsurf, textrect = create_textObject(text, font_text)
#     textrect.center = location
#     win.blit(textsurf, textrect)


# def track(text, location, size):
#     message_display(text, location, size, win)


def get_jutsu_selected_visual(jutsu, win):
    visual_cue = VisualCue(msg=str(jutsu.get_jutsu_signs()), w=glob_var.display_width, h=(glob_var.display_height*0.0625),
                          text_color=black, typ=[], seq=[], x=0, y=glob_var.display_height * .75, win=win)

    text_ = "You have selected: " + str(jutsu.jutsu_icon_name)
    font = pygame.font.Font("freesansbold.ttf", int(9.259259259259259e-05 * glob_var.display_area * .5))

    textsurf, textRect = create_textObject(text_, font)
    textRect.center = (glob_var.display_width/2, (glob_var.display_height*.25))
    win.blit(textsurf, textRect)

    pygame.display.update()

    time.sleep(3)
    return visual_cue


# ------------------------------------------------------------------------------
# GAME LOOP CLASSES
# ------------------------------------------------------------------------------
class Button:

    font = pygame.font.Font("freesansbold.ttf", int(3.7037037037037037e-05 * glob_var.display_area * .5))
    is_clicked = False
    clickable = False
    class_clickable = False

    def __init__(self, msg, x, y, w, h, color, alpha, win):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r, self.g, self.b = color
        self.alpha = alpha
        self.win = win

    def create_text(self):
        textsurf, textRect = create_textObject(self.msg, self.font)
        textRect.center = ((self.x + (self.w/2)), (self.y + (self.h/2)))
        return textsurf, textRect

    def create_button(self):
        # clickable = self.click_status()
        # if self.clickable:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
            self.clickable = True
            Button.class_clickable = True

            button = pygame.Surface((self.w, self.h), pygame.SRCALPHA)  # per-pixel alpha
            button.fill((self.r, self.g, self.b, self.alpha))  # notice the alpha value in the color
            self.win.blit(button, (self.x, self.y))

            if click[0] == 1:
                print('clicked')
                self.is_clicked = True
        else:
            self.clickable = False
            # Button.class_clickable = False
            button = pygame.draw.rect(self.win, (self.r, self.g, self.b), (self.x, self.y, self.w, self.h))

        text, rect = self.create_text()
        self.win.blit(text, rect)

    # else:
    #     button = pygame.Surface((self.w, self.h), pygame.SRCALPHA)  # per-pixel alpha
    #     button.fill((self.r, self.g, self.b, self.alpha))  # notice the alpha value in the color
    #     self.win.blit(button, (self.x, self.y))
    #     text, rect = self.create_text()
    #     self.win.blit(text, rect)








class CharacterIcon:

    _folder = 'character_icons/'
    icon_size = (int(glob_var.display_width * .1), int(glob_var.display_height * .15))

    queued_to_be_attacked = None
    class_clickable = False

    def __init__(self, icon_name, player_num, icon_num):
        self.icon_name = icon_name
        self.player_num = player_num
        self.icon_num = icon_num

        self.img = self.resize_image()  # I have no idea how this is being called
        self.health = 100

    def get_x(self):
        if self.player_num == 1:
            x_location = glob_var.display_width * .025
        elif self.player_num == 2:
            x_location = glob_var.display_width * (7/8)
        else:
            return "invalid PLAYER number provided to Class Icon get_x method"
        return x_location

    def get_y(self):
        if self.icon_num == 1:
            y_location = glob_var.display_height / 5
        elif self.icon_num == 2:
            y_location = glob_var.display_height * (2 / 5)
        elif self.icon_num == 3:
            y_location = glob_var.display_height * (3 / 5)
        else:
            return "invalid ICON number provided to Class Icon get_y method"
        return y_location

    def get_position(self):
        x, y = self.get_x(), self.get_y()
        return x,y

    def get_image_from_string(self):
        try:
            path = self._folder + self.icon_name + ".jpg"
            img = pygame.image.load(path)
        except Exception as e:
            try:
                path = self._folder + self.icon_name + ".png"
                img = pygame.image.load(path)
            except Exception as e:
                return f"Couldn't find jpg nor png for icon {self.icon_name}."
        return img

    def load_image(self):
        img = self.get_image_from_string()
        return img

    def resize_image(self):
        img = self.load_image()
        resized = pygame.transform.scale(img, self.icon_size)
        return resized

    def highlight_image(self, img):
        img = img.convert()
        img.set_alpha(100)
        return img

    def click_status(self):  # This can be cleaned up
        mouse = pygame.mouse.get_pos()
        x, y = self.get_x(), self.get_y()
        size = self.icon_size[0]
        if (x + size) > mouse[0] > x and (y + size) > mouse[1] > y:
            return True
        else:
            return False

    def display_bar(self):
        bar_x, bar_y = self.get_x(), self.get_y() + self.icon_size[1] + (glob_var.display_height * 0.00625)
        bar_width = int(self.icon_size[0] * (self.health / 100))

        bar = pygame.Surface((bar_width, 10), pygame.SRCALPHA)
        bar.fill((255, 0, 0, 255))  # includes the alpha value

        bar_message = f"Health:  {self.health}"
        font = pygame.font.Font("freesansbold.ttf", int(1.8518518518518518e-05 * glob_var.display_area * .5))
        textsurf, textRect = create_textObject(bar_message, font)
        textRect.center = (bar_x + (self.icon_size[0] / 2), bar_y + (glob_var.display_height * 0.0225))

        glob_var.win.blit(bar, (bar_x, bar_y))
        glob_var.win.blit(textsurf, textRect)

    def display_image(self):
        img = self.img
        if Jutsu_Icon.class_isclicked:
            if GameManager.player1_turn and self.player_num == 2 or not GameManager.player1_turn and self.player_num == 1:
                img = self.highlight_image(img)

                if self.click_status():
                    CharacterIcon.class_clickable = True
                    click = pygame.mouse.get_pressed()
                    if click[0] == 1:
                        CharacterIcon.queued_to_be_attacked = self

        glob_var.win.blit(img, (self.get_x(), self.get_y()))
        self.display_bar()

    def check_health(self):
        if self.health <= 0:
            self.die()

    def die(self):
        input('death' + str(self.icon_name))



class Jutsu_Icon(CharacterIcon):

    _folder = 'jutsu_icons/'
    icon_size = (int(glob_var.display_width * 0.06666666666666667), int(glob_var.display_height * 0.1))

    class_clickable = False
    class_isclicked = False

    xOffset_from_character_icon = glob_var.display_width // 12
    queued_for_attack = None

    def __init__(self, icon_name, player_num, icon_num, parent_icon):
        super().__init__(icon_name, player_num, icon_num)
        self.parent_icon = parent_icon

    def get_x(self):
        x_p = self.parent_icon.get_x()
        if self.player_num == 1:
            x_p += (glob_var.display_width * .025)  # was 30
            x = x_p + (self.xOffset_from_character_icon * self.icon_num)
        elif self.player_num == 2:
            x = x_p - (self.xOffset_from_character_icon * self.icon_num)  # mirror effect
        else:
            return "invalid player number provided to jutsu_get_x"
        return x

    def get_y(self):
        y_p = self.parent_icon.get_y()
        y = y_p + (glob_var.display_height * 0.025)
        return y

    def display_image(self):
        x, y = self.get_x(), self.get_y()
        img = self.resize_image()

        if self.click_status():
            Jutsu_Icon.class_clickable = True

            img = img.convert()
            img.set_alpha(100)

            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                Jutsu_Icon.class_isclicked = True
                Jutsu_Icon.queued_for_attack = self

        if not Jutsu_Icon.class_clickable:
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                if CharacterIcon.class_clickable:
                    Jutsu_Icon.class_isclicked = False
                if not CharacterIcon.class_clickable:
                    Jutsu_Icon.queued_for_attack = None
                    Jutsu_Icon.class_isclicked = False
                    print("CLICKED AWAY")

        glob_var.win.blit(img, (x, y))
        self.display_name()

    def display_name(self):
        msg1 = self.icon_name
        msg2 = f"Damage: {self.get_damage()}"
        font = pygame.font.Font("freesansbold.ttf", int(2.2222222222222223e-05 * glob_var.display_area * .5))
        x, y = (self.get_x() + self.icon_size[0] / 2, self.get_y() + self.icon_size[1] + (glob_var.display_height * 0.0125))

        textsurf, textRect = create_textObject(msg1, font)
        textsurf2, textRect2 = create_textObject(msg2, font)
        textRect.center = (x,y)
        textRect2.center = (x, y + (glob_var.display_height * 0.01875))

        glob_var.win.blit(textsurf, textRect)
        glob_var.win.blit(textsurf2, textRect2)

    def get_damage(self):
        for item in jutsu_signs.names_of_characters:
            if list(item.values())[0] == self.parent_icon.icon_name:
                return item[self.icon_name][1]
        else:
            return "Character not found in chars list from damage signs"




# -----------------------------------------------------------------------------------------------
# WEAVING LOOP CLASSES
# -----------------------------------------------------------------------------------------------
class VisualCue:

    box_color = (150, 150, 150)
    box_outline = (200, 200, 200)

    def __init__(self, msg, w, h, text_color, typ, seq, win, x=None, y=None, image_str=None):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r, self.g, self.b = text_color
        self.typ = typ
        self.seq = seq
        self.win = win
        self.image_str = image_str

        if self.typ == 'header':
            self.font = pygame.font.Font("freesansbold.ttf", int(0.00014814814814814815 * glob_var.display_area * .5))
        elif self.typ == 'prompt':
            self.font = pygame.font.Font("freesansbold.ttf", int(7.407407407407407e-05 * glob_var.display_area * .5))
        elif self.typ == 'jutsu':
            self.font = pygame.font.Font("freesansbold.ttf", int(5.555555555555556e-05 * glob_var.display_area * .5))
        else:
            self.font = pygame.font.Font("freesansbold.ttf", int(9.259259259259259e-05 * glob_var.display_area * .5))

    def get_x(self):
        if self.typ == 'header':
            self.x = glob_var.display_width // 2 - (self.w // 2)
        elif self.typ == 'prompt':
            self.x = glob_var.display_width * ((len(self.seq) + 1) / 6) - (glob_var.display_width * 0.125)
        elif self.typ == 'jutsu':
            self.x = glob_var.display_width * (len(self.seq) / 6) - (glob_var.display_width * 0.083333333333)
        elif self.typ == 'image':
            self.x = glob_var.display_width * (len(self.seq) / 6) - (glob_var.display_width * 0.1)
        return self.x

    def get_y(self):
        if self.typ == 'header':
            self.y = (glob_var.display_height * 0.025)
        elif self.typ == 'prompt':
            self.y = (glob_var.display_height * 0.1625)
        elif self.typ == 'jutsu':
            self.y = (glob_var.display_height * 0.3)
        elif self.typ == 'image':
            self.y = (glob_var.display_height * 0.3625)
        return self.y

    def text_objects(self):
        textsurface = self.font.render(self.msg, True, (self.r, self.g, self.b))
        return textsurface, textsurface.get_rect()

    def create_text(self):
        if self.x is None:
            self.x = self.get_x()
        if self.y is None:
            self.y = self.get_y()
        textsurf, textRect = self.text_objects()
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
        return textsurf, textRect

    def display_image(self):
        location = (self.get_x(), self.get_y())
        img = pygame.image.load(self.image_str)
        self.win.blit(img, location)

    def create_cue(self):
        if self.x is None:
            self.x = self.get_x()
        if self.y is None:
            self.y = self.get_y()
        button = pygame.draw.rect(self.win, self.box_color, (self.x, self.y, self.w, self.h))
        text, rect = self.create_text()
        self.win.blit(text, rect)
