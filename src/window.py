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
        # List with lists of all xpos and list with all ypos
        xpos_list, ypos_list = [],[]
        ypos = self.height / 2 - math.floor(len(board.layout) / 2) * self.slot_spacing
        for slots in board.layout:
            current_xpos_list = []
            xpos = self.width / 2 - math.floor(slots / 2) * self.slot_spacing
            for i in range(slots):
                pygame.draw.circle(self.win, (0, 0, 0), (xpos, ypos), 5)
                current_xpos_list.append(xpos)
                xpos += self.slot_spacing
            xpos_list.append(current_xpos_list)
            ypos_list.append(ypos)
            ypos += self.slot_spacing
        """Draw lines"""
        for i in range(len(ypos_list)):
            pygame.draw.line(self.win, (0,0,0), (xpos_list[i][0],ypos_list[i]), (xpos_list[i][-1],ypos_list[i]), width=3)
            if i == len(ypos_list)-1:
                break
            for xpos in xpos_list[i]:
                if xpos in xpos_list[i+1]:
                    pygame.draw.line(self.win, (255,0,0), (xpos, ypos_list[i]), (xpos, ypos_list[i+1]), width=3)
        
        pygame.draw.line(self.win, (0,255,0), (xpos_list[0][0], ypos_list[0]), (xpos_list[2][4], ypos_list[2]), width=3)
        

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