from look_ahead_ai.ai import AI
from window import Window


class Run:
    def __init__(self, game):
        self.game = game
        self.win = Window(self.game.board)
        self.run()

    def run(self):
        ai = AI()
        while True:
            self.win.update(self.game.board)
            if not self.game.foxs_turn:
                self.game.move_on_valid_move(self.win.selected_pos, self.win.direction)
            else:
                self.game = ai.get_best_move(3, self.game, self.win)
            fox_won, hen_won = self.game.check_win()
            if fox_won or hen_won:
                break
        print("Someone won, game ended")
