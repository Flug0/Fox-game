from look_ahead_ai.heuristics import Heuristics
from look_ahead_ai.node import Node
from board import Board
import math
import time

"""
Minimax algorithm with alpha-beta pruning.

Minimiser = Fox
Maximiser = Hen

Every node is a representation of the board at a given moment.
"""


# TODO: Make it perform better, moving a step forward on the mirror side of middle is equal and don't have to be
#   calculated twice.

# TODO: Also moving 1 step with one sheep, and then 1 step with another, might be the same as moving in opposite order,
#   if fox don't capture a piece in between.

class AI:
    def get_best_move(self, depth, game, win):
        minInt = float("-inf")
        maxInt = float("inf")
        node = Node(game.copy())
        node.add_children()
        bestEvaluation = self.minimax(node, depth, minInt, maxInt, win) # AI plays foxes
        for child in node.children:
            #print("Current child eval =", child.evaluation)
            if child.evaluation == bestEvaluation:
                return child.game
        raise Exception("No best move")

    def minimax(self, node, depth, alpha, beta, win):
        #win.update(node.game.board)
        if depth == 0:  # or node is a terminal node
            node.evaluation = Heuristics(node.game).points
            #print("Nodes final evaluation = {0}".format(node.evaluation))
        elif node.game.foxs_turn: # Minimiser
            minEvaluation = float('inf')
            for child in node.children:
                child.add_children()
                evaluation = self.minimax(child, depth - 1, alpha, beta, win)
                #print("Foxes turn")
                #print("Current evaluation = {0}, depth = {1}".format(evaluation, depth))
                minEvaluation = min(minEvaluation, evaluation)
                beta = min(beta, minEvaluation)
                if beta <= alpha:
                    break
            node.evaluation = minEvaluation
        else: # Maximiser
            maxEvaluation = float('-inf')
            for child in node.children:
                child.add_children()
                evaluation = self.minimax(child, depth - 1, alpha, beta, win)
                #print("Hens turn")
                #print("Current evaluation = {0}, depth = {1}".format(evaluation, depth))
                maxEvaluation = max(maxEvaluation, evaluation)
                alpha = max(alpha, maxEvaluation)
                if beta <= alpha:
                    break
            node.evaluation = maxEvaluation

        return node.evaluation
