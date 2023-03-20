from window import Window
from board import Board
from piece import *
from look_ahead_ai.minimax_algo import Minimax_algo
from look_ahead_ai.node import Node


class Game():
    def __init__(self):
        self.board = Board()
        self.win = Window(self.board)
        self.hens = 20
        self.foxes = 2
        self.foxs_turn = False
        self.did_capture = False
        self.selected_piece = None
        # self.board.slots[0][2] = Fox(0, 2)
        #print(self.board.neighbor_matrix)

    def move_on_valid_move(self, position, direction):
        startX, startY = position
        self.selected_piece = self.board.get_slot(startY, startX).type
        endX, endY = self.next_pos(position, direction)

        # Finds all the ways a move is invalid for both Hens and Foxes
        if (endX, endY, self.win.direction) not in self.board.neighbor_matrix[startY][startX] \
                or 0 >= endY >= len(self.board.neighbor_matrix) - 1 \
                or 0 >= endX >= len(self.board.neighbor_matrix[endY]) -1 \
                or self.selected_piece == "Empty" \
                or self.selected_piece is None:
            return False, self.board

        # If it's Fox's turn:
        # 1: Find if move is legal for foxes. If it is - step 2
        # 2: Try to move piece. If successful - step 3
        # 3: Check if it captured. If it did - remove captured piece.
        if self.foxs_turn:
            valid_move, newEndX, newEndY = self.valid_fox_move(endX, endY, direction)
            if valid_move:
                #print("Valid fox move")
                if self.board.move_piece(startX, startY, newEndX, newEndY):
                    #print("Moved piece")
                    if self.did_capture:
                        #print("Captured Hen")
                        self.remove_piece(endX, endY)
                    return True, self.board

        # If it's Hen's turn:
        # 1: Find if move is legal for Hen's. If it is - step 2
        # 2: Try to move piece. If successful - end turn
        else:
            if self.valid_hen_move(endY, endX, direction):
                if self.board.move_piece(startX, startY, endX, endY):
                    self.foxs_turn = True
                    return True, self.board
        return False, self.board

    def check_double_jump(self, endY, endX, direction):
        doubleJumpX, doubleJumpY = self.next_pos((endX, endY), direction)
        if (doubleJumpX, doubleJumpY, direction) in self.board.neighbor_matrix[endY][endX] and \
                self.board.slots[doubleJumpY][doubleJumpX].type == "Empty" and \
                0 <= doubleJumpX <= len(self.board.neighbor_matrix[doubleJumpY]) -1 and \
                0 <= doubleJumpY <= len(self.board.neighbor_matrix) -1:
            self.did_capture = True
            return True, doubleJumpX, doubleJumpY
        self.did_capture = False
        self.foxs_turn = False
        return False, endX, endY

    def valid_fox_move(self, endX, endY, direction):
        if self.selected_piece == "Fox":
            # Can only hop to an empty square if did not capture last turn
            if self.board.get_slot(endY, endX).type == "Empty" and not self.did_capture:
                self.foxs_turn = False
                return True, endX, endY
            # This is to stop the fox from jumping any more if does not try to capture another hen.
            elif self.board.get_slot(endY, endX).type == "Empty" and self.did_capture:
                self.foxs_turn = False
                self.did_capture = False
                return False, endX, endY
            elif self.board.get_slot(endY, endX).type == "Hen":
                return self.check_double_jump(endY, endX, direction)
        return False, endX, endY

    def valid_hen_move(self, endY, endX, direction):
        if direction in [2, 3, 4, 5, 6] and self.board.get_slot(endY, endX).type == "Empty" \
                and self.selected_piece == "Hen":
            return True
        return False

    def next_pos(self, pos, direction):
        if direction == 0:
            return pos[0], pos[1] - 1
        elif direction == 1:
            return pos[0] + 1, pos[1] - 1
        elif direction == 2:
            return pos[0] + 1, pos[1]
        elif direction == 3:
            return pos[0] + 1, pos[1] + 1
        elif direction == 4:
            return pos[0], pos[1] + 1
        elif direction == 5:
            return pos[0] - 1, pos[1] + 1
        elif direction == 6:
            return pos[0] - 1, pos[1]
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

    def run(self):
        minimax = Minimax_algo()
        minInt = float("-inf")
        maxInt = float("inf")
        while True:
            thisNode = Node(self.board)
            self.win.update(self.board)
            if not self.foxs_turn:
                self.move_on_valid_move(self.win.selected_pos, self.win.direction)
            else:
                heuristics, newBoard = minimax.minimax(thisNode, 7, minInt, maxInt, True)
                self.board = newBoard
            fox_won, hen_won = self.check_win()
            if fox_won or hen_won:
                break
        print("Someone won, game ended")