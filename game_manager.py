
class GameManager:
    player1_turn = True
    end_game = False

    @staticmethod
    def change_turn():
        GameManager.player1_turn = not GameManager.player1_turn

    @staticmethod
    def check_characters(all_characters):
        if all_characters[0].dead and all_characters[1].dead and all_characters[2].dead:
            GameManager.player2_wins()
        elif all_characters[3].dead and all_characters[4].dead and all_characters[5].dead:
            GameManager.player1_wins()

    @staticmethod
    def player2_wins():
        print('PLAYER 2 WINS')
        import game_ops
        game_ops.end_game(2)

    @staticmethod
    def player1_wins():
        print('PLAYER 1 WINS')
        import game_ops
        game_ops.end_game(1)

