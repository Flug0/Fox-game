from look_ahead_ai.heuristics import Heuristics
from look_ahead_ai.node import Node
from board import Board
import math
import time
import concurrent.futures
import multiprocessing

"""
Minimax algorithm with alpha-beta pruning.

Minimiser = Fox
Maximiser = Hen

Every node is a representation of the board at a given moment.
"""


# TODO Make it perform better, moving a step forward on the mirror side of middle is equal and don't have to be
#   calculated twice.

# TODO Also moving 1 step with one sheep, and then 1 step with another, might be the same as moving in opposite order,
#   if fox don't capture a piece in between.

class AI:
    def get_best_move(self, depth, game, with_parallel, with_alpha_beta_pruning):
        minInt = float("-inf")
        maxInt = float("inf")
        node = Node(game.copy())
        node.add_children()
        self.max_depth = depth
        if with_parallel:
            best_evaluation, count = self.get_best_move_parallel(depth, node, with_alpha_beta_pruning)
        else:
            if with_alpha_beta_pruning:
                print("-- AI is thinking using alpha-beta pruning but sequential --")
                best_evaluation, count = self.minimax_with_alpha_beta_pruning(node, depth, minInt, maxInt, 0)
            else:
                print("-- AI is thinking without pruning and in sequential --")
                best_evaluation, count = self.minimax_no_pruning(node, depth, 0)
        
        for child in node.children:
            print(child.evaluation)
            if child.evaluation == best_evaluation:
                return child.game, count, best_evaluation
        raise Exception("No best move")
        #return game, count


    def get_best_move_parallel(self, depth, node, with_alpha_beta_pruning):
        # Create an executor
        if with_alpha_beta_pruning:
            pass
        else:
            return self.minimax_no_prune_helper(node, depth, 0)
        raise Exception("No best move")

    def minimax_no_prune_helper(self, node, depth, counter):
        if depth == 0 or node.game.someone_has_won():  # or node is a terminal node
            node.evaluation = Heuristics(node.game).points
        else:
            for child in node.children:
                child.add_children()
            minEvaluation = float('inf')
            maxEvaluation = float('-inf')
            if depth == self.max_depth:  # create processes only for top level calls
                with multiprocessing.Pool() as pool:
                    print(len(node.children))
                    results = [pool.apply_async(self.minimax_no_prune_helper, (child, depth - 1, counter+1)) for child in node.children]
                    for child, result in zip(node.children, results):
                        evaluation, counter = result.get()
                        child.evaluation = evaluation  # Manually update evaluation for each child
                        print("Evaluation:", evaluation)
                        if node.game.foxs_turn:
                            minEvaluation = min(minEvaluation, evaluation)
                        else:
                            maxEvaluation = max(maxEvaluation, evaluation)
                    # Shut down the pool
                    pool.close()
                    pool.join()
                    node.evaluation = minEvaluation if node.game.foxs_turn else maxEvaluation
                    
            else:  # for non-top level calls, execute the recursion sequentially
                for child in node.children:
                    evaluation, counter = self.minimax_no_prune_helper(child, depth - 1, counter+1)
                    if node.game.foxs_turn:
                        minEvaluation = min(minEvaluation, evaluation)
                    else:
                        maxEvaluation = max(maxEvaluation, evaluation)
                node.evaluation = minEvaluation if node.game.foxs_turn else maxEvaluation
        return node.evaluation, counter


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
