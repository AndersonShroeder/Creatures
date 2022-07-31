from copy import deepcopy
from dataclasses import dataclass
from Genomes import Genome
import Genomes as Genomes
from visualize import GraphVisualization

@dataclass
class Actor:
    x: int
    y: int
    input_nodes = []
    output_nodes = []
    nodes = []
    connections = []
    mutation_rate: float = .05
    genome: Genome = None
    food: int = 40
    inputs: list = None
    output_vector = []

    def __repr__(self):
        return str(self.food)

    def generate_input(self, num_input): #Creates NodeGenes that are tagged as inputs and added to input node list
        self.input_nodes = [Genomes.NodeGene(0, i+1) for i in range(num_input)]
        self.nodes += self.input_nodes


    def generate_output(self, num_output): #Same as generate_input but for outputs
        self.output_nodes = [Genomes.NodeGene(2, i+len(self.nodes) + 1) for i in range(num_output)]
        self.nodes += self.output_nodes


    def generate_empty(self, num_input, num_output):
        self.generate_input(num_input)
        self.generate_output(num_output)
        self.genome = Genomes.Genome(self.connections, self.nodes)


    # generates a genome that has mutated connections
    def generate_mutated(self, num_input, num_output, number):
        self.generate_empty(num_input, num_output)
        self.genome.mutate_x(self.mutation_rate, number)


    def feedForward(self): #New method possibly required - currently activations happen without complete sum - might not be a bad thing?
        #input step - somewhat workaround - nodes and inputs must be input in exact order. Possible fix = dictionary
        self.output_vector = []
        for index, node in enumerate(self.input_nodes):
            node.sum = self.input_nodes[index].sum


        #for each connection we take the inNode sum multiply it by the connection weight and sum it to outNode sum
        for gene in self.genome.connections:
            #print(gene.inNode.sum * gene.weight)
            gene.outNode.sum += gene.outNode.activation(gene.inNode.sum * gene.weight)


        #output step - another workaround - outputs must be read in exact/static order
        for i in self.output_nodes:
            self.output_vector.append(i.activation(i.sum))

        #reset node values
        for node in self.genome.nodes:
            node.sum = 0


    def replicate(self):
        a = deepcopy(self)
        a.x -= 1
        a.y -= 1
        return a


    def time_step(self):
        self.genome.mutate(self.mutation_rate)
        self.feedForward()


    def visualize(self):
        G = GraphVisualization()
        cons = [i for i in self.genome.connections if i.status == True]
        nds = self.genome.nodes
        G.graph(nds, cons)

