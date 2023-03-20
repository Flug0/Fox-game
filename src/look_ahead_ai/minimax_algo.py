from look_ahead_ai.heuristics import Heuristics
from look_ahead_ai.node import Node
from board import Board

"""
Minimax algorithm with alpha-beta pruning.

Minimiser = Fox
Maximiser = Sheep

Every node is a representation of the board at a given moment.
"""


# TODO: Make it perform better, moving a step forward on the mirror side of middle is equal and don't have to be
#   calculated twice.

# TODO: Also moving 1 step with one sheep, and then 1 step with another, might be the same as moving in opposite order,
#   if fox don't capture a piece in between.

class Minimax_algo:
    def __init__(self, game):
        self.heuristics = Heuristics(game)
        self.points = self.heuristics.points

    def minimax(self, node, depth, alpha, beta, maximizingPlayer):
        self.heuristics.calculate_heuristic()
        print("Current evaluation = {0}, depth = {1}".format(self.points, depth))
        if depth == 0:  # or node is a terminal node
            return self.heuristics.calculate_heuristic(), node.board  # static evaluation of node
        if maximizingPlayer:
            print("Hi")
            maxEvaluation = float('-inf')
            for child in node.children:
                newNode = node(child.board)
                evaluation = self.minimax(newNode, depth - 1, alpha, beta, False)
                maxEvaluation = max(maxEvaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            print("1")
            return maxEvaluation, node.board
        else:
            print("Hello")
            minEvaluation = float('inf')
            for child in node:
                newNode = node(child.board)
                evaluation = self.minimax(newNode, depth - 1, alpha, beta, True)
                minEvaluation = min(minEvaluation, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minEvaluation, node.board


#if __name__ == "__main__":
#    lookahead_AI = Minimax_algo()
#    board = Board()
#    thisNode = Node(board)
#    lookahead_AI.minimax(thisNode, 3, int('-inf'), int('inf'), True)
