import pygame
import time
import global_variables as glob_var
import jutsu_signs_damage
from game_manager import GameManager
import game_manager


black = (0,0,0)
pygame.init()


# --------------------------------------------------------------------------------------------------------------
# Visual FUNCTIONS
# --------------------------------------------------------------------------------------------------------------
def create_textObject(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()


def get_selected_jutsu_prompt(jutsu):  # TODO I don't like the name of this function.
    selection_text1 = HeaderText(msg="You have selected " + str(jutsu.jutsu_icon_name).upper(), text_color=glob_var.black, size=glob_var.display_width/30.4, x=None, y=None)
    selection_text2 = HeaderText(msg="You have selected " + str(jutsu.jutsu_icon_name).upper(), text_color=glob_var.orange, size=glob_var.display_width/31, x=None, y=None)
    selection_text1.y = glob_var.display_height / 2
    selection_text2.y = glob_var.display_height / 2
    selection_text1.display_text()
    selection_text2.display_text()

    pygame.display.update()
    time.sleep(3)


# ------------------------------------------------------------------------------
# GAME LOOP CLASSES
# ------------------------------------------------------------------------------

class CharacterIcon:

    _folder = 'character_icons/'
    icon_size = (int(glob_var.display_width * .075), int(glob_var.display_width * .075))

    def __init__(self, icon_name, player_num, icon_num):
        self.icon_name = icon_name
        self.player_num = player_num
        self.icon_num = icon_num

        self.img = self.resize_image()
        self.health = 100

        self.x = self.get_x()
        self.y = self.get_y()

        self.bar, self.bar_x, self.bar_y, self.bar_message = self.create_bar()

        self.dead = False

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
                return f"EXCEPTION ---- Couldn't find jpg nor png for icon {self.icon_name}."
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
        bar_width = abs(int(self.icon_size[0] * (self.health / 100)))

        bar = pygame.Surface((bar_width, glob_var.display_height/83.5), pygame.SRCALPHA)
        bar.fill((255, 0, 0, 255))
        bar_message = TextCue(f"Health:  {self.health}", black, (glob_var.display_width / 103),(bar_x + (self.icon_size[0] / 2)), bar_y + (glob_var.display_height * 0.0225))

        return bar, bar_x, bar_y, bar_message

    def display_bar(self):
        glob_var.win.blit(self.bar, (self.bar_x, self.bar_y))
        self.bar_message.display_text()

    def display_image(self):
        if not self.dead:
            if game_manager.JutsuManager.queued_for_attack != "":
                if GameManager.player1_turn and self.player_num == 2 or not GameManager.player1_turn and self.player_num == 1:
                    self.img.set_alpha(100)

                    if self.click_status():
                        self.img.set_alpha(255)
                        game_manager.CharacterManager.mouse_cleared = False

                        click = pygame.mouse.get_pressed()
                        if click[0] == 1:
                            game_manager.CharacterManager.queued_to_be_attacked = self
            else:
                self.img.set_alpha(255)

        glob_var.win.blit(self.img, (self.x, self.y))
        self.display_bar()

    def check_health(self):
        if self.health <= 0:
            self.die()

    def die(self):
        print('DEAD: ' + str(self.icon_name))
        self.health = 0
        self.dead = True
        self.img = pygame.transform.scale(pygame.image.load('character_icons/silverbox.jpg'), self.icon_size).convert()


class Jutsu_Icon(CharacterIcon):

    _folder = 'jutsu_icons/'
    icon_size = (int(glob_var.display_width * (1/15)), int(glob_var.display_height * 0.1))
    offset_from_character_icon = glob_var.display_width // 12

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
        msg1 = TextCue(self.icon_name, black, glob_var.display_width/112, x, y)
        msg2 = TextCue(f"Damage: {self.get_damage()}", black, glob_var.display_width/112, x, y + (glob_var.display_height * 0.01875))

        return msg1, msg2

    def display_name(self):
        self.msg1.display_text()
        self.msg2.display_text()

    def get_damage(self):  # TODO I think I can eventually merge this with the same function in game_ops. Not sure.
        for item in jutsu_signs_damage.names_of_characters:
            if list(item.values())[0] == self.parent_icon.icon_name:
                return item[self.icon_name][1]
        else:
            return "Character not found in chars list from damage signs"

    def display_image(self):
        if not self.parent_icon.dead:

            if self.click_status():
                game_manager.JutsuManager.mouse_cleared = False

                self.img.set_alpha(100)

                click = pygame.mouse.get_pressed()
                if click[0] == 1:
                    game_manager.JutsuManager.queued_for_attack = self


            if not self.click_status():
                self.img.set_alpha(255)

            glob_var.win.blit(self.img, (self.x, self.y))
            self.display_name()


class Button:

    def __init__(self, x, y, w, h, msg='', destination=None, highlight=True, customfont=0):
        self.x = x - w // 2
        self.y = y - h // 2
        self.w = w
        self.h = h
        self.msg = msg
        self.destination = destination
        self.highlight = highlight
        self.customfont = customfont

        self.boxcolor = glob_var.orange
        self.boxoutline = glob_var.black
        self.textcolor = glob_var.white
        self.textsize = self.w // 7

        self.text = self.create_text()

    def create_text(self):
        if self.customfont != 0:
            text = TextCue(self.msg, self.textcolor, self.customfont, self.x + self.w // 2, self.y + self.h // 2)
        else:
            text = TextCue(self.msg, self.textcolor, self.textsize, self.x + self.w // 2, self.y + self.h // 2)
        return text

    def click_status(self):  # This can be cleaned up
        mouse = pygame.mouse.get_pos()
        if (self.x + self.w) > mouse[0] > self.x and (self.y + self.h) > mouse[1] > self.y:
            return True
        else:
            return False

    def display_button(self):

        pygame.draw.rect(glob_var.win, self.boxoutline, (self.x-2, self.y-2, self.w+4, self.h+4), 0)

        if self.click_status() and self.highlight:
            pygame.draw.rect(glob_var.win, (255,207,158), (self.x, self.y, self.w, self.h), 0)

            click = pygame.mouse.get_pressed()
            if click[0] == 1 and self.destination is not None:
                self.destination()

        else:
            pygame.draw.rect(glob_var.win, self.boxcolor, (self.x, self.y, self.w, self.h), 0)

        if self.msg != '':
            self.text.display_text()



class TextCue:

    def __init__(self, msg, text_color, size, x, y):
        self.msg = msg
        self.r, self.g, self.b = text_color
        self.size = size
        self.x = x
        self.y = y

        self.font = pygame.font.Font("freesansbold.ttf", int(self.size))

        self.text, self.rect = self.create_text()

    def create_text(self):
        textsurface = self.font.render(self.msg, True, (self.r, self.g, self.b))
        return textsurface, textsurface.get_rect()

    def display_text(self):
        self.rect.center = (self.x, self.y)
        glob_var.win.blit(self.text, self.rect)


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


class Picture:

    def __init__(self, file_name, x, y, w, h, border=''):
        self.file_name = file_name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.border = border

        self.img = self.load_image()  # I have no idea how this is being called

    def load_image(self):
        img = self.get_image_from_string()
        img = self.resize_image(img)
        return img

    def get_image_from_string(self):
        try:
            img = pygame.image.load(self.file_name)
        except Exception:
            return f"Couldn't image {self.file_name}."
        return img

    def resize_image(self, img):
        resized = pygame.transform.scale(img, (self.w, self.h)).convert()
        return resized

    def display_image(self):
        if self.border != '':
            pygame.draw.rect(glob_var.win, glob_var.orange, (self.x - self.w//2 - 3, self.y - self.h//2 - 3, self.w + 6, self.h + 6), 0)

        glob_var.win.blit(self.img, (self.x - self.w // 2, self.y - self.h // 2))
