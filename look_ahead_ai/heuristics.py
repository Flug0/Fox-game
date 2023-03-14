import src.game

"""
Maximising player = Sheep
Minimising player = Fox
"""


class Heuristics:
    def __init__(self):
        self.game = src.game.Game()
        self.board = self.game.board
        self.points = 0
        self.calculate_heuristic()

    def calculate_heuristic(self):
        self.winning_position()
        self.hens_alive()
        self.foxes_alive()
        self.hens_in_goal()

    def winning_position(self):
        fox_won, sheep_won = self.game.check_win()
        if fox_won:
            self.points = -1000
        elif sheep_won:
            self.points = 1000

    def hens_alive(self):
        for hen in range(self.game.hens):
            self.points += 1

    def foxes_alive(self):
        for fox in range(self.game.foxes):
            self.points -= 10

    def hens_in_goal(self):
        for hens_in_nest in range(self.board.get_hens_in_nest()):
            self.points += 1
