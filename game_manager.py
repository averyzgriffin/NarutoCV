

class GameManager:
    player1_turn = True

    @staticmethod
    def change_turn():
        GameManager.player1_turn = not GameManager.player1_turn

