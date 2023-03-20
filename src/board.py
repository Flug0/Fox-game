from piece import *

class Board():
    def __init__(self):
        self.layout = [3, 3, 7, 7, 7, 3, 3]
        self.slots = [[None for _ in range(max(self.layout))] for _ in range(len(self.layout))]
        # posX, posY, direction from slot to neighbor (0-7, 0 = Up, 1 = Up/Right, 2 = Right...)
        self.neighbor_matrix = [[[ ] for _ in range(max(self.layout))] for _ in range(len(self.layout))]

        self.set_neighbor_matrix()
        self.set_initial_peices()


    def set_neighbor_matrix(self):
        for row in range(len(self.layout)):
            offset = int((7 - self.layout[row]) / 2)
            for col in range(offset, self.layout[row] + offset):
                # Set right/left neighbors
                if col != offset:
                    self.neighbor_matrix[row][col].append((col-1,row,6))
                if col != self.layout[row]+offset-1:
                    self.neighbor_matrix[row][col].append((col+1,row,2))
                # Set up/down neighbors
                if row != 0:
                    if not (row == 2 and (col < 2 or col > 4)):
                        self.neighbor_matrix[row][col].append((col,row-1,0))
                if row != len(self.layout)-1:
                    if not (row == 4 and (col < 2 or col > 4)):
                        self.neighbor_matrix[row][col].append((col,row+1,4))
                # Set diagonal neighbors
                if col%2 == 1 and row%2 == 1:
                    self.__set_cross_neighbors(row, col)
    
    def set_initial_peices(self):
        x, y = 2, 0
        for i in range(2):
            for j in range(3):
                self.slots[y][x] = Hen(y, x)
                x += 1
            y += 1
            x = 2
        for i in range(2):
            x = 0
            for j in range(7):
                self.slots[y][x] = Hen(y, x)
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
        self.slots[y][x] = Fox(y,x)
        self.slots[y][x+1] = Empty(y,x+1)
        self.slots[y][x+2] = Fox(y,x+2)
        #print(self.slots)
                

    
    def __set_cross_neighbors(self, row, col):
        self.neighbor_matrix[row][col].append((col-1, row-1, 7))
        self.neighbor_matrix[row][col].append((col+1, row-1, 1))
        self.neighbor_matrix[row][col].append((col-1, row+1, 5))
        self.neighbor_matrix[row][col].append((col+1, row+1, 3))

        self.neighbor_matrix[row-1][col-1].append((col, row, 3))
        self.neighbor_matrix[row+1][col-1].append((col, row, 1))
        self.neighbor_matrix[row-1][col+1].append((col, row, 5))
        self.neighbor_matrix[row+1][col+1].append((col, row, 7))
    
    def move_piece(self, col, row, col2, row2):
        """Moves piece from one slot to another, if second slot not empty, return false"""
        if self.slots[row2][col2] is None:
            return False
        if not self.slots[row2][col2].type == "Empty":
            return False
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
