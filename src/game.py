from window import Window
from board import Board
from piece import *


class Game():
    def __init__(self):
        self.board = Board()
        self.hens = 20
        self.foxes = 2
        self.foxs_turn = False
        self.did_capture = False
        self.selected_piece = None
        self.capturePos = None

    def copy(self):
        newGame = Game()
        newGame.board = Board(self.board)
        newGame.hens = self.hens
        newGame.foxes = self.foxes
        newGame.foxs_turn = self.foxs_turn
        newGame.did_capture = self.did_capture
        newGame.selected_piece = self.selected_piece
        newGame.capturePos = self.capturePos
        return newGame

    def check_valid_move(self, position, direction):
        startY, startX = position
        self.selected_piece = self.board.get_slot(startY, startX).type
        endY, endX = self.next_pos(position, direction)

        # Finds all the ways a move is invalid for both Hens and Foxes
        if (endY, endX, direction) not in self.board.neighbor_matrix[startY][startX] \
                or 0 >= endY > len(self.board.slots) \
                or 0 >= endX > len(self.board.slots[endY]) \
                or self.selected_piece == "Empty" \
                or self.selected_piece is None:
            return False, [endY, endX]

        # If it's Fox's turn:
        # 1: Find if move is legal for foxes. If it is - step 2
        # 2: Try to move piece. If successful - step 3
        # 3: Check if it captured. If it did - remove captured piece.
        if self.foxs_turn:
            valid_move, endPos = self.valid_fox_move(endY, endX, direction)
            if valid_move:
                return True, endPos

        # If it's Hen's turn:
        # 1: Find if move is legal for Hen's. If it is - step 2
        # 2: Try to move piece. If successful - end turn
        else:
            if self.valid_hen_move(endY, endX, direction):
                return True, [endY, endX]
        return False, [endY, endX]

    def valid_hen_move(self, endY, endX, direction):
        if direction in [2, 3, 4, 5, 6] and self.board.get_slot(endY, endX).type == "Empty" \
                and self.selected_piece == "Hen":
            return True
        return False

    def valid_fox_move(self, endY, endX, direction):
        if self.selected_piece == "Fox":
            jumpSlot = self.board.get_slot(endY, endX).type
            # Can only hop to an empty square if did not capture last turn
            if jumpSlot == "Empty" and not self.did_capture:
                #self.foxs_turn = False
                return True, [endY, endX]
            # This is to stop the fox from jumping any more if does not try to capture another hen.
            elif jumpSlot == "Empty" and self.did_capture:
                #self.foxs_turn = False
                self.did_capture = False
                self.capturePos = None
                return False, [endY, endX]
            elif jumpSlot == "Hen":
                return self.check_double_jump(endY, endX, direction)
        return False, [endY, endX]

    def check_double_jump(self, endY, endX, direction):
        doubleJumpY, doubleJumpX = self.next_pos((endY, endX), direction)
        if (doubleJumpY, doubleJumpX, direction) not in self.board.neighbor_matrix[endY][endX] and \
                0 <= doubleJumpY < len(self.board.slots) and \
                0 <= doubleJumpX < len(self.board.slots[doubleJumpY]) and \
                self.board.slots[doubleJumpY][doubleJumpX] is not None and \
                self.board.slots[doubleJumpY][doubleJumpX].type == "Empty":
            self.did_capture = True
            self.capturePos = [endY, endX]
            return True, [doubleJumpY, doubleJumpX]
        self.did_capture = False
        #self.foxs_turn = False
        self.capturePos = None
        return False, [endY, endX]

    def move(self, startPos, endPos):
        if self.board.move_piece(startPos[0], startPos[1], endPos[0], endPos[1]):
            #print("Moved a piece")
            if self.foxs_turn:
                self.foxs_turn = False  # TODO: Remove and actually fix turns
                if self.did_capture and self.capturePos:
                    self.remove_piece(self.capturePos[0], self.capturePos[1])
            else:
                self.foxs_turn = True
            return True
        return False

    def next_pos(self, pos, direction):
        if direction == 0:
            return pos[0] - 1, pos[1]
        elif direction == 1:
            return pos[0] - 1, pos[1] + 1
        elif direction == 2:
            return pos[0], pos[1] + 1
        elif direction == 3:
            return pos[0] + 1, pos[1] + 1
        elif direction == 4:
            return pos[0] + 1, pos[1]
        elif direction == 5:
            return pos[0] + 1, pos[1] - 1
        elif direction == 6:
            return pos[0], pos[1] - 1
        elif direction == 7:
            return pos[0] - 1, pos[1] - 1
        else:
            return -1, -1

    def remove_piece(self, col, row):
        if self.board.slots[row][col].type == "Hen":
            self.hens -= 1
        elif self.board.slots[row][col].type == "Fox":
            self.foxes -= 1
        self.board.set_slot(row, col, Empty(row, col))

    def check_win(self):
        if self.hens <= 8:
            print("Foxes won")
            return True, False
        elif self.foxes <= 0:
            print("Hens won")
            return False, True
        elif self.board.get_hens_in_nest() == 9:
            print("Hens won")
            return False, True
        return False, False
