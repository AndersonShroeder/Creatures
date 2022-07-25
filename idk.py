import random as rand
from visualize import GraphVisualization

class NodeGene:
    def __init__(self, type:int, id):
        types = ['INPUT', 'HIDDEN', 'OUTPUT']
        self.type = types[type] # 0 = input, 1 = hidden, 2 = output
        self.id = id # id number of node
    
    def __repr__(self):
        return str(self.id)

class ConGene:
    def __init__(self, inNode, outNode, weight = 0, status = True, id = 0):
        self.inNode = inNode
        self.outNode = outNode
        self.weight = weight
        self.status = status #enables or disables the gene connection
        self.id = id # represents innovation number for crossover
    def __repr__(self):
        return str([self.inNode.id, self.outNode.id])
        #return str([{self.inNode: self.inNode.type}, {self.outNode:self.outNode.type}])

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
                self.connections.append(ConGene(inNode, outNode, 1, True))


    def mutate_node(self, connection:ConGene):
        #
        #generate new connection
        new_node  = NodeGene(1, len(self.nodes)+1)
        self.nodes.append(new_node)
        self.connections.append(ConGene(new_node, 
                                        connection.outNode, 
                                        connection.weight, 
                                        True, 
                                        len(self.connections)))

        #update old connection
        connection.outNode = new_node
        connection.weight = 1


    def mutate_status(self, connection:ConGene):
        connection.status = not connection.status

    
    def mutate_weight_multi(self, connection:ConGene, factor = .8):
        connection.weight *= factor


    def mutate_weight_random(self, connection:ConGene):
        connection.weight = rand.uniform(-2, 2) # random float between -2 and 2
    

    def mutate(self, mutation_rate):
        mutation = True if rand.randint(0, 100) <= mutation_rate * 100 else False
        
        if mutation:
            if self.connections:
                r = rand.randint(0, len(self.connections) - 1)
                connection:ConGene = self.connections[r]

                #some mutations happen more frequently - this simulates
                prob = rand.randint(1, 100)
                if prob <= 25:
                    self.mutate_node(connection)

                if prob > 25 and prob <= 60:    
                    self.mutate_status(connection)

                else:
                    lst = [self.mutate_con,self.mutate_weight_multi, self.mutate_weight_random]
                    rand.choice(lst)(connection)

            else:
                self.mutate_con(connection=None)
# 
class Test:
    def __init__(self):
        self.nodes = []
        self.connections = []
        self.genome = None

    def generate_input(self, num_input):
        for i in range(num_input):
            self.nodes.append(NodeGene(0, i + 1))
    
    def generate_output(self, num_output):
        for i in range(num_output):
            self.nodes.append(NodeGene(2, 1+len(self.nodes)))

    def generate_empty(self, num_input, num_output):
        self.generate_input(num_input)
        self.generate_output(num_output)
        self.genome = Genome(self.connections, self.nodes)

    def mutate_xgen(self, num_generations, rate):
        for i in range(num_generations):
            self.genome.mutate(rate)
            if i%50 == 0:
                self.visualize()
            #print(f"Generation {i + 1}: {self.genome.connections}")

    def visualize(self):
        G = GraphVisualization()
        cons = self.genome.connections
        nds = self.genome.nodes
        G.graph(nds, cons)

test = Test()
test.generate_empty(12, 6)
test.mutate_xgen(1000, .1)

