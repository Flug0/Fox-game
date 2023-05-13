from look_ahead_ai.ai import AI
from window import Window
import time
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import numpy as np


MAX_DEPTH = 5
HEN_DEPTH = 2
FOX_DEPTH = 3

class Run:
    def __init__(self, game):
        self.game = game
        self.win = Window(self.game.board)
        self.round = 0
        self.run()

    def run(self):

        ai = AI()

        plot_data = []

        while True:
            self.win.update(self.game.board)
            if not self.game.foxs_turn:

                self.game, _, _ = ai.get_best_move(HEN_DEPTH, self.game, with_parallel=True, with_alpha_beta_pruning=True)
            else:
                plot_data.append(get_data(self.game, ai))
                #game2 = self.game.copy()

                #start_time = time.time()
                self.game, _, b = ai.get_best_move(FOX_DEPTH, self.game, with_parallel=True, with_alpha_beta_pruning=True)
                #end_time = time.time()
                #print("Time for Parallel, NO PRUNE, AI to think:", end_time-start_time)

                """
                start_time = time.time()
                game2, _, b2 = ai.get_best_move(6, game2, with_parallel=True, with_alpha_beta_pruning=True)
                end_time = time.time()
                print("Time for Parallel, AB-PRUNE, AI to think:", end_time-start_time)

                
                if compare_game_states(self.game, game2):
                    print("Games are equal")
                else:
                    print("Games are not equal")
                    print("BEST EVAL NO PARALLEL =", b)
                    print("BEST EVAL PARALLEL =", b2)
                """
            self.round += 1
            print("Round: ", self.round)
            if self.round > 100:
                break
            fox_won, hen_won = self.game.check_win()
            if fox_won or hen_won:
                break
        
        #create_table(plot_data)

        write_data_to_file(plot_data)

        #create_table_plot(plot_data)

        #create_plot(plot_data)

        print("Someone won, game ended")

def get_data(game, ai):
    """
    Compare depths: How many nodes searched, what is max Eval and did it differ?
    With/without alpha beta pruning
    With/without variable depth
    """

    normal_list = []
    alpha_beta_list = []

    for i in range(1, MAX_DEPTH+1):
        #g,c,b = get_data_from_ai(i, game, ai, True, False)
        #normal_list.append((g,c,b))
        g,c,b = get_data_from_ai(i, game, ai, True, True)
        alpha_beta_list.append((g,c,b))
    
    for i, calc in enumerate(alpha_beta_list):
        #print("Depth =", i+1)
        #print("Amount of nodes looked through =", calc[1])
        #print("Max Eval =", calc[2])
        pass

    comparison_results = []
    for j in range(MAX_DEPTH):
        temp = []
        for i in range(j+1):
            temp.append(True if compare_game_states(alpha_beta_list[i][0], alpha_beta_list[j][0]) else False)
        comparison_results.append(temp)
    
    return normal_list, alpha_beta_list, comparison_results

def create_plot(plot_data):
    depth_stats = [[0 for _ in range(MAX_DEPTH-(MAX_DEPTH-i)+1)] for i in range(MAX_DEPTH)]
    for data in plot_data:
        for j, lists in enumerate(data[2]):
            for i, elem in enumerate(lists):
                if elem:
                    depth_stats[j][i] += 1

    #print(depth_stats)
    depth_stats = [[round(elem/len(plot_data),4) for elem in sublist] for sublist in depth_stats]
    #print(depth_stats)
    for i, list in enumerate(depth_stats):
        #print(f"Depth {i+1} to {len(list)} vs Max Depth: {len(list)}")
        #print(list)
        pass
    #print(len(plot_data))

    for depth in range(0, MAX_DEPTH):
        plt.plot([i for i in range(1,len(plot_data)*2,2)],[data[0][depth][1] for data in plot_data], label='No Pruning', linestyle='solid')
        plt.plot([i for i in range(1,len(plot_data)*2,2)],[data[1][depth][1] for data in plot_data], label='Alpha-Beta Pruning', linestyle='dashed')
    

    plt.xlabel('Turn')
    plt.ylabel('Number of Nodes Searched')
    plt.title('Nodes Searched, Alpha-Beta Pruning vs No Pruning, Depth 4')
    plt.legend()
    plt.show()

def write_data_to_file(plot_data):
    # Iterate over depths
    for depth in range(1, MAX_DEPTH+1):
        # Initialize an empty list to store binary values
        converted_list = [[] for _ in range(MAX_DEPTH+1)]
        
        # Iterate over plot_data
        for i, lists in enumerate(plot_data):
            # Convert True/False to 1/0 and append to binary_list
            for j, list in enumerate(lists[2]):
                converted_list[len(list)-1].append([1 if val else 0 for val in list])

    with open("data.txt", "a") as f:
        f.write(f"\n{HEN_DEPTH}vs{FOX_DEPTH}\n")
        for i, list in enumerate(converted_list[1:-1]):
            f.write(f"Depth {1} to {MAX_DEPTH-1} vs Max Depth: {MAX_DEPTH}\n")
            for data in list:
                if len(data) > 1:
                    f.write(str(data[:-1]) + " ")
            f.write("\n")
    


def create_table_plot(plot_data):
    
    # Iterate over depths
    for depth in range(1, MAX_DEPTH+1):
        # Initialize an empty list to store binary values
        converted_list = [[] for _ in range(MAX_DEPTH+1)]
        
        # Iterate over plot_data
        for i, lists in enumerate(plot_data):
            # Convert True/False to 1/0 and append to binary_list
            for j, list in enumerate(lists[2]):
                converted_list[len(list)-1].append([1 if val else 0 for val in list])


        #print(converted_list)

        for i, list in enumerate(converted_list):
            plt.plot([i for i in range(1,len(list)*2,2)], [data[:-1] for data in list], label='No Pruning', linestyle='solid')

    plt.show()

def create_table(plot_data):
    # Create table with headers
    tables = []
    for depth in range(1, MAX_DEPTH+1):
        header = ["Move"] + [f"Depth {i} vs depth {depth}" for i in range(1, depth+1)]
        tables.append(PrettyTable(header))

    # Add rows to the table
    for i, lists in enumerate(plot_data):
        move_number = i*2 + 1
        for j, list in enumerate(lists[2]):
            row = [move_number] + list
            tables[j].add_row(row)

    # Print the table
    for table in tables:
        print(table)

def get_data_from_ai(depth, game, ai, parallel, alpha_beta):
    g, c, b = ai.get_best_move(depth, game, parallel, alpha_beta)
    return g, c, b

def compare_game_states(game1, game2):
    for row in range(0, 7):
        for col in range(0, 7):
            if game1.board.slots[row][col] == None:
                continue
            if game1.board.slots[row][col].type != game2.board.slots[row][col].type:
                #print("Not equal at row:", row, "col:", col)
                return False
    return True
