import global_variables as glob_var


class GameManager:
    player1_turn = True
    end_game = False
    winner = None
    active_game = False

    @staticmethod
    def change_turn():
        GameManager.player1_turn = not GameManager.player1_turn

    @staticmethod
    def check_characters():
        if CharacterManager.all_characters[0].dead and CharacterManager.all_characters[1].dead and CharacterManager.all_characters[2].dead:
            GameManager.end_game = True
            GameManager.winner = 2
        elif CharacterManager.all_characters[3].dead and CharacterManager.all_characters[4].dead and CharacterManager.all_characters[5].dead:
            GameManager.end_game = True
            GameManager.winner = 1


class CharacterManager:
    player1_character1_icon = None
    player1_character2_icon = None
    player1_character3_icon = None
    player2_character1_icon = None
    player2_character2_icon = None
    player2_character3_icon = None
    all_characters = None

    mouse_cleared = True
    queued_to_be_attacked = None


class JutsuManager:
    player1_character1_jutsu1_icon = None
    player1_character1_jutsu2_icon = None
    player1_character1_jutsu3_icon = None
    player1_character1_jutsu4_icon = None
    player1_character2_jutsu1_icon = None
    player1_character2_jutsu2_icon = None
    player1_character2_jutsu3_icon = None
    player1_character2_jutsu4_icon = None
    player1_character3_jutsu1_icon = None
    player1_character3_jutsu2_icon = None
    player1_character3_jutsu3_icon = None
    player1_character3_jutsu4_icon = None
    player2_character1_jutsu1_icon = None
    player2_character1_jutsu2_icon = None
    player2_character1_jutsu3_icon = None
    player2_character1_jutsu4_icon = None
    player2_character2_jutsu1_icon = None
    player2_character2_jutsu2_icon = None
    player2_character2_jutsu3_icon = None
    player2_character2_jutsu4_icon = None
    player2_character3_jutsu1_icon = None
    player2_character3_jutsu2_icon = None
    player2_character3_jutsu3_icon = None
    player2_character3_jutsu4_icon = None

    mouse_cleared = True
    queued_for_attack = None


def easy_difficulty():
    glob_var.easymode = True
    glob_var.hardmode = False


def hard_difficulty():
    glob_var.easymode = False
    glob_var.hardmode = True


def show_signs():
    glob_var.showsigns = True


def hide_signs():
    glob_var.showsigns = False

