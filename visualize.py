import networkx as nx
import matplotlib.pyplot as plt
   
  
# Defining a Class
class GraphVisualization:
   
    def __init__(self):
          
        # visual is a list which stores all 
        # the set of edges that constitutes a
        # graph
        self.visual = []
          
    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
          
    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self, nodes):
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(self.visual)
        nx.draw_networkx(G, node_size = 20, with_labels=False, linewidths = .5
                        )
        plt.axis('off')
        plt.show()
  
    def graph(self, nodes, connections):
        for i in connections:
            i, j = i.inNode.id, i.outNode.id
            self.addEdge(i, j)
        self.visualize(nodes)



nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
lst = [[17, 19], [19, 21], [10, 20], [20, 13], [21, 13]]
temp = []
