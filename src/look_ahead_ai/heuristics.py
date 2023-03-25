import math
"""
Maximising player = Hen
Minimising player = Fox
"""

class Heuristics:
    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.points = 0
        self.calculate_heuristic()

    def calculate_heuristic(self):
        self.points = 0
        self.winning_position()
        self.hens_alive()
        self.foxes_alive()
        self.hens_in_goal()
        return self.points

    def winning_position(self):
        fox_won, sheep_won = self.game.check_win()
        if fox_won:
            self.points = -1000
        elif sheep_won:
            self.points = 1000

    def hens_alive(self):
        self.points += (10*self.game.hens)

    def foxes_alive(self):
        self.points -= (10*self.game.foxes)

    def hens_in_goal(self):
        self.points += (3*self.board.get_hens_in_nest())

    def square_points(self):
        # Adding point the further down the board a hen gets
        # Don't really care about the foxes now, since they mainly care about catching chickens
        for [row, column] in range(self.board.hens_position):
            self.points += row
            self.points += math.floor(abs(3.5-column)) # 3 is middle
