from look_ahead_ai.heuristics import Heuristics
"""
maximizingPlayer: True = Sheep, False = Fox
node: Not implemnted, but this is equal to the steps taken by the AI, steps forms a tree of "nodes" hence the name.
depth: Hopefully we can calculate about 5 or 6 steps into the future at a given step.
"""
class Minimax_algo():
    def __init__(self):
        self.heuristics = Heuristics()

    def minimax(self, node, depth, alpha, beta, maximizingPlayer):
        if depth == 0:  # or node is a terminal node
            return self.heuristics.calculate_heuristic()  # static evaluation of node
        if maximizingPlayer:
            maxEvaluation = int('-inf')
            for child in node:
                evaluation = self.minimax(child, depth - 1, alpha, beta, False)
                maxEvaluation = max(maxEvaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return maxEvaluation
        else:
            minEvaluation = int('inf')
            for child in node:
                evaluation = self.minimax(child, depth - 1, alpha, beta, False)
                minEvaluation = min(minEvaluation, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return minEvaluation


if __name__ == "__main__":
    lookahead_AI = Minimax_algo()
    lookahead_AI.minimax(node, 3, int('-inf'), int('inf'), True)

# TODO: Implement nodes
# TODO: Have a point system eg: + 100 for winning, +10 for getting a sheep into the foxes starting position -10 for
# getting a sheep captured etc.
# TODO: Make it perform better, moving a step forward on the mirror side of middle is equal and don't
# have to be calculated twice.
# TODO: Also moving 1 step with one sheep, and then 1 step with another, might be the same as moving in opposite order,
# if fox don't capture a piece in between.