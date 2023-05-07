import pygame, math, sys
from constants import WIDTH, HEIGHT, FPS, BACKGROUND_COLOR as BC


class Window():
    def __init__(self, board):
        self.width = WIDTH
        self.height = HEIGHT
        self.win = pygame.display.set_mode((self.width, self.height))
        self.slot_spacing = math.floor(min(self.width, self.height) / 10)
        self.margin = math.floor(min(self.width, self.height) / 2) - 3.5 * self.slot_spacing
        self.clock = pygame.time.Clock()
        self.positions = self.calculate_positions(board)
        self.selected = None
        self.selected_pos = (0, 2)
        self.selected_piece = None
        self.direction = -1
        self.pos_dict = self.convert_cords_to_position()


    def calculate_positions(self, board):
        # List with lists of all xpos and list with all ypos
        pos_list = []
        xpos_list, ypos_list = [],[]
        ypos = self.height / 2 - math.floor(len(board.layout) / 2) * self.slot_spacing
        for slots in board.layout:
            current_xpos_list = []
            xpos = self.width / 2 - math.floor(slots / 2) * self.slot_spacing
            for i in range(slots):
                current_xpos_list.append(xpos)
                xpos += self.slot_spacing
            xpos_list.append(current_xpos_list)
            ypos_list.append(ypos)
            ypos += self.slot_spacing
        for i in range(len(xpos_list)):
            for x in xpos_list[i]:
                pos_list.append((x, ypos_list[i]))
        return pos_list
    
    def convert_cords_to_position(self):
        return {(0,2):0, (0,3):1, (0,4):2, (1,2):3, (1,3):4, (1,4):5, (2,0):6, (2,1):7, (2,2):8, (2,3):9, (2,4):10, (2,5):11, (2,6):12, (3,0):13, (3,1):14, (3,2):15, (3,3):16, (3,4):17, (3,5):18, (3,6):19, (4,0):20, (4,1):21, (4,2):22, (4,3):23, (4,4):24, (4,5):25, (4,6):26, (5,2):27, (5,3):28, (5,4):29, (6,2):30, (6,3):31, (6,4):32}

    def get_position(self, pos):
        return self.positions[pos]


    def draw_board(self, board):
        # Draw hens nest
        pygame.draw.rect(self.win, (255, 255, 204), (self.width/2-self.slot_spacing, self.height/2+self.slot_spacing, self.slot_spacing*2, self.slot_spacing*2))
        # Draw lines
        self.draw_lines()
        # Draw positions
        for pos in self.positions:
            pygame.draw.circle(self.win, (0,0,0), pos, 15)
        # Highlight selected
        if self.selected is None:
            pygame.draw.circle(self.win, (101,255,0), self.get_position(self.pos_dict[self.selected_pos]), 25)
        # Draw pieces
        current_pos = 0
        for row in board.slots:
            for slot in row:
                if slot == None:
                    continue
                if slot.type == "Hen":
                    pygame.draw.circle(self.win, (255,255,0), self.positions[current_pos], 15)
                if slot.type == "Fox":
                    pygame.draw.circle(self.win, (255,0,0), self.positions[current_pos], 15)
                current_pos += 1

    
    def draw_lines(self):
        """Draw all lines, this is not hardcoding :)"""
        pygame.draw.line(self.win, (0,0,200), self.positions[0], self.positions[2], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[3], self.positions[5], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[6], self.positions[12], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[13], self.positions[19], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[20], self.positions[26], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[27], self.positions[29], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[30], self.positions[32], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[0], self.positions[30], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[1], self.positions[31], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[2], self.positions[32], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[6], self.positions[20], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[7], self.positions[21], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[11], self.positions[25], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[12], self.positions[26], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[0], self.positions[26], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[2], self.positions[20], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[6], self.positions[32], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[12], self.positions[30], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[8], self.positions[24], width=5)
        pygame.draw.line(self.win, (0,0,200), self.positions[10], self.positions[22], width=5)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #print("PRESS")
                if event.key == pygame.K_LEFT:
                    if self.selected_pos[0] < 2 or self.selected_pos[0] > 4:
                        if self.selected_pos[1] == 2:
                            return
                    elif self.selected_pos[0] >= 2 or self.selected_pos[0] <= 4:
                        if self.selected_pos[1] == 0:
                            return
                    self.selected_pos = (self.selected_pos[0], self.selected_pos[1]-1)
                    return 1

                elif event.key == pygame.K_RIGHT:
                    if self.selected_pos[0] < 2 or self.selected_pos[0] > 4:
                        if self.selected_pos[1] == 4:
                            return
                    elif self.selected_pos[0] >= 2 or self.selected_pos[0] <= 4:
                        if self.selected_pos[1] == 6:
                            return
                    self.selected_pos = (self.selected_pos[0], self.selected_pos[1]+1)
                    return 1
                elif event.key == pygame.K_UP:
                    if self.selected_pos[1] < 2 or self.selected_pos[1] > 4:
                        if self.selected_pos[0] == 2:
                            return
                    elif self.selected_pos[1] >= 2 or self.selected_pos[1] <= 4:
                        if self.selected_pos[0] == 0:
                            return
                    self.selected_pos = (self.selected_pos[0]-1, self.selected_pos[1])
                    return 1
                elif event.key == pygame.K_DOWN:
                    if self.selected_pos[1] < 2 or self.selected_pos[1] > 4:
                        if self.selected_pos[0] == 4:
                            return
                    elif self.selected_pos[1] >= 2 or self.selected_pos[1] <= 4:
                        if self.selected_pos[0] == 6:
                            return
                    self.selected_pos = (self.selected_pos[0]+1, self.selected_pos[1])
                    return 1

                elif event.key == pygame.K_1 or event.key == pygame.K_KP8:
                    self.direction = 0
                elif event.key == pygame.K_2 or event.key == pygame.K_KP9:
                    self.direction = 1
                elif event.key == pygame.K_3 or event.key == pygame.K_KP6:
                    self.direction = 2
                elif event.key == pygame.K_4 or event.key == pygame.K_KP3:
                    self.direction = 3
                elif event.key == pygame.K_5 or event.key == pygame.K_KP2:
                    self.direction = 4
                elif event.key == pygame.K_6 or event.key == pygame.K_KP1:
                    self.direction = 5
                elif event.key == pygame.K_7 or event.key == pygame.K_KP4:
                    self.direction = 6
                elif event.key == pygame.K_8 or event.key == pygame.K_KP7:
                    self.direction = 7


    def update(self, board):
        self.clock.tick(FPS)
        #print("Tick")
        something_happened = self.get_input()
        self.win.fill(BC)
        if something_happened == 1 or self.selected_piece is None:
            self.draw_board(board)
            pygame.display.update()
            





if __name__ == "__main__":
    w = Window()
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        w.update()