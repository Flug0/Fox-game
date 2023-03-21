import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from game import Game

BOARD_SIZE = 7*7

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(BOARD_SIZE, BOARD_SIZE * BOARD_SIZE) # Input layer
        self.fc2 = nn.Linear(BOARD_SIZE * BOARD_SIZE, BOARD_SIZE * BOARD_SIZE) # Hidden layer
        self.fc3 = nn.Linear(BOARD_SIZE * BOARD_SIZE, BOARD_SIZE * BOARD_SIZE) # Output layer

    def forward(self, x):
        x = x.view(-1, BOARD_SIZE)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class Environment:
    def __init__(self):
        self.game = Game()
    
    def reset(self):
        self.game = Game()
        return self.game.board.slots

    def step(self, action):
        pass

# Define your loss function
criterion = nn.MSELoss()

# Define your optimizer
model = Model()
env = Environment()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Define your training loop
def train(model, env, optimizer, criterion, num_episodes=1000):
    for i_episode in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            # Use the model to choose an action
            action = model(torch.from_numpy(state).float())
            action = torch.argmax(action).item()

            # Play the game with the selected action
            next_state, reward, done, info = env.step(action)

            # Calculate the loss
            target = reward + model(torch.from_numpy(next_state).float()).max().detach()
            loss = criterion(model(torch.from_numpy(state).float())[action], target)

            # Update the model
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            state = next_state