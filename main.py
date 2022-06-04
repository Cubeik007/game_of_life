from tkinter.tix import COLUMN
import pygame
import random
from pygame.locals import *
import time
import tkinter as tk

pygame.font.init()

#global variables


BLOCK_SIZE = 10
ROWS = 50
COLUMNS = 50
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
        self.survive = {0: False, 1: False, 2:True, 3:True, 4:False, 5:False, 6:False, 7:False, 8:False}
        self.born = {0: False, 1: False, 2:False, 3:True, 4:False, 5:False, 6:False, 7:False, 8:False}
        self.time = DEFAULT_TIME
        self.pause = True
        self.counter = 0
        self.settings_rect = None
        self.mouse_pos = (None, None)

    def change_on_click(self):
        x, y = (self.mouse_pos[0] // BLOCK_SIZE, self.mouse_pos[1] // BLOCK_SIZE)
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
                    if self.grid[(x+i) % COLUMNS][(y+j) % ROWS] != None:
                        self.counter += 1
                if self.grid[x][y] == None:
                    if self.born.get(self.counter):
                        next_grid[x][y] = 0
                else:
                    if self.survive.get(self.counter):
                        if self.grid[x][y] < len(SHADES) -1:
                            next_grid[x][y] = self.grid[x][y] + 1
                        else:
                            next_grid[x][y] = self.grid[x][y]
                    else:
                        next_grid[x][y] = None
        self.grid = next_grid.copy()

    def settings_button(self):
        font = pygame.font.SysFont("arial", BLOCK_SIZE*2)
        settings_text = font.render("Settings", True, (0, 0, 255))        
        self.settings_rect = settings_text.get_rect(topleft = (BLOCK_SIZE, HEIGHT+BLOCK_SIZE))
        pygame.draw.rect(self.surface, (114, 114, 114), self.settings_rect, 0)
        self.surface.blit(settings_text, (BLOCK_SIZE, HEIGHT+BLOCK_SIZE))

    def choise_window(self):
        self.root = tk.Tk()
        self.root.title('Settings')
        self.root.geometry("")
        self.root.resizable(True, True)
        self.label_survive = tk.Label(self.root, text='Survive')
        self.label_born = tk.Label(self.root, text='Born')
        self.label_survive.grid(column = 0, columnspan= 9, row = 0)
        self.label_born.grid(column = 0, columnspan= 9, row = 3)
        self.checkboxes_survive = []
        self.checkboxes_born = []
        self.new_survive = self.survive.copy()
        self.new_born = self.born.copy()
        for i in range(9):
            self.checkboxes_survive.append(tk.Checkbutton(self.root, text=str(i), command = lambda: self.new_values(0, i)))
            if self.survive[i]:
                self.checkboxes_survive[i].select()
            self.checkboxes_survive[i].grid(column = i, row = 1)
            self.checkboxes_born.append(tk.Checkbutton(self.root, text=str(i), command = lambda: self.new_values(1, i)))
            if self.born[i]:
                self.checkboxes_born[i].select()
            self.checkboxes_born[i].grid(column = i, row = 4)
        self.save_button = tk.Button(self.root, text = "Save", command = self.save_values)
        self.save_button.grid(column = 0, columnspan= 9, row = 5)
        self.root.mainloop()

    def new_values(self, type, number):
        print(number)
        if type == 0:
            print(type)
            self.new_survive[number] = not self.new_survive[number]
        if type == 1:
            self.new_born[number] = not self.new_born[number]


    def save_values(self):
        self.survive = self.new_survive
        self.born = self.new_born
        self.root.destroy()
        print(self.survive)



        # rect = pygame.draw.rect(self.surface, (114, 114, 114), (HEIGHT+1)*BLOCK_SIZE, BLOCK_SIZE, )
        # text_rect = settings.get_rect(center=rect.center)
        # self.game_screen.blit(settings, text_rect)
        #self.surface.blit(settings (BLOCK_SIZE, index*BLOCK_SIZE))
        # rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        # pygame.draw.rect(self.surface, SHADES[self.grid[x][y]], rect, 0)

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
                        self.mouse_pos = pygame.mouse.get_pos()
                        self.change_on_click()
                        if self.settings_rect.collidepoint(self.mouse_pos):
                            self.choise_window()
            self.print_grid()
            self.settings_button()
            time.sleep(self.time)
            pygame.display.update()
            self.next_generation()

"""
class Settings_window(object):

        def __init__(born, survive):
            root = tk.Tk()
            root.title('Settings')
            root.geometry("200x100")
            label_born = tk.Label(root, bg='white', width=20, text='Survive')
            label_born.grid(column = 0, columnspan= 8)
            checkboxes_survive = []
            labels_survive = []
            for i in range(8):
                    labels_survive.append(tk.Label(root,text=str(i)))
                    checkboxes_survive.append(tk.Checkbutton)
            c1 = tk.Checkbutton(root, text='Python', onvalue=1, offvalue=0)
            c1.pack()

        root.mainloop()

    def run(self):
        root = tk.Tk()
            root.title('Settings')
            root.geometry("200x100")
            label_born = tk.Label(root, bg='white', width=20, text='Survive')
            label_born.grid(column = 0, columnspan= 8)
            checkboxes_survive = []
            labels_survive = []
            for i in range(8):
                    labels_survive.append(tk.Label(root,text=str(i)))
                    checkboxes_survive.append(tk.Checkbutton)
            c1 = tk.Checkbutton(root, text='Python', onvalue=1, offvalue=0)
        

        root.mainloop()
"""
                  


if __name__ == "__main__":
    game = Game()
    game.run()