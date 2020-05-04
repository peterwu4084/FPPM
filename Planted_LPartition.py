from itertools import combinations
from random import random
from networkx import Graph

class Planted_LPartition(Graph):
    '''
    A class to generate networks by the planted l-partition model.

    Parameters
    ----------
    l : int
        The number of communities.
    Nc : int
        The size of each community.
    pin : float, between 0 and 1
        The probability that two vertices inside the same community
        are connected.
    pout : float between 0 and 1
        The probability that two vertices in different communities
        are connected.
    '''
    def __init__(self, l, Nc, pin, pout):
        super().__init__()
        vertices = [(c*Nc + i, {'value': c}) for c in range(l) for i in range(Nc)]
        self.add_nodes_from(vertices)

        for m, n in combinations(range(l*Nc), 2):
            if self.nodes[m]['value'] == self.nodes[n]['value']:
                if random() < pin:
                    self.add_edge(m, n)
            else:
                if random() < pout:
                    self.add_edge(m, n)
                    