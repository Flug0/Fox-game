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
        self.square_points()
        return self.points

    def winning_position(self):
        fox_won, hens_won = self.game.check_win()
        if fox_won:
            self.points = -10000
        elif hens_won:
            self.points = 10000

    def hens_alive(self):
        self.points += (10*self.game.hens)

    def foxes_alive(self):
        self.points -= (10*self.game.foxes)

    def hens_in_goal(self):
        self.points += (3*self.board.get_hens_in_nest())

    def square_points(self):
        # Adding point the further down the board a hen gets
        # Don't really care about the foxes now, since they mainly care about catching chickens
        for [row, column] in self.board.hens_position:
            self.points += row*3
            #self.points += math.floor(abs(3.5-column)) # 3 is middle
