from look_ahead_ai.heuristics import Heuristics
from look_ahead_ai.node import Node
import multiprocessing as mp
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
    def get_best_move(self, depth, game, with_parallel, with_alpha_beta_pruning):
        minInt = float("-inf")
        maxInt = float("inf")
        node = Node(game.copy())
        node.add_children()
        if with_parallel:
            maxThreads = mp.cpu_count()
            print("Max amount of threads:", maxThreads)
            pool = mp.Pool(processes=len(node.children))
            for child in node.children:
                child.add_children()
                if with_alpha_beta_pruning:
                    print("-- AI is thinking using alpha-beta pruning and in parallel --")
                    inputs = [(child, depth-1, minInt, maxInt, 0)]
                    best_evaluations = pool.starmap(self.minimax_with_alpha_beta_pruning, inputs)
                    print(best_evaluations)
                else:
                    print("-- AI is thinking without pruning but in parallel --")
                    inputs = [(child, depth-1, 0)]
                    best_evaluations = pool.starmap(self.minimax_no_pruning, inputs)
                    print(best_evaluations)
            best_evaluation = max(best_evaluations)
        else:
            if with_alpha_beta_pruning:
                print("-- AI is thinking using alpha-beta pruning but sequential --")
                best_evaluation, count = self.minimax_with_alpha_beta_pruning(node, depth, minInt, maxInt, 0)
            else:
                print("-- AI is thinking without pruning and in sequential --")
                best_evaluation, count = self.minimax_no_pruning(node, depth, 0)
        for child in node.children:
            if child.evaluation == best_evaluation:
                return child.game, count
        raise Exception("No best move")
        #return game, count

    def minimax_with_alpha_beta_pruning(self, node, depth, alpha, beta, counter):
        if depth == 0 or node.game.someone_has_won():  # or node is a terminal node
            node.evaluation = Heuristics(node.game).points
        elif node.game.foxs_turn: # Minimiser
            minEvaluation = float('inf')
            for child in node.children:
                child.add_children()
                evaluation, counter = self.minimax_with_alpha_beta_pruning(child, depth - 1, alpha, beta, counter+1)
                minEvaluation = min(minEvaluation, evaluation)
                beta = min(beta, minEvaluation)
                if beta <= alpha:
                    break
            node.evaluation = minEvaluation
        else: # Maximiser
            maxEvaluation = float('-inf')
            for child in node.children:
                child.add_children()
                evaluation, counter = self.minimax_with_alpha_beta_pruning(child, depth - 1, alpha, beta, counter+1)
                maxEvaluation = max(maxEvaluation, evaluation)
                alpha = max(alpha, maxEvaluation)
                if beta <= alpha:
                    break
            node.evaluation = maxEvaluation
        return node.evaluation, counter

    def minimax_no_pruning(self, node, depth, counter):
        if depth == 0 or node.game.someone_has_won():  # or node is a terminal node
            node.evaluation = Heuristics(node.game).points
        elif node.game.foxs_turn: # Minimiser
            minEvaluation = float('inf')
            for child in node.children:
                child.add_children()
                evaluation, counter = self.minimax_no_pruning(child, depth - 1, counter+1)
                minEvaluation = min(minEvaluation, evaluation)
            node.evaluation = minEvaluation
        else: # Maximiser
            maxEvaluation = float('-inf')
            for child in node.children:
                child.add_children()
                evaluation, counter = self.minimax_no_pruning(child, depth - 1, counter+1)
                maxEvaluation = max(maxEvaluation, evaluation)
            node.evaluation = maxEvaluation
        return node.evaluation, counter
