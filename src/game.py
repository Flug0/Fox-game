from window import Window
from board import Board
from piece import Piece, Fox, Hen

class Game():
    def __init__(self):
        self.win = Window()
        self.board = Board()
    
    def get_move(self):
        pass
    
    def run(self):
        while True:
            self.win.update(self.board)