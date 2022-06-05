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
        self.window = Window()
        self.buttons = [["Settings", None], ["Clear", None], ["Pause", None], ["Random", None]]

    # this function changes dead cells to living and vice versa
    def change_on_click(self):
        x, y = (self.mouse_pos[0] // BLOCK_SIZE, self.mouse_pos[1] // BLOCK_SIZE)
        print(x,y)
        if x >= ROWS or y >= COLUMNS:
            return None
        if self.grid[x][y] == None:
            self.grid[x][y] = 0
        else:
            self.grid[x][y] = None

    #creating next generation of GoL
    def next_generation(self):
        if self.pause:
            return None
        next_grid = [[None for y in range(ROWS)] for x in range(COLUMNS)] #empty grid to store values
        for x in range(COLUMNS):
            for y in range(ROWS):
                self.counter = 0
                for i, j in around_element:
                    if self.grid[(x+i) % COLUMNS][(y+j) % ROWS] != None: #modulo used -> table is looped
                        self.counter += 1
                if self.grid[x][y] == None:     #dead cells become alive
                    if self.born.get(self.counter):
                        next_grid[x][y] = 0
                else:
                    if self.survive.get(self.counter):
                        if self.grid[x][y] < len(SHADES) -1:     #living cells survive + change of color
                            next_grid[x][y] = self.grid[x][y] + 1
                        else:
                            next_grid[x][y] = self.grid[x][y]
                    else:
                        next_grid[x][y] = None
        self.grid = next_grid.copy()

    # creating settings button
    def generate_buttons(self):
        font = pygame.font.SysFont("arial", BLOCK_SIZE*2)
        left_coords = BLOCK_SIZE
        for button in self.buttons: 
            my_font = font.render(button[0], True, (0, 0, 255))
            button[1] = my_font.get_rect(topleft = (left_coords, HEIGHT+BLOCK_SIZE))
            pygame.draw.rect(self.surface, (114, 114, 114), button[1], 0)
            self.surface.blit(my_font, (left_coords, HEIGHT+BLOCK_SIZE))
            left_coords = left_coords + button[1].width + BLOCK_SIZE





    def print_grid(self):
        for x in range(ROWS):
            for y in range(COLUMNS):
                if self.grid[x][y] != None:
                    rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.surface, SHADES[self.grid[x][y]], rect, 0)

    def clear_grid(self):
        for x in range(COLUMNS):
            for y in range(ROWS):
                self.grid[x][y] = None 

    def pause_game(self):
        self.pause = not self.pause

    def random_game(self):
        for x in range(COLUMNS):
            for y in range(ROWS):
                if bool(random.getrandbits(1)):
                    self.grid[x][y] = 0
                else:
                    self.grid[x][y] = None
                     

    
    def mouse_clicked(self):
        self.change_on_click()
        if self.buttons[0][1].collidepoint(self.mouse_pos):
            self.window.show_window()                       #creating window as a new object
            self.survive = self.window.old_survive.copy()  #updating conditions
            self.born = self.window.old_born.copy()
        if self.buttons[1][1].collidepoint(self.mouse_pos):
            self.clear_grid()
        if self.buttons[2][1].collidepoint(self.mouse_pos):
            self.pause_game()
        if self.buttons[3][1].collidepoint(self.mouse_pos):
            self.random_game()


    def run(self):
        running = True
        while running:
            self.surface.fill(BLACK)
            for event in pygame.event.get():
                if event.type == QUIT:
                        running = False
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        self.pause_game()
                if event.type == MOUSEBUTTONDOWN:
                    self.mouse_pos = pygame.mouse.get_pos()
                    self.mouse_clicked()
            self.print_grid()
            self.generate_buttons()
            time.sleep(self.time)
            pygame.display.update()
            self.next_generation()


class Window(object):
    def __init__(self) -> None:
        self.root = None
        self.new_survive = []
        self.new_born = []
        self.checkboxes_survive=[]
        self.checkboxes_born = []
        self.old_survive = {0: False, 1: False, 2:True, 3:True, 4:False, 5:False, 6:False, 7:False, 8:False}
        self.old_born = {0: False, 1: False, 2:False, 3:True, 4:False, 5:False, 6:False, 7:False, 8:False}

    def show_window(self):
        self.root = tk.Tk()
        self.new_survive = [tk.BooleanVar() for x in range (9)]
        self.new_born = [tk.BooleanVar() for x in range (9)]
        self.root.title('Settings')
        self.root.geometry("")
        self.root.resizable(True, True)

        self.checkboxes_survive=[]
        self.checkboxes_born = []

        self.label_survive = tk.Label(self.root, text='Survive')
        self.label_survive.grid(column = 0, columnspan= 9, row = 0)
        
        self.label_born = tk.Label(self.root, text='Born')
        self.label_born.grid(column = 0, columnspan= 9, row = 3)            
        
        for i in range(9):              #creating all checkboxes 
            self.checkboxes_survive.append(tk.Checkbutton(self.root, text=str(i), variable = self.new_survive[i]))
            self.checkboxes_born.append(tk.Checkbutton(self.root, text=str(i), variable = self.new_born[i]))
            if self.old_survive[i]:
                self.checkboxes_survive[i].select()
            self.checkboxes_survive[i].grid(column = i, row = 1)
            if self.old_born[i]:
                self.checkboxes_born[i].select()
            self.checkboxes_born[i].grid(column = i, row = 4)

        self.save_button = tk.Button(self.root, text = "Save", command = self.save_values)
        self.save_button.grid(column = 0, columnspan= 9, row = 5)
        self.root.mainloop()

        
    def save_values(self):
        for i in range(9):
            self.old_survive[i] = self.new_survive[i].get()
            self.old_born[i] = self.new_born[i].get()
        self.root.destroy()
        
        

if __name__ == "__main__":
    game = Game()
    game.run()