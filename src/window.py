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
        self.selected_pos = (-1, -1)
        self.direction = -1

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
    
    def get_position(self, pos):
        return self.positions[pos]


    def draw_board(self, board):
        # Draw lines
        self.draw_lines()
        # Draw positions
        for pos in self.positions:
            pygame.draw.circle(self.win, (0,0,0), pos, 15)
        # Highlight selected
        if self.selected is not None:
            pygame.draw.circle(self.win, (101,255,0), self.get_position(self.selected), 25)
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
                print("PRESS")

                if event.key == pygame.K_q:
                    self.selected = 0
                    self.selected_pos = (2,0)
                elif event.key == pygame.K_w:
                    self.selected = 1
                    self.selected_pos = (3,0)
                elif event.key == pygame.K_e:
                    self.selected = 2
                    self.selected_pos = (4,0)
                elif event.key == pygame.K_r:
                    self.selected = 3
                    self.selected_pos = (2,1)
                elif event.key == pygame.K_t:
                    self.selected = 4
                    self.selected_pos = (3,1)
                elif event.key == pygame.K_y:
                    self.selected = 5
                    self.selected_pos = (4,1)
                elif event.key == pygame.K_u:
                    self.selected = 6
                    self.selected_pos = (0,2)
                elif event.key == pygame.K_i:
                    self.selected = 7
                    self.selected_pos = (1,2)
                elif event.key == pygame.K_o:
                    self.selected = 8
                    self.selected_pos = (2,2)
                elif event.key == pygame.K_p:
                    self.selected = 9
                    self.selected_pos = (3,2)
                elif event.key == pygame.K_a:
                    self.selected = 10
                    self.selected_pos = (4,2)
                elif event.key == pygame.K_s:
                    self.selected = 11
                    self.selected_pos = (5,2)
                elif event.key == pygame.K_d:
                    self.selected = 12
                    self.selected_pos = (6,2)
                elif event.key == pygame.K_f:
                    self.selected = 13
                    self.selected_pos = (0,3)
                elif event.key == pygame.K_g:
                    self.selected = 14
                    self.selected_pos = (1,3)
                elif event.key == pygame.K_h:
                    self.selected = 15
                    self.selected_pos = (2,3)
                elif event.key == pygame.K_j:
                    self.selected = 16
                    self.selected_pos = (3,3)
                elif event.key == pygame.K_k:
                    self.selected = 17
                    self.selected_pos = (4,3)
                elif event.key == pygame.K_l:
                    self.selected = 18
                    self.selected_pos = (5,3)
                elif event.key == pygame.K_z:
                    self.selected = 19
                    self.selected_pos = (6,3)
                elif event.key == pygame.K_x:
                    self.selected = 20
                    self.selected_pos = (0,4)
                elif event.key == pygame.K_c:
                    self.selected = 21
                    self.selected_pos = (1,4)
                elif event.key == pygame.K_v:
                    self.selected = 22
                    self.selected_pos = (2,4)
                elif event.key == pygame.K_b:
                    self.selected = 23
                    self.selected_pos = (3,4)
                elif event.key == pygame.K_n:
                    self.selected = 24
                    self.selected_pos = (4,4)
                elif event.key == pygame.K_m:
                    self.selected = 25
                    self.selected_pos = (5,4)
                elif event.key == pygame.K_LEFT:
                    self.selected = 26
                    self.selected_pos = (6,4)
                elif event.key == pygame.K_UP:
                    self.selected = 27
                    self.selected_pos = (2,5)
                elif event.key == pygame.K_DOWN:
                    self.selected = 28
                    self.selected_pos = (3,5)
                elif event.key == pygame.K_RIGHT:
                    self.selected = 29
                    self.selected_pos = (4,5)
                elif event.key == pygame.K_9:
                    self.selected = 30
                    self.selected_pos = (2,6)
                elif event.key == pygame.K_0:
                    self.selected = 31
                    self.selected_pos = (3,6)
                elif event.key == pygame.K_PLUS:
                    self.selected = 32
                    self.selected_pos = (4,6)
                elif event.key == pygame.K_1:
                    self.direction = 0
                elif event.key == pygame.K_2:
                    self.direction = 1
                elif event.key == pygame.K_3:
                    self.direction = 2
                elif event.key == pygame.K_4:
                    self.direction = 3
                elif event.key == pygame.K_5:
                    self.direction = 4
                elif event.key == pygame.K_6:
                    self.direction = 5
                elif event.key == pygame.K_7:
                    self.direction = 6
                elif event.key == pygame.K_8:
                    self.direction = 7


    def update(self, board):
        self.clock.tick(FPS)
        print("Tick")
        self.get_input()
        self.win.fill(BC)
        self.draw_board(board)
        pygame.display.update()
            





if __name__ == "__main__":
    w = Window()
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        w.update()