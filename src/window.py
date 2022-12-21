import pygame, math
from constants import WIDTH, HEIGHT, FPS, BACKGROUND_COLOR as BC


class Window():
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.win = pygame.display.set_mode((self.width, self.height))
        self.slot_spacing = math.floor(min(self.width, self.height) / 10)
        self.clock = pygame.time.Clock()

    def draw_board(self, board):
        """Draw layout"""
        ypos = self.height / 2 - math.floor(len(board.layout) / 2) * self.slot_spacing
        for slots in board.layout:
            xpos = self.width / 2 - math.floor(slots / 2) * self.slot_spacing
            for i in range(slots):
                pygame.draw.circle(self.win, (0, 0, 0), (xpos, ypos), 5)
                xpos += self.slot_spacing
            ypos += self.slot_spacing
                

        """Draw Pieces"""
        pass

    def update(self, board):
        self.clock.tick(FPS)
        print("Tick")
        self.win.fill(BC)
        self.draw_board(board)
        pygame.display.update()
            





if __name__ == "__main__":
    w = Window()
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        w.update()