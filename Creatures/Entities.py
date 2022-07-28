from time import perf_counter
import Genomes as Genomes
from visualize import GraphVisualization
import numpy as np

class Actor:
    def __init__(self, x, y):
        self.input_nodes = []
        self.output_nodes = []
        self.nodes = []
        self.connections = []
        self.x = x
        self.y = y
        self.mutation_rate = .05
        self.genome = None
        self.food = 40
        self.inputs = None

    def __repr__(self):
        return str(self.food)


    def generate_input(self, num_input): #Creates NodeGenes that are tagged as inputs and added to input node list
        start1= perf_counter()
        self.input_nodes = [Genomes.NodeGene(0, i+1) for i in range(num_input)]
        self.nodes += self.input_nodes
        end1 = perf_counter()

        start = perf_counter()
        for i in range(num_input):
            node = Genomes.NodeGene(0, i + 1)
            self.input_nodes.append(node)
            self.nodes.append(node)
        end = perf_counter()
        print(end1 - start1)
        print(end - start)
        


    def generate_output(self, num_output): #Same as generate_input but for outputs
        for i in range(num_output):
            node = Genomes.NodeGene(2, 1+len(self.nodes))
            self.output_nodes.append(node)
            self.nodes.append(node)


    def generate_empty(self, num_input, num_output):
        self.generate_input(self, num_input)
        self.generate_output(self, num_output)
        self.genome = Genomes.Genome(self.connections, self.nodes)


    def feedForward(self): #New method possibly required - currently activations happen without complete sum - might not be a bad thing?
        output_vector = []

        #input step - somewhat workaround - nodes and inputs must be input in exact order. Possible fix = dictionary
        for index, node in enumerate(self.genome.input_nodes):
            node.sum = self.input_nodes[index]


        #for each connection we take the inNode sum multiply it by the connection weight and sum it to outNode sum
        check_list = []
        for gene in self.genome.connections:
            #print(gene.inNode.sum * gene.weight)
            gene.outNode.sum += gene.outNode.activation(gene.inNode.sum * gene.weight)


        #output step - another workaround - outputs must be read in exact/static order
        for i in self.genome.output_nodes:
            output_vector.append(i.activation(i.sum))

        #reset node values
        for node in self.enome.nodes:
            node.sum = 0

        return output_vector

    def time_step(self):
        self.genome.mutate(self.mutation_rate)
        self.feedForward()

    def visualize(self):
        G = GraphVisualization()
        cons = [i for i in self.genome.connections if i.status == True]
        nds = self.genome.nodes
        G.graph(nds, cons)



N = Actor(1, 1)
N.generate_input(30)