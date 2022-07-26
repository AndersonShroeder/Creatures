
from math import inf
from re import X
from cv2 import Mat
from numpy import exp
import random as rand
from visualize import GraphVisualization
import numpy as np

innovations = {}
#node_innovations = {}

class ForwardProp:
    def __init__(self):
        pass

    def feedForward(self, genome, inputs): #New method possibly required - currently activations happen without complete sum - might not be a bad thing?
        output_vector = []
        #input step - somewhat workaround - nodes and inputs must be input in exact order. Possible fix = dictionary
        for index, node in enumerate(genome.input_nodes):
            node.sum = inputs[index]

        #for each connection we take the inNode sum multiply it by the connection weight and sum it to outNode sum
        check_list = []
        for gene in genome.connections:
            #print(gene.inNode.sum * gene.weight)
            gene.outNode.sum += gene.outNode.activation(gene.inNode.sum * gene.weight)

        #output step - another workaround - outputs must be read in exact/static order
        for i in genome.output_nodes:
            output_vector.append(i.activation(i.sum))

        #reset node values
        for node in genome.nodes:
            node.sum = 0

        return output_vector
ff = ForwardProp()

class NodeGene:
    def __init__(self, type:int, id):
        types = ['INPUT', 'HIDDEN', 'OUTPUT']
        self.type = types[type] # 0 = input, 1 = hidden, 2 = output
        self.id = id # id number of node

        #for feed forward loop - keep track of sum into node
        self.sum = 0
        self.activation_func = None
        self.activation_val = 0

    
    def __repr__(self):
        return str(self.id)
    
    def activation(self, num):
        return 1/(1+exp(-num))


class ConGene:
    def __init__(self, inNode, outNode, weight = 0.02, status = True):
        self.inNode = inNode
        self.outNode = outNode
        self.weight = weight
        self.status = status #enables or disables the gene connection
        self.id = self.gen_id()# represents innovation number for crossover
         
    def __repr__(self):
        if self.status == True:
            return str([self.inNode.id, self.outNode.id])  
        else: return "-"
        #return str([{self.inNode: self.inNode.type}, {self.outNode:self.outNode.type}])

    def gen_id(self):
        lst = (self.inNode, self.outNode)
        if lst not in innovations:
            if innovations:
                max_ = max(innovations.values())
            else:
                max_ = 0
            innovations[lst] = max_ + 1
        else:
            self.id = innovations[lst]


class Genome:
    def __init__(self, connections, nodes):
        self.connections = connections
        self.nodes = nodes

    def mutate_con(self, connection:ConGene): #method losses effectiveness the more dense the network is
        valid = False
        v = True

        #generate random choices and check if valid - for loop prevents infinite while loop if there are no valid connections
        for i in range(len(self.nodes)):
            inNode = rand.choice(self.nodes)
            outNode = rand.choice(self.nodes)
            if outNode.type != 'INPUT' and outNode != inNode:
                valid = True
                break

        if valid:
            #Check if generated value is not in list
            for i in self.connections:
                if [i.inNode, i.outNode] == [inNode, outNode]:
                    v = False
            if v:   
                self.connections.append(ConGene(inNode, outNode))


    def mutate_node(self, connection:ConGene, r):
        #generate new connection
        new_node  = NodeGene(1, len(self.nodes)+1)
        self.nodes.append(new_node)
        self.connections.append(ConGene(new_node, connection.outNode))

        #update old connection status to false
        self.connections[r].status = False

        #create new connection from old in node
        self.connections.append(ConGene(connection.inNode, new_node, connection.weight))


    def mutate_status(self, connection:ConGene):
        connection.status = not connection.status

    
    def mutate_weight_multi(self, connection:ConGene, factor = .08):
        connection.weight *= factor


    def mutate_weight_random(self, connection:ConGene):
        connection.weight *= rand.uniform(-2, 2) # random float between -2 and 2
    

    def mutate(self, mutation_rate):
        mutation = True if rand.randint(0, 100) <= mutation_rate * 100 else False
        
        if mutation:
            if self.connections:
                r = rand.randint(0, len(self.connections) - 1)
                connection:ConGene = self.connections[r]

                #some mutations happen more frequently - this simulates
                prob = rand.randint(1, 100)
                if prob <= 25:
                    self.mutate_node(connection, r)

                if prob > 25 and prob <= 60:    
                    self.mutate_status(connection)

                else:
                    lst = [self.mutate_con, self.mutate_weight_multi, self.mutate_weight_random]
                    rand.choice(lst)(connection)


            else:
                self.mutate_con(connection=None)

    def crossover(self, second):
        # Find matching genes in order to randomly assign to new genome
        pass

class Test:
    def __init__(self, x, y):
        self.input_nodes = []
        self.output_nodes = []
        self.nodes = []
        self.connections = []
        self.x = x
        self.y = y
        self.genome = None
        self.food = 40
        self.inputs = None

    def __repr__(self):
        return str(self.food)

    def generate_input(self, num_input):
        for i in range(num_input):
            node = NodeGene(0, i + 1)
            self.input_nodes.append(node)
            self.nodes.append(node)
    
    def generate_output(self, num_output):
        for i in range(num_output):
            node =NodeGene(2, 1+len(self.nodes))
            self.output_nodes.append(node)
            self.nodes.append(node)

    def generate_empty(self, num_input, num_output):
        self.generate_input(num_input)
        self.generate_output(num_output)
        self.genome = Genome(self.connections, self.nodes)

    def mutate_xgen(self, num_generations, rate):
        for i in range(num_generations):
            self.genome.mutate(rate)
            self.inputs = [i.sum for i in self.input_nodes]
            ff.feedForward(self, self.inputs)
            # if i%200 == 0:
            #     self.visualize()
            #print(f"Generation {i + 1}: {self.genome.connections}")

    def visualize(self):
        G = GraphVisualization()
        cons = [i for i in self.genome.connections if i.status == True]
        nds = self.genome.nodes
        G.graph(nds, cons)

class MatrixRep:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.creatures = []
        self.lst = []
        self.output = None

    def build(self):
        self.lst = np.zeros((self.rows, self.cols), dtype=object)

    def spawn(self, num):
        for i in range(num):
            check = True
            while check:
                randx = rand.randint(0, self.cols - 1)
                randy = rand.randint(0, self.rows - 1)
                if self.lst[randy][randx] == 0:
                    check = False
            creature = Test(randx, randy)
            creature.generate_empty(2, 4)
            self.creatures.append(creature)
            self.lst[randy][randx] = creature
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
            for y in self.lst:
                for x in self.lst:
                    if self.lst[y][x] == 2:
                        dist = abs(y - cy) + abs(x - cx)
                        if dist < close_dist:
                            cur_close = [y, x]

            creature.input_nodes[0].sum = cur_close[0]
            creature.input_nodes[1].sum = cur_close[1]

    def forward_pass(self):
        for creature in self.creatures:
            creature.mutate_xgen(1, 1)
            self.output = ff.feedForward(creature, creature.inputs) #place holder feedforward -need to integrate


    def move(self):
        for creature in self.creatures:
            out = self.output
            self.lst[creature.y][creature.x] = 0
            if out[0] > .5 and creature.x != 0 and self.lst[creature.y][creature.x - 1] == 0: #left movement
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
            creature.food -= 2
            self.lst[creature.y][creature.x] = creature
        
    def check_status(self):
        for creature in self.creatures:
            if creature.food <= 0:
                self.creatures.remove(creature)

    def run(self, turns, gens):
        self.build()
        self.spawn(1)
        for i in range(gens):
            for i in range(turns):
                self.forward_pass()
                self.move()
                self.check_status()
            print(self.lst)


# test1 = Test()
# test1.generate_empty(12, 6)
# test1.mutate_xgen(1000, .01)


matr = MatrixRep(5, 5)
matr.run(500, 10)
