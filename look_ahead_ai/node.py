from src.window import Window
from src.game import Game

class Node:
    def __init__(self, board):
        self.board = board
        self.children = []
        self.add_children()

    def add_children(self):
        for direction in range(8):
            for row in range(len(self.board.slots)):
                for column in range(len(self.board.slots[row])):
                    #TODO: Check all valid moves and add them to self.children
                    pass

