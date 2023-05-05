from look_ahead_ai.ai import AI
from window import Window
import time
import matplotlib.pyplot as plt


class Run:
    def __init__(self, game):
        self.game = game
        self.win = Window(self.game.board)
        self.run()

    def run(self):

        ai = AI()

        plot_data = []

        while True:
            #self.game.check_if_fox_trapped() # Check if fox is trapped
            self.win.update(self.game.board)
            if not self.game.foxs_turn:
                #valid_move, endPos = self.game.check_valid_move(self.win.selected_pos, self.win.direction)
                #if valid_move:
                #    self.game.move(self.win.selected_pos, endPos)
                self.game, _, _ = ai.get_best_move(2, self.game, with_parallel=False, with_alpha_beta_pruning=True)
            else:
                #valid_move, endPos = self.game.check_valid_move(self.win.selected_pos, self.win.direction)
                #if valid_move:
                #    self.game.move(self.win.selected_pos, endPos)
                #t0 = time.time()
                plot_data.append(get_data(self.game, ai))
                self.game, _, _ = ai.get_best_move(2, self.game, with_parallel=False, with_alpha_beta_pruning=True)
                #t1 = time.time()
                #print("-- AI has finished thinking --")
                #print("Amount of nodes looked through =", node_count)
                #print("Time for AI to think:", t1-t0)
            fox_won, hen_won = self.game.check_win()
            if fox_won or hen_won:
                break
        
        for depth in range(1, 2):
            plt.plot([i for i in range(1,len(plot_data)*2,2)],[data[0][depth-1][1] for data in plot_data], label='No Pruning', linestyle='solid')
            plt.plot([i for i in range(1,len(plot_data)*2,2)],[data[1][depth-1][1] for data in plot_data], label='Alpha-Beta Pruning', linestyle='dashed')

        plt.xlabel('Turn')
        plt.ylabel('Number of Nodes Searched')
        plt.title('Nodes Searched, Alpha-Beta Pruning vs No Pruning, Depth 4')
        plt.legend()
        plt.show()

        print("Someone won, game ended")

def get_data(game, ai):
    """
    Compare depths: How many nodes searched, what is max Eval and did it differ?
    With/without alpha beta pruning
    With/without variable depth
    """
    normal_list = []
    alpha_beta_list = []
    for i in range(4, 5):
        g,c,b = get_data_from_ai(i, game, ai, False, False)
        normal_list.append((g,c,b))
        g,c,b = get_data_from_ai(i, game, ai, False, True)
        alpha_beta_list.append((g,c,b))
    
    for i, calc in enumerate(alpha_beta_list):
        print("Depth =", i+1)
        print("Amount of nodes looked through =", calc[1])
        print("Max Eval =", calc[2])

    return normal_list, alpha_beta_list



def get_data_from_ai(depth, game, ai, parallel, alpha_beta):
    g, c, b = ai.get_best_move(depth, game, parallel, alpha_beta)
    return g, c, b

def compare_game_states(game1, game2):
    for row in range(0, 7):
        for col in range(0, 7):
            if game1.board.slots[row][col] == None:
                continue
            if game1.board.slots[row][col].type != game2.board.slots[row][col].type:
                print("Not equal at row:", row, "col:", col)
                return False
    return True
