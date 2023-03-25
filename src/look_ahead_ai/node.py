import itertools


class Node:
    def __init__(self, game):
        self.game = game
        self.children = []
        self.evaluation = None

    def add_children(self):
        #pieceList = list(itertools.chain(self.game.board.fo5xs_position, self.game.board.hens_position))
        pieceList = self.game.board.foxs_position if self.game.foxs_turn else self.game.board.hens_position
        for [row, column] in pieceList:
            for direction in range(8):
                valid_move, endPos = self.game.check_valid_move((row, column), direction)
                if valid_move:
                    child_game = self.game.copy()
                    child_game.move((row, column), endPos)
                    self.children.append(Node(child_game))
        #print("Amount of children:", len(self.children))
