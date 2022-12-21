

class Piece():
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def move(self, row, col):
        self.row = row
        self.col = col


class Fox(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.type = "Fox"

    def allowed_move(self, board):
        pass

class Hen(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.type = "Hen"

    def allowed_move(self, board):
        pass