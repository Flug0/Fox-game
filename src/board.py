

class Board():
    def __init__(self):
        self.slots = [[]]
        self.layout = [3, 3, 7, 7, 7, 3, 3]
        self.neighbor_matrix = [[[ [] ] for _ in range(max(self.layout))] for _ in range(len(self.layout))]

        self.set_neighbor_matrix()

    def set_neighbor_matrix(self):
        for i in range(len(self.layout)):
            for j in range(self.layout[i]):
                # Set right/left neighbors
                if j != 0:
                    self.neighbor_matrix[i][j].append((i,j-1))
                if j != self.layout[i]-1:
                    self.neighbor_matrix[i][j].append((i,j+1))
                
        pass
    
    def set_slot(self, row, col, piece):
        self.slots[row][col] = piece
    
    def get_slot(self, row, col):
        return self.slots[row][col]