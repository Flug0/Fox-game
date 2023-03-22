import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from game import Game
from RLOutputs import Converter

BOARD_SIZE = 7*7
INPUT_SIZE = 33
HIDDEN_SIZE = BOARD_SIZE * BOARD_SIZE
OUTPUT_SIZE = 248

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN_SIZE) # Input layer
        self.fc2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE) # Hidden layer
        self.fc3 = nn.Linear(HIDDEN_SIZE, OUTPUT_SIZE) # Output layer

    def forward(self, x):
        x = x.view(-1, INPUT_SIZE)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        x = self.fc3(x)
        return x

    def save(self, filename='model.pth'):
        torch.save(self.state_dict(), filename)

class Environment:
    def __init__(self):
        self.game = Game()
        self.board = self.game.board
    
    def reset(self):
        self.game = Game()
        return self.game.board.slots

    # Function that converts the board into a list representing the board
    def get_state(self):
        self.state = []
        for row in self.game.board.slots:
            for column in row:
                if column == None:
                    pass
                elif column.type == "Empty":
                    self.state.append(0)
                elif column.type == "Hen":
                    self.state.append(1)
                elif column.type == "Fox":
                    self.state.append(2)
        self.state = np.array(self.state)
        return self.state

    # Takes an action and returns the next board position
    # If action is invalid, next_state = state
    def next_board_position(self, action):
        pos = converter.convert_action_to_move(action)
        return self.board.move_piece(pos[0][0], pos[0][1], pos[1][0], pos[1][1])


    # Function that takes an action and returns the next state, reward, done, and info
    # If action is invalid, next_state = state and reward = -X
    def step(self, action):
        if not self.next_board_position(action):
            reward = -10
        else:
            reward = 10
        if self.game.check_win():
            reward = 100
            done = True
        return self.get_state(), reward, done, None

# Define training loop
def train(model, env, optimizer, criterion, num_episodes=1000):
    for i_episode in range(num_episodes):
        env.reset()
        done = False
        while not done:
            optimizer.zero_grad()
            state = torch.tensor(env.get_state(), dtype=torch.float)

            # Use the model to choose an action
            output = model(state)
            action = torch.argmax(output).item()

            # Play the game with the selected action, if action invalid, next_state = state and reward = -X
            next_state, reward, done, info = env.step(action)

            # Calculate the loss
            target = reward + model(torch.from_numpy(next_state).float()).max().detach()
            print("Target: " + str(target))
            print("Target: " + str(target.detach()))

            print(state)
            print(model(state))
            print(torch.argmax(model(state)))
            print(model(state)[0][torch.argmax(model(state))])

            loss = criterion(model(state.float())[0][action], target)
            
            print("Loss: " + str(loss))

            

            # Update the model
            #optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            state = next_state

# Define loss function
criterion = nn.MSELoss()

# Define optimizer
model = Model()
env = Environment()
optimizer = optim.Adam(model.parameters(), lr=0.01)
converter = Converter()
print(env.get_state())
print(env.board)

# TODO MOVE STUFF TO GPU

train(model, env, optimizer, criterion)

