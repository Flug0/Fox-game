from src.window import Window
from src.board import Board
from src.piece import *

class Game():
    def __init__(self):
        self.board = Board()
        self.win = Window(self.board)
        self.hens = 20
        self.foxes = 2
        self.foxs_turn = False
        self.more_jumps = False
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
                # Try to see if it is possible to double jump again
                newX, newY = self.more_double_jumps(doublejumpX, doublejumpY)
                if self.win.end_turn or not self.more_jumps:
                    self.foxs_turn = False
                    self.win.end_turn = False
                else:
                    self.more_double_jumps(newX, newY)
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
        if self.hens <= 8:
            print("Foxes won")
            pass
        elif self.foxes <= 0:
            print("Hens won")
            pass
        elif self.board.get_hens_in_nest() == 9:
            print("Hens won")
            pass

    
    def run(self):
        while True:
            self.win.update(self.board)
            self.move_piece()
            self.check_win()
    """
    Tries too look in all directions from starting position to see if it is possible to double jump again.
    E.g. The neighbour square contains a 'Hen' and the one beyond is 'Empty'
    If it is, then set the global variable 'self.win.more_jumps = True', to indicate that it is still the foxes turn
    If it is not possible, then set the variable to False.
    """
    def more_double_jumps(self, startX, startY):
        for i in range(0, 9):
            endX, endY = self.next_pos((startX, startY), i)
            if (endX, endY, i) in self.board.neighbor_matrix[startY][startX] and \
                    self.board.slots[endY][endX].type == "Hen":
                doublejumpX, doublejumpY = self.next_pos((endX, endY), i)
                if (doublejumpX, doublejumpY, i) in self.board.neighbor_matrix[endY][endX] and \
                        self.board.slots[doublejumpX][doublejumpY].type == "Empty":
                    self.more_jumps = True
                    self.foxs_turn = True
                    return doublejumpX, doublejumpY
        self.more_jumps = False
        self.foxs_turn = False


            