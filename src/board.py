from piece import *
import copy

class Board():
    def __init__(self, board=None):
        if board is None:
            self.layout = [3, 3, 7, 7, 7, 3, 3]
            self.slots = [[None for _ in range(max(self.layout))] for _ in range(len(self.layout))]
            # posX, posY, direction from slot to neighbor (0-7, 0 = Up, 1 = Up/Right, 2 = Right...)
            self.neighbor_matrix = [[[ ] for _ in range(max(self.layout))] for _ in range(len(self.layout))]
            self.hens_position = []
            self.foxs_position = []

            self.set_neighbor_matrix()
            self.set_initial_peices()
        else:
            #self.layout = board.layout.copy()
            self.layout = board.layout
            self.slots = copy.deepcopy(board.slots)
            #self.neighbor_matrix = copy.deepcopy(board.neighbor_matrix)
            self.neighbor_matrix = board.neighbor_matrix
            self.hens_position = board.hens_position.copy()
            self.foxs_position = board.foxs_position.copy()

    def set_neighbor_matrix(self):
        for row in range(len(self.layout)):
            offset = int((7 - self.layout[row]) / 2)
            for col in range(offset, self.layout[row] + offset):
                # Set right/left neighbors
                if col != offset:
                    self.neighbor_matrix[row][col].append((row, col-1, 6))
                if col != self.layout[row]+offset-1:
                    self.neighbor_matrix[row][col].append((row, col+1, 2))
                # Set up/down neighbors
                if row != 0:
                    if not (row == 2 and (col < 2 or col > 4)):
                        self.neighbor_matrix[row][col].append((row-1, col, 0))
                if row != len(self.layout)-1:
                    if not (row == 4 and (col < 2 or col > 4)):
                        self.neighbor_matrix[row][col].append((row+1, col, 4))
                # Set diagonal neighbors
                if col%2 == 1 and row%2 == 1:
                    self.__set_cross_neighbors(row, col)
    
    def set_initial_peices(self):
        x, y = 2, 0
        for i in range(2):
            for j in range(3):
                self.slots[y][x] = Hen(y, x)
                self.hens_position.append([y, x])
                x += 1
            y += 1
            x = 2
        for i in range(2):
            x = 0
            for j in range(7):
                self.slots[y][x] = Hen(y, x)
                self.hens_position.append([y, x])
                x += 1
            y += 1
        x = 0
        for j in range(7):
            self.slots[y][x] = Empty(y, x)
            x += 1
        y += 1
        x = 2
        for j in range(3):
            self.slots[y][x] = Empty(y, x)
            x += 1
        y += 1
        x = 2
        self.slots[y][x] = Fox(y, x)
        self.foxs_position.append([y, x])
        self.slots[y][x+1] = Empty(y, x+1)
        self.slots[y][x+2] = Fox(y, x+2)
        self.foxs_position.append([y, x+2])
        #print(self.slots)

    def __set_cross_neighbors(self, row, col):
        self.neighbor_matrix[row][col].append((row-1, col-1, 7))
        self.neighbor_matrix[row][col].append((row-1, col+1, 1))
        self.neighbor_matrix[row][col].append((row+1, col-1, 5))
        self.neighbor_matrix[row][col].append((row+1, col+1, 3))

        self.neighbor_matrix[row-1][col-1].append((row, col, 3))
        self.neighbor_matrix[row+1][col-1].append((row, col, 1))
        self.neighbor_matrix[row-1][col+1].append((row, col, 5))
        self.neighbor_matrix[row+1][col+1].append((row, col,7))
    
    def move_piece(self, row, col, row2, col2):
        """Moves piece from one slot to another, if second slot not empty, return false"""
        #print("Moving piece from", row, col, "to", row2, col2)
        if self.slots[row2][col2] is None:
            return False
        if not self.slots[row2][col2].type == "Empty":
            return False
        if self.slots[row][col].type == "Empty":
            return False
        # To keep track of where the fox or hens move to
        # This is for Heuristics
        fromType = self.slots[row][col].type
        if fromType == "Fox":
            self.foxs_position = [[row2, col2] if position == [row, col] else position for position in self.foxs_position]
        elif fromType == "Hen":
            self.hens_position = [[row2, col2] if position == [row, col] else position for position in self.hens_position]
        # This moves the pieces on the board
        self.slots[row][col].move(row2, col2)
        self.slots[row2][col2] = self.slots[row][col]
        self.slots[row][col] = Empty(row, col)
        return True

    def set_slot(self, row, col, piece):
        self.slots[row][col] = piece
    
    def get_slot(self, row, col):
        if row == -1 or col == -1:
            return Empty(-1,-1)
        return self.slots[row][col]

    def get_hens_in_nest(self):
        count = 0
        for i in range(3):
            if isinstance(self.slots[-3][i+2], Hen):
                count += 1
        for i in range(2):
            for j in range(3):
                if isinstance(self.slots[-1-i][j+2], Hen):
                    count += 1
        return(count)
