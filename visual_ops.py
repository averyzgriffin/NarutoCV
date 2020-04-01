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


def get_jutsu_selected_visual(jutsu):
    visual_cue = TextCue(str(jutsu.get_jutsu_signs()), black, 50, glob_var.display_width // 2, glob_var.display_height * 7/8)

    selection_text = HeaderText(msg="You have selected: " + str(jutsu.jutsu_icon_name), text_color=black, size=50, x=None, y=None)
    selection_text.display_text()

    pygame.display.update()

    time.sleep(3)
    return visual_cue


# ------------------------------------------------------------------------------
# GAME LOOP CLASSES
# ------------------------------------------------------------------------------

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

        self.x = self.get_x()
        self.y = self.get_y()

        self.bar, self.bar_x, self.bar_y, self.bar_message = self.create_bar()

    def get_x(self):
        if self.player_num == 1:
            x_location = glob_var.display_width * .025
        elif self.player_num == 2:
            x_location = glob_var.display_width * (7/8)
        else:
            return "invalid PLAYER number provided to Class Icon get x method"
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


    def get_image_from_string(self):
        try:
            path = self._folder + self.icon_name + ".jpg"
            img = pygame.image.load(path)
        except Exception:
            try:
                path = self._folder + self.icon_name + ".png"
                img = pygame.image.load(path)
            except Exception:
                return f"Couldn't find jpg nor png for icon {self.icon_name}."
        return img

    def load_image(self):
        img = self.get_image_from_string()
        return img

    def resize_image(self):
        img = self.load_image()
        resized = pygame.transform.scale(img, self.icon_size).convert()
        return resized

    def click_status(self):  # This can be cleaned up
        mouse = pygame.mouse.get_pos()
        size = self.icon_size[0]
        if (self.x + size) > mouse[0] > self.x and (self.y + size) > mouse[1] > self.y:
            return True
        else:
            return False

    def create_bar(self):
        bar_x, bar_y = self.x, self.y + self.icon_size[1] + (glob_var.display_height * 0.00625)
        bar_width = int(self.icon_size[0] * (self.health / 100))

        bar = pygame.Surface((bar_width, 10), pygame.SRCALPHA)
        bar.fill((255, 0, 0, 255))
        bar_message = TextCue(f"Health:  {self.health}", black, (glob_var.display_area // 86283),(bar_x + (self.icon_size[0] / 2)), bar_y + (glob_var.display_height * 0.0225))

        return bar, bar_x, bar_y, bar_message

    def display_bar(self):
        glob_var.win.blit(self.bar, (self.bar_x, self.bar_y))
        self.bar_message.display_text()

    def display_image(self):
        if Jutsu_Icon.class_isclicked:
            if GameManager.player1_turn and self.player_num == 2 or not GameManager.player1_turn and self.player_num == 1:
                self.img.set_alpha(100)

                if self.click_status():
                    CharacterIcon.class_clickable = True
                    click = pygame.mouse.get_pressed()
                    if click[0] == 1:
                        CharacterIcon.queued_to_be_attacked = self

        glob_var.win.blit(self.img, (self.x, self.y))
        self.display_bar()

    def check_health(self):
        if self.health <= 0:
            self.die()

    def die(self):
        input('death' + str(self.icon_name))



class Jutsu_Icon(CharacterIcon):

    _folder = 'jutsu_icons/'
    icon_size = (int(glob_var.display_width * (1/15)), int(glob_var.display_height * 0.1))
    offset_from_character_icon = glob_var.display_width // 12

    class_clickable = False
    class_isclicked = False
    queued_for_attack = None

    def __init__(self, icon_name, player_num, icon_num, parent_icon):
        self.parent_icon = parent_icon
        super().__init__(icon_name, player_num, icon_num)

        self.x = self.get_x()
        self.y = self.get_y()

        self.msg1, self.msg2 = self.create_name()


    def get_x(self):
        x_p = self.parent_icon.x
        if self.player_num == 1:
            x_p += (glob_var.display_width * .025)  # was 30
            x = x_p + (self.offset_from_character_icon * self.icon_num)
        elif self.player_num == 2:
            x = x_p - (self.offset_from_character_icon * self.icon_num)  # mirror effect
        else:
            return "invalid player number provided to jutsu get x"
        return x

    def get_y(self):
        y_p = self.parent_icon.get_y()
        y = y_p + (glob_var.display_height * 0.025)
        return y

    def create_name(self):
        x, y = (self.x + self.icon_size[0] / 2, self.y + self.icon_size[1] + (glob_var.display_height * 0.0125))
        msg1 = TextCue(self.icon_name, black, 14, x, y)
        msg2 = TextCue(f"Damage: {self.get_damage()}", black, 14, x, y + (glob_var.display_height * 0.01875))

        return msg1, msg2

    def display_name(self):
        self.msg1.display_text()
        self.msg2.display_text()


    def get_damage(self):
        for item in jutsu_signs.names_of_characters:
            if list(item.values())[0] == self.parent_icon.icon_name:
                return item[self.icon_name][1]
        else:
            return "Character not found in chars list from damage signs"

    def display_image(self):

        if self.click_status():
            Jutsu_Icon.class_clickable = True

            self.img.set_alpha(100)

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

        glob_var.win.blit(self.img, (self.x, self.y))
        self.display_name()


class TextCue:

    def __init__(self, msg, text_color, size, x, y):
        self.msg = msg
        self.r, self.g, self.b = text_color
        self.size = size
        self.x = x
        self.y = y

        self.font = pygame.font.Font("freesansbold.ttf", int(self.size))

    def create_text(self):
        textsurface = self.font.render(self.msg, True, (self.r, self.g, self.b))
        return textsurface, textsurface.get_rect()

    def display_text(self):
        text, rect = self.create_text()
        rect.center = (self.x, self.y)
        glob_var.win.blit(text, rect)


class HeaderText(TextCue):

    def __init__(self, msg, text_color, size, x, y):
        super().__init__(msg, text_color, size, x, y)

        self.x = glob_var.display_width // 2
        self.y = glob_var.display_height / 8.35

        self.font = pygame.font.Font("freesansbold.ttf", int(self.size))


class PromptText(TextCue):

    def __init__(self, msg, text_color, size, seq, x, y):
        super().__init__(msg, text_color, size, x, y)

        self.seq = seq
        self.x = ((len(self.seq) + 1) / 8) * glob_var.display_width
        self.y = (glob_var.display_height // 4.175)

        self.font = pygame.font.Font("freesansbold.ttf", int(self.size))


class JutsuText(TextCue):

    def __init__(self, msg, text_color, size, seq, x, y):
        self.seq = seq
        super().__init__(msg, text_color, size, x, y)

        self.x = ((len(self.seq)) / 8) * glob_var.display_width
        self.y = (glob_var.display_height // 3.25)

        self.font = pygame.font.Font("freesansbold.ttf", int(self.size))






# -----------------------------------------------------------------------------------------------
# WEAVING LOOP CLASSES
# -----------------------------------------------------------------------------------------------
# class VisualCue:
#
#     box_color = (150, 150, 150)
#     box_outline = (200, 200, 200)
#
#     def __init__(self, msg, w, h, text_color, typ, seq, x=None, y=None):
#         self.msg = msg
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#         self.r, self.g, self.b = text_color
#         self.typ = typ
#         self.seq = seq
#
#         if self.typ == 'header':
#             self.font = pygame.font.Font("freesansbold.ttf", int(0.00014814814814814815 * glob_var.display_area * .5))
#         elif self.typ == 'prompt':
#             self.font = pygame.font.Font("freesansbold.ttf", int(7.407407407407407e-05 * glob_var.display_area * .5))
#         elif self.typ == 'jutsu':
#             self.font = pygame.font.Font("freesansbold.ttf", int(5.555555555555556e-05 * glob_var.display_area * .5))
#         else:
#             self.font = pygame.font.Font("freesansbold.ttf", int(9.259259259259259e-05 * glob_var.display_area * .5))
#
#     def get_x(self):
#         if self.typ == 'header':
#             self.x = glob_var.display_width // 2 - (self.w // 2)
#         elif self.typ == 'prompt':
#             self.x = glob_var.display_width * ((len(self.seq) + 1) / 6) - (glob_var.display_width * 0.125)
#         elif self.typ == 'jutsu':
#             self.x = glob_var.display_width * (len(self.seq) / 6) - (glob_var.display_width * 0.083333333333)
#         return self.x
#
#     def get_y(self):
#         if self.typ == 'header':
#             self.y = (glob_var.display_height * 0.025)
#         elif self.typ == 'prompt':
#             self.y = (glob_var.display_height * 0.1625)
#         elif self.typ == 'jutsu':
#             self.y = (glob_var.display_height * 0.3)
#         return self.y
#
#     def text_objects(self):
#         textsurface = self.font.render(self.msg, True, (self.r, self.g, self.b))
#         return textsurface, textsurface.get_rect()
#
#     def create_text(self):
#         if self.x is None:
#             self.x = self.x
#         if self.y is None:
#             self.y = self.get_y()
#         textsurf, textRect = self.text_objects()
#         textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
#         return textsurf, textRect
#
#     def create_cue(self):
#         if self.x is None:
#             self.x = self.get_x()
#         if self.y is None:
#             self.y = self.get_y()
#         button = pygame.draw.rect(glob_var.win, self.box_color, (self.x, self.y, self.w, self.h))
#         text, rect = self.create_text()
#         glob_var.win.blit(text, rect)


# class ImageCue(VisualCue):
#     def __init__(self, image_str):
#         self.image_str = image_str
#
#     def display_image(self):
#         location = (self.get_x(), self.get_y())
#         img = pygame.image.load(self.image_str).convert()
#         glob_var.win.blit(img, location)
#
#         elif self.typ == 'image':
#             self.x = glob_var.display_width * (len(self.seq) / 6) - (glob_var.display_width * 0.1)
#
#         elif self.typ == 'image':
#             self.y = (glob_var.display_height * 0.3625)

