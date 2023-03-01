"""
maximizingPlayer: True = Sheep, False = Fox
node: Not implemnted, but this is equal to the steps taken by the AI, steps forms a tree of "nodes" hence the name.
depth: Hopefully we can calculate about 5 or 6 steps into the future at a given step.
"""
class Lookahead_AI():
    def __init__(self):
        pass

    def minmax(self, node, depth, maximizingPlayer):
        if depth == 0:  # or node is a terminal node
            return 0  # static ealuation of node
        if maximizingPlayer:
            maxEvaluation = int('-inf')
            for child in node:
                evaluation = self.minmax(child, depth - 1, False)
                maxEvaluation = max(maxEvaluation, evaluation)
            return maxEvaluation
        else:
            minEvaluation = int('inf')
            for child in node:
                evaluation = self.minmax(child, depth - 1, False)
                minEvaluation = min(minEvaluation, evaluation)
            return minEvaluation


if __name__ == "__main__":
    lookahead_AI = Lookahead_AI()
    lookahead_AI.minmax(node, 3, True)

# TODO: Implement nodes
# TODO: Have a point system eg: + 100 for winning, +10 for getting a sheep into the foxes starting position -10 for
# getting a sheep captured etc.
# TODO: Make it perform better, moving a step forward on the mirror side of middle is equal and don't
# have to be calculated twice.
# TODO: Also moving 1 step with one sheep, and then 1 step with another, might be the same as moving in opposite order,
# if fox don't capture a piece in between.