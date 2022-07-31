from math import inf
import random as rand
from time import sleep, time
import numpy as np
import os
from Entities import Actor

class MatrixRep:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.creatures = []
        self.lst = []
        self.output = None

    def build(self):
        self.lst = np.zeros((self.rows, self.cols), dtype=object)

    def spawn(self, num, food = True, creature = True):
        if creature:
            for i in range(num):
                check = True
                while check:
                    randx = rand.randint(0, self.cols - 1)
                    randy = rand.randint(0, self.rows - 1)
                    if self.lst[randy][randx] == 0:
                        check = False
                    
                creature = Actor(randx, randy)
                creature.generate_mutated(2, 4, 0)
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
                self.lst[randy][randx] = 2

    def get_inputs(self):
        for creature in self.creatures:
            #Find closest food only right now - search
            cx, cy = creature.x, creature.y
            cur_close = None
            close_dist = inf
            for y in range(len(self.lst)):
                for x in range(len(self.lst)):
                    if self.lst[y][x] == 2:
                        dist = abs(y - cy) + abs(x - cx)
                        if dist < close_dist:
                            cur_close = [y, x]

            creature.input_nodes[0].sum = cur_close[0]
            creature.input_nodes[1].sum = cur_close[1]

    def forward_pass(self):
        self.get_inputs()
        for creature in self.creatures:
            creature.time_step()


    def move(self):
        for creature in self.creatures:
            out = creature.output_vector
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
                creature.food = 40
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
                self.spawn(1, food = False)

    def run(self, turns, gens):
        self.build()
        self.spawn(1)
        self.spawn(3, creature=False)
        for i in range(gens):
            print(f"{self.lst}")
            for i in range(turns):
                self.forward_pass()
                self.move()
                self.check_status()
            
            #sleep(1)


world = MatrixRep(10, 10)
world.run(2, 400)