#!/usr/bin/env python
import unittest
from test import test_support
from nose.tools import *

from thesis import blondel
import networkx as nx


class SimpleTestCase(unittest.TestCase):
    def setUp(self):
        from lib import karate_graph
        G = karate_graph.karate_graph()
        self.G = G
    
    def testComputeQ(self):
        self.G = nx.Graph()
        self.G = nx.path_graph(5)
        self.G.remove_node(0)
        for (startNode, endNode, data) in self.G.edges(data=True):
            data['weight'] = 1
        
        import matplotlib.pyplot as plt
        pos = nx.graphviz_layout(self.G, prog='neato')
        nx.draw(self.G, pos)
 
        B = blondel.BlondelClusterer(self.G)
        Q = B.computeQ()
        
#        plt.show()
#        print Q
        
        self.assertEqual(Q, 0)
    
#    def test(self):
#        partition = blondel.cluster(self.G)
#        # returns list o list of partiotions
        
        
def test_main():
    test_support.run_unittest(SimpleTestCase)

if __name__ == '__main__':
    test_main()
