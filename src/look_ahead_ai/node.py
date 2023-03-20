
class Node:
    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.children = []
        self.add_children()
        # self.move = None

    def add_children(self):
        for direction in range(8):
            for row in range(len(self.board.slots)):
                for column in range(len(self.board.slots[row])):
                    if 0 <= row <= len(self.board.neighbor_matrix) - 1 \
                            and 0 <= column <= len(self.board.neighbor_matrix[row]) - 1 \
                            and self.board.slots[row][column] is not None:
                        print("Tried a move")
                        valid_move, newBoard = self.game.move_on_valid_move((row, column), direction)
                        if valid_move:
                            newNode = Node(newBoard)
                            self.children.append(newNode)
                            # self.move = [(row, column), direction]
