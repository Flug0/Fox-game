from look_ahead_ai.ai import AI
from window import Window
import time


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
                valid_move, endPos = self.game.check_valid_move(self.win.selected_pos, self.win.direction)
                if valid_move:
                    self.game.move(self.win.selected_pos, endPos)
            else:
                t0 = time.time()
                self.game = ai.get_best_move(3, self.game, self.win)
                t1 = time.time()
                print("AI time:", t1-t0)
            fox_won, hen_won = self.game.check_win()
            if fox_won or hen_won:
                break
        print("Someone won, game ended")
