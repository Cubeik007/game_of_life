from tkinter.tix import COLUMN
import pygame
import random
from pygame.locals import *
import time

pygame.font.init()

#global variables


BLOCK_SIZE = 10
ROWS = 60
COLUMNS = 60
WIDTH = BLOCK_SIZE*COLUMNS
HEIGHT = BLOCK_SIZE*ROWS
LOWER_WIDTH = BLOCK_SIZE*20
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
SHADES = (WHITE, (172,203,255), (146,187,255), (120,170,255), (100,158,255), (65,136,255))
DEFAULT_TIME = 0.2


class Game(object):

    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT+LOWER_WIDTH))
        self.surface.fill(BLACK)
        self.grid = [[False for y in range(ROWS)] for x in range(COLUMNS)]
        self.active_blocks = []
        self.color_of_blocks = []
        self.survive = [2, 3]
        self.born = [3]
        self.time = DEFAULT_TIME

    def change_on_click(self, pos):
        x, y = (pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE)
        print(pos)
        print(x,y)
        if x > ROWS or y > COLUMNS:
            return None
        self.grid[x][y] = not self.grid[x][y]
        if self.grid[x][y]:
            self.active_blocks.append((x,y))
            self.color_of_blocks.append(0)
        else:
            self.active_blocks.pop(self.active_blocks.index((x,y)))
            self.colors_of_blocks.pop(self.active_blocks.index((x,y)))

    def print_grid(self):
        for index, block in enumerate(self.active_blocks):
            rect = pygame.Rect(block[0]*BLOCK_SIZE, block[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.surface, SHADES[self.color_of_blocks[index]], rect, 0)
            if self.color_of_blocks[index] < len(SHADES) - 1:
                self.color_of_blocks[index] += 1


    def run(self):
        running = True
        while running:
            self.surface.fill(BLACK)
            for event in pygame.event.get():
                if event.type == QUIT:
                        running = False
                if event.type == KEYDOWN:
                    """if event.key == K_LEFT:
                        self.move_shape_left()
                    if event.key == K_RIGHT:
                        self.move_shape_right()
                    if event.key == K_UP:
                        self.rotate_shape()
                    if event.key == K_DOWN:
                        self.faster_time = 0.05"""
                    pass
                if event.type == MOUSEBUTTONDOWN:
                        self.change_on_click(pygame.mouse.get_pos())
            self.print_grid()
            time.sleep(self.time)
            pygame.display.update()


                  


if __name__ == "__main__":
    game = Game()
    game.run()