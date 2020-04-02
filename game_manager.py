
class GameManager:
    player1_turn = True
    end_game = False
    winner = None

    @staticmethod
    def change_turn():
        GameManager.player1_turn = not GameManager.player1_turn

    @staticmethod
    def check_characters():
        if CharacterManager.all_characters[0].dead and CharacterManager.all_characters[1].dead and CharacterManager.all_characters[2].dead:
            # GameManager.player2_wins()
            GameManager.end_game = True
            GameManager.winner = 2
        elif CharacterManager.all_characters[3].dead and CharacterManager.all_characters[4].dead and CharacterManager.all_characters[5].dead:
            # GameManager.player1_wins()
            GameManager.end_game = True
            GameManager.winner = 1

    @staticmethod
    def player2_wins():
        print('PLAYER 2 WINS')
        import main_game
        main_game.end_game(2)

    @staticmethod
    def player1_wins():
        print('PLAYER 1 WINS')
        import main_game
        main_game.end_game(1)


class CharacterManager:
    player1_character1_icon = None
    player1_character2_icon = None
    player1_character3_icon = None
    player2_character1_icon = None
    player2_character2_icon = None
    player2_character3_icon = None
    all_characters = None


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
2