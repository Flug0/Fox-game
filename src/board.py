

class Board():
    def __init__(self):
        self.slots = [[]]
        self.layout = None

        self.set_layout()
    
    def set_layout(self):
        """Sets board layout to Fox and Hen game"""
        self.layout = [3, 3, 7, 7, 7, 3, 3]
    
    def set_slot(self, row, col, piece):
        self.slots[row][col] = piece
    
    def get_slot(self, row, col):
        return self.slots[row][col]