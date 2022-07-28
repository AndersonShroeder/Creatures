from dataclasses import dataclass
from numpy import exp
import numpy.random as rand
innovations = {}


@dataclass
class NodeGene:
    type: int # 0 = input, 1 = hidden, 2 = output
    id: int # id number of node
    sum: int = 0
    activation_func: bool = None
    activation_val: int = 0

    def activation(self, num): # currently sigmoid
        return 1/(1+exp(-num))


@dataclass
class ConGene:

    inNode: NodeGene
    outNode: NodeGene
    weight: float
    status: bool = True #enables or disables the gene connection
    innovations = innovations
    id: int = None # represents innovation number for crossover

    def __post_init__(self):
        self.gen_id(self.innovations)

    def gen_id(self, innovations:dict):
        lst = (self.inNode, self.outNode)

        if lst not in innovations:
            innovations[lst] = len(innovations) + 1

        self.id = innovations[lst]
    
    


class Genome:
    def __init__(self, connections, nodes):
        self.connections = connections
        self.nodes = nodes

    def mutate_con(self, *args): #method losses effectiveness the more dense the network is
        valid = False
        v = True

        #generate random choices and check if valid - for loop prevents infinite while loop if there are no valid connections
        for i in self.nodes:
            inNode = rand.choice(self.nodes)
            outNode = rand.choice(self.nodes)
            if outNode.type != 'INPUT' and outNode != inNode:
                valid = True
                break

        if valid:
            #Check if generated value is not in list
            for i in self.connections:
                if [i.inNode, i.outNode] is [inNode, outNode]:
                    v = False
            if v:   
                self.connections.append(ConGene(inNode, outNode))


    def mutate_node(self, connection:ConGene):
        #generate new connection
        new_node  = NodeGene(1, len(self.nodes)+1)
        self.nodes.append(new_node)
        self.connections.append(ConGene(new_node, connection.outNode))

        #update old connection outNode to new inNode
        connection.outNode = new_node
        

    def mutate_status(self, connection:ConGene):
        connection.status = not connection.status

    
    def mutate_weight_multi(self, connection:ConGene, factor = .08):
        connection.weight *= factor


    def mutate_weight_random(self, connection:ConGene):
        connection.weight *= rand.uniform(-2, 2) # random float between -2 and 2
    

    def mutate(self, mutation_rate):
        mutation = True if rand.random(0, 100) <= mutation_rate else False
        
        if mutation:
            if self.connections:
                connection:ConGene = rand.choice(self.connections)

                #some mutations happen more frequently - this simulates
                prob = rand.randint(1, 100)
                if prob <= 25:
                    self.mutate_node(connection)

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