
class Node:
    def __init__(self, game):
        self.game = game
        self.children = []
        self.evaluation = None

    def add_children(self):
        for row in range(len(self.game.board.slots)):
            for column in range(len(self.game.board.slots[row])):
                if self.game.board.slots[row][column] is not None and self.game.board.slots[row][column].type != "Empty":
                    for direction in range(8):
                        child_game = self.game.copy()
                        valid_move = child_game.move_on_valid_move((row, column), direction)
                        if valid_move:
                            self.children.append(Node(child_game))

