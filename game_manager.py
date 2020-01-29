

class GameManager:
    player_turn = True

    @staticmethod
    def change_turn():
        GameManager.player_turn = not GameManager.player_turn

