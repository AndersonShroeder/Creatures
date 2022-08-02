from copy import deepcopy
from math import inf
import random as rand
from time import sleep, time
import numpy as np
import os
from Entities import Food
from Entities import Actor
import pygame

WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OCR")

WHITE = (255,255,255)
BLACK = (0,0,0)



pygame.init()
font = pygame.font.Font(None, 120)

FPS = 60

class MatrixRep:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.creatures = []
        self.lst = []
        self.output = None
        self.dead = 0
        self.count = 0

    def build(self):
        for i in range(self.rows):
            self.lst.append([])
            for j in range(self.cols):
                self.lst[i].append(0)

    def movec(self, creature):
        check = True
        while check:
            randx = rand.randint(0, self.cols - 1)
            randy = rand.randint(0, self.rows - 1)
            if self.lst[randy][randx] == 0:
                check = False
        creature.genome.mutate(creature.mutation_rate)
        creature.y = randy
        creature.x = randx
        creature.row = randy * WIDTH/10
        creature.col = randx * WIDTH/10
        self.lst[randy][randx] = creature

    def spawn(self, num, food = True, creature = True):
        if creature:
            for i in range(num):
                check = True
                while check:
                    randx = rand.randint(0, self.cols - 1)
                    randy = rand.randint(0, self.rows - 1)
                    if self.lst[randy][randx] == 0:
                        check = False
                    
                creature = Actor(randx, randy, randx * WIDTH/num, randy * WIDTH/num, HEIGHT/num)
                creature.generate_mutated(2, 4, 10)
                self.creatures.append(creature)
                self.lst[randy][randx] = creature

        if food:
            for i in range(num):
                check = True
                while check:
                    randx = rand.randint(0, self.cols - 1)
                    randy = rand.randint(0, self.rows - 1)
                    if self.lst[randy][randx] == 0:
                        check = False
                self.lst[randy][randx] = Food(randx, randy, randx * WIDTH/num, randy * WIDTH/num, HEIGHT/num)

    def get_inputs(self):
        for creature in self.creatures:
            #Find closest food only right now - search
            cx, cy = creature.x, creature.y
            cur_close = None
            close_dist = inf
            for y in range(len(self.lst)):
                for x in range(len(self.lst)):
                    if type(self.lst[y][x]) is Food:
                        dist = abs(y - cy) + abs(x - cx)
                        if dist < close_dist:
                            cur_close = [y, x]

            creature.input_nodes[0].sum = cur_close[0] - creature.y
            creature.input_nodes[1].sum = cur_close[1] - creature.x

    def forward_pass(self):
        self.get_inputs()
        for creature in self.creatures:
            creature.time_step()


    def move(self):
        for creature in self.creatures:
            out = creature.output_vector
            #print(out)
            self.lst[creature.y][creature.x] = 0
            if out[0] > .5 and creature.x != 0: #left movement
                creature.x -= 1
                creature.food -=1
            if out[1] >.5 and creature.x != self.cols - 1: #right movement
                creature.x += 1
                creature.food -=1
            if out[2] > .5 and creature.y != 0:
                creature.y -= 1
                creature.food -=1
            if out[3] > .5 and creature.y != self.rows - 1:
                creature.y += 1
                creature.food -=1
            if self.lst[creature.y][creature.x] == 2:
                creature.food = 800
                creature.foodcol += 1
                new = creature.replicate()
                self.creatures.append(new)
                self.spawn(1, creature=False)
            creature.food -= 1
            self.lst[creature.y][creature.x] = creature
        
    def check_status(self):
        for creature in self.creatures:
            if creature.food <= 0:
                self.lst[creature.y][creature.x] = 0
                self.creatures.remove(creature)
            if len(self.creatures) == 0:
                self.dead += 4
                print(self.dead)
                self.spawn(4, food = False)

    def run(self, turns, gens):
        self.build()
        self.spawn(5)
        
        for i in range(gens):
            print(f"{self.lst}")
            for i in range(turns):
                self.forward_pass()
                self.move()
                self.check_status()
            
            #sleep(1)
        
    def evaluation(self):
        max_ = 0
        genome = None
        for creature in self.creatures:
            max_ = max(creature.foodcol, max_)
            if creature.foodcol == max_:
                if max_ > 0:
                    genome = creature.genome
            self.lst[creature.y][creature.x] = 0
        
        self.creatures = []
        self.spawn(5, food = False)
        if genome:
            for creature in self.creatures:
                creature.genome = deepcopy(genome)
                #pass

    

    def time_step(self, turns):
        for i in range(turns):
            self.forward_pass()
            self.move()
            #self.check_status()
            self.count += 1
        if self.count == 160:
            self.evaluation()
            self.count = 0
        
def draw_grid(start_x, start_y, end_x, end_y, win, number_blocks):
    blockSize = (end_x - start_x)//number_blocks #Set the size of the grid block
    for y in range(0, end_y - start_y, blockSize):
        for x in range(0, end_x- start_x, blockSize):
            rect = pygame.Rect(x+start_x, y+start_y, blockSize, blockSize) #create and draw grid
            pygame.draw.rect(win, BLACK, rect, 1)


def draw(win, grid):
    win.fill(BLACK)
    for index, row in enumerate(grid):
        for indexx, box in enumerate(row):
            if box == 0:
                pygame.draw.rect(win, WHITE, (indexx * HEIGHT/len(row), index * HEIGHT/len(row), HEIGHT/len(row), HEIGHT/len(row)))
            else:
                box.draw(win)

    #draw the grid
    #draw_grid(0, 0, 800, 800, WIN, 10)
    pygame.display.update()

def main(win):
    run = True
    clock = pygame.time.Clock()
    grid = MatrixRep(160, 160)
    grid.build()
    grid.spawn(50)
    #grid.spawn(4, creature=False)
    while run:
        grid.time_step(1)
        draw(win, grid.lst)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main(WIN)