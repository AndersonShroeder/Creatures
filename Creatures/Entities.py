import Genomes

class Actor:
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


    def generate_input(self, num_input): #Creates NodeGenes that are tagged as inputs and added to input node list
        for i in range(num_input):
            node = Genomes.NodeGene(0, i + 1)
            self.input_nodes.append(node)
            self.nodes.append(node)
    

    def generate_output(self, num_output): #Same as generate_input but for outputs
        for i in range(num_output):
            node = Genomes.NodeGene(2, 1+len(self.nodes))
            self.output_nodes.append(node)
            self.nodes.append(node)


    def generate_empty(self, num_input, num_output):
        self.generate_input(self, num_input)
        self.generate_output(self, num_output)
        self.genome = Genomes.Genome(self.connections, self.nodes)


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




N = Actor(1,1)