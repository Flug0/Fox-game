from look_ahead_ai.minimax_algo import Minimax_algo
from look_ahead_ai.node import Node

class Run:
    def __init__(self, game) -> None:
        self.game = game
        self.board = game.board
        self.win = game.win
        self.run()

    def run(self):
        minimax_class = Minimax_algo(self.game)
        minInt = float("-inf")
        maxInt = float("inf")
        while True:
            thisNode = Node(self.game)
            self.win.update(self.board)
            if not self.foxs_turn:
                self.move_on_valid_move(self.win.selected_pos, self.win.direction)
            else:
                _, newBoard = minimax_class.minimax(thisNode, 7, minInt, maxInt, True)
                self.board = newBoard
                print("Hen moved")
            fox_won, hen_won = self.check_win()
            if fox_won or hen_won:
                break
        print("Someone won, game ended")