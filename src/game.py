from window import Window
from board import Board
from piece import *

class Game():
    def __init__(self):
        self.board = Board()
        self.win = Window(self.board)
        self.hens = 20
        self.foxes = 2
        self.foxs_turn = False
        #self.board.slots[0][2] = Fox(0, 2)
        print(self.board.neighbor_matrix)
    
    def move_piece(self):
        """Check if allowed move, if allowed move piece"""
        if self.board.get_slot(self.win.selected_pos[1], self.win.selected_pos[0]).type == "Empty":
            return False
        if self.board.get_slot(self.win.selected_pos[1], self.win.selected_pos[0]).type == "Hen" and self.win.direction not in [2,3,4,5,6]:
            return False
        startX, startY = self.win.selected_pos
        endX, endY = self.next_pos(self.win.selected_pos, self.win.direction)
        # Move one slot
        if (endX, endY, self.win.direction) in self.board.neighbor_matrix[startY][startX]:
            if self.foxs_turn and isinstance(self.board.get_slot(self.win.selected_pos[1], self.win.selected_pos[0]), Fox):
                self.foxs_turn = False
            elif not self.foxs_turn and isinstance(self.board.get_slot(self.win.selected_pos[1], self.win.selected_pos[0]), Hen):
                self.foxs_turn = True
            else:
                return False
            if self.board.move_piece(startX, startY, endX, endY):
                return True
            else:
                self.foxs_turn = not self.foxs_turn
        # Return if Hen or not Fox's turn
        if self.board.get_slot(self.win.selected_pos[1], self.win.selected_pos[0]).type == "Hen" or not self.foxs_turn:
            return False
        if endY > len(self.board.neighbor_matrix) -1:
            return False
        elif endX > len(self.board.neighbor_matrix[endY]) -1:
            return False
        # If other piece is Fox, return
        if self.board.slots[endY][endX] is not None:
            if self.board.slots[endY][endX].type == "Fox":
                return False
        doublejumpX, doublejumpY = self.next_pos((endX, endY), self.win.direction)
        if (doublejumpX, doublejumpY, self.win.direction) in self.board.neighbor_matrix[endY][endX]:
            if self.board.move_piece(startX, startY, doublejumpX, doublejumpY):
                self.remove_piece(endX, endY)
                self.foxs_turn = False
                return True
        return False
    
    def next_pos(self, pos, direction):
        if direction == 0:
            return (pos[0], pos[1]-1)
        elif direction == 1:
            return (pos[0]+1, pos[1]-1)
        elif direction == 2:
            return (pos[0]+1, pos[1])
        elif direction == 3:
            return (pos[0]+1, pos[1]+1)
        elif direction == 4:
            return (pos[0], pos[1]+1)
        elif direction == 5:
            return (pos[0]-1, pos[1]+1)
        elif direction == 6:
            return (pos[0]-1, pos[1])
        elif direction == 7:
            return (pos[0]-1, pos[1]-1)
        else:
            return (-1, -1)
        
        
    def remove_piece(self, col, row):
        if self.board.slots[row][col].type == "Hen":
            self.hens -= 1
        elif self.board.slots[row][col].type == "Fox":
            self.foxes -= 1
        self.board.set_slot(row, col, Empty(row, col))
    
    def check_win(self):
        if self.hens <= 0:
            pass
        elif self.foxes <= 0:
            pass
        elif self.board.get_hens_in_nest() == 9:
            pass

    
    def run(self):
        while True:
            self.win.update(self.board)
            self.move_piece()
            self.check_win()
            