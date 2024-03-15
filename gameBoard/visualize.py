import sys
import pygame


class Visualize:
    def __init__(self):
        pygame.init()

        # define board size
        self.Height = 15
        self.Width = 15
        # define colors
        self.BLACK = (41, 36, 33)
        self.WHITE = (255, 245, 238)
        self.BROWN = (174, 112, 0)
        self.BLUE = (68, 206, 246)
        self.YELLOW = (210, 180, 140)

        # define board and piece position and size
        self.WINDOW_SIZE = (700, 700)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.pieces_surface = pygame.Surface(self.WINDOW_SIZE, pygame.SRCALPHA)
        self.highlight_surface = pygame.Surface(self.WINDOW_SIZE, pygame.SRCALPHA)

        # set window title
        pygame.display.set_caption("gobang")

        # fill background
        self.screen.fill(self.YELLOW)

        # define font
        self.font = pygame.font.Font(None, 40)

        # define board and piece position and size
        self.BOARD_POSITION = (50, 50)
        self.CELL_SIZE = 40
        self.BOARD_SIZE = (self.CELL_SIZE * self.Height, self.CELL_SIZE * self.Width)

    # draw board
    def draw_board(self):
        """Draw the board"""
        for i in range(self.Height + 1):
            pygame.draw.line(self.screen, self.BLACK,
                             (self.BOARD_POSITION[0], self.BOARD_POSITION[1] + i * self.CELL_SIZE),
                             (self.BOARD_POSITION[0] + self.BOARD_SIZE[0], self.BOARD_POSITION[1] + i * self.CELL_SIZE))
        for i in range(self.Width + 1):
            pygame.draw.line(self.screen, self.BLACK,
                             (self.BOARD_POSITION[0] + i * self.CELL_SIZE, self.BOARD_POSITION[1]),
                             (self.BOARD_POSITION[0] + i * self.CELL_SIZE, self.BOARD_POSITION[1] + self.BOARD_SIZE[1]))
        pygame.display.update()

    # draw piece
    def draw_piece(self, pos, color):
        """Draw a piece on the board, highlight the latest piece"""
        # print(pos)
        self.highlight_surface.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.circle(self.pieces_surface, color, (
            self.BOARD_POSITION[0] + pos[0] * self.CELL_SIZE, self.BOARD_POSITION[1] + pos[1] * self.CELL_SIZE), 15)
        pygame.draw.circle(self.highlight_surface, self.BLUE, (
            self.BOARD_POSITION[0] + pos[0] * self.CELL_SIZE, self.BOARD_POSITION[1] + pos[1] * self.CELL_SIZE), 15,
                           width=3)
        self.screen.blits([(self.pieces_surface, (0, 0)), (self.highlight_surface, (0, 0))])
        pygame.display.update()

    # draw end screen
    def draw_end_screen(self, winner):
        """Draw the end screen"""
        if winner == 1:
            text = self.font.render("Black wins!", True, self.BLACK)
        elif winner == 2:
            text = self.font.render("White wins!", True, self.BLACK)
        else:
            text = self.font.render("Draw!", True, self.BLACK)

        # Text background
        pygame.draw.rect(self.screen, self.WHITE, (
            self.WINDOW_SIZE[0] / 2 - text.get_width() / 2 - 10, self.WINDOW_SIZE[1] / 3 - text.get_height() / 2 - 10,
            text.get_width() + 20, text.get_height() + 20))
        pygame.draw.rect(self.screen, self.BLACK, (
            self.WINDOW_SIZE[0] / 2 - text.get_width() / 2 - 10, self.WINDOW_SIZE[1] / 3 - text.get_height() / 2 - 10,
            text.get_width() + 20, text.get_height() + 20), width=3)
        # Text
        self.screen.blit(text, (
            self.WINDOW_SIZE[0] / 2 - text.get_width() / 2, self.WINDOW_SIZE[1] / 3 - text.get_height() / 2))
        pygame.display.update()

        # Restart and Quit buttons
        pygame.draw.rect(self.screen, self.WHITE,
                         (self.WINDOW_SIZE[0] / 2 - 115, self.WINDOW_SIZE[1] / 3 + 50, 110, 50))
        pygame.draw.rect(self.screen, self.BLACK,
                         (self.WINDOW_SIZE[0] / 2 - 115, self.WINDOW_SIZE[1] / 3 + 50, 110, 50), width=3)
        pygame.draw.rect(self.screen, self.WHITE, (self.WINDOW_SIZE[0] / 2 + 5, self.WINDOW_SIZE[1] / 3 + 50, 95, 50))
        pygame.draw.rect(self.screen, self.BLACK, (self.WINDOW_SIZE[0] / 2 + 5, self.WINDOW_SIZE[1] / 3 + 50, 95, 50),
                         width=3)

        text = self.font.render("Restart", True, self.BLACK)
        self.screen.blit(text, (self.WINDOW_SIZE[0] / 2 - 110 + 50 - text.get_width() / 2,
                                self.WINDOW_SIZE[1] / 3 + 50 + 25 - text.get_height() / 2))
        text = self.font.render("Quit", True, self.BLACK)
        self.screen.blit(text, (
            self.WINDOW_SIZE[0] / 2 + 55 - text.get_width() / 2,
            self.WINDOW_SIZE[1] / 3 + 50 + 25 - text.get_height() / 2))
        pygame.display.update()

        # Wait for user input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.WINDOW_SIZE[0] / 2 - 100 < mouse_x < self.WINDOW_SIZE[0] / 2 and \
                            self.WINDOW_SIZE[1] / 3 + 50 < mouse_y < self.WINDOW_SIZE[1] / 3 + 50 + 50:
                        return 0  # restart
                    elif self.WINDOW_SIZE[0] / 2 < mouse_x < self.WINDOW_SIZE[0] / 2 + 100 and \
                            self.WINDOW_SIZE[1] / 3 + 50 < mouse_y < self.WINDOW_SIZE[1] / 3 + 50 + 50:
                        return 1  # quit

    # get mouse click position
    def get_input(self):
        """Get the mouse click position"""
        # wait for user input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # round to the nearest cell
                    x = round((mouse_x - self.BOARD_POSITION[0]) / self.CELL_SIZE)
                    y = round((mouse_y - self.BOARD_POSITION[1]) / self.CELL_SIZE)
                    # check if the click is on the board if not ignore
                    if x < self.BOARD_SIZE[0] and y < self.BOARD_SIZE[1]:
                        return x, y
