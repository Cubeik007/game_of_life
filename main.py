from tkinter.tix import COLUMN
import pygame
import random
from pygame.locals import *
import time

pygame.font.init()

#global variables


BLOCK_SIZE = 10
ROWS = 30
COLUMNS = 30
WIDTH = BLOCK_SIZE*COLUMNS
HEIGHT = BLOCK_SIZE*ROWS
LOWER_WIDTH = BLOCK_SIZE*5
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
SHADES = (WHITE, (172,203,255), (146,187,255), (120,170,255), (100,158,255), (65,136,255))
DEFAULT_TIME = 0.2
around_element = [(i,j) for i in (-1, 1, 0) for j in (-1, 1, 0)][:-1]


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT+LOWER_WIDTH))
        self.surface.fill(BLACK)
        self.grid = [[None for y in range(ROWS)] for x in range(COLUMNS)]
        self.survive = [2, 3]
        self.born = [3]
        self.time = DEFAULT_TIME
        self.pause = True
        self.counter = 0

    def change_on_click(self, pos):
        x, y = (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)
        print(pos)
        print(x,y)
        if x >= ROWS or y >= COLUMNS:
            return None
        if self.grid[x][y] == None:
            self.grid[x][y] = 0
        else:
            self.grid[x][y] = None

    def next_generation(self):
        if self.pause:
            return None
        next_grid = [[None for y in range(ROWS)] for x in range(COLUMNS)]
        for x in range(COLUMNS):
            for y in range(ROWS):
                self.counter = 0
                for i, j in around_element:
                    if 0 <= x+i < COLUMNS and 0 <= y+j < ROWS:
                        if self.grid[x+i][y+j] != None:
                            self.counter += 1
                if self.grid[x][y] == None:
                    if self.counter in self.born:
                        next_grid[x][y] = 0
                else:
                    if self.counter in self.survive:
                        if self.grid[x][y] < len(SHADES) -1:
                            next_grid[x][y] = self.grid[x][y] + 1
                        else:
                            next_grid[x][y] = self.grid[x][y]
                    else:
                        next_grid[x][y] = None
        self.grid = next_grid.copy()

    def settings_button(self):
        font = pygame.font.SysFont("arial", BLOCK_SIZE*3)
        settings = font.render("Settings", True, WHITE)
        self.surface.blit(settings (BLOCK_SIZE, index*BLOCK_SIZE))
        rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.surface, SHADES[self.grid[x][y]], rect, 0)









    def print_grid(self):
        for x in range(ROWS):
            for y in range(COLUMNS):
                if self.grid[x][y] != None:
                    rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.surface, SHADES[self.grid[x][y]], rect, 0)
            

    def run(self):
        running = True
        while running:
            self.surface.fill(BLACK)
            for event in pygame.event.get():
                if event.type == QUIT:
                        running = False
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        self.pause = not self.pause
                        print(self.pause)
                if event.type == MOUSEBUTTONDOWN:
                        self.change_on_click(pygame.mouse.get_pos())
            self.print_grid()
            time.sleep(self.time)
            pygame.display.update()
            self.next_generation()


                  


if __name__ == "__main__":
    game = Game()
    game.run()