#!/usr/bin/python

import networkx as nx

class BlondelClusterer(object):
    def __init__(self, Graph):
        self.G = Graph
        # initially every node is in different cluster
        for nodeNo in xrange(1, self.G.number_of_nodes()+1):
            self.G.node[nodeNo]['cluster'] = nodeNo
        self.computeQ()
        self.clusters = []

    def computeQ(self):
        
        m = 0.5 * sum([data['weight'] for startNode, endNode, data in self.G.edges_iter(data=True)])
        
        total = 0.0
        
        for nodeNo in xrange(1, self.G.number_of_nodes()+1):
            for secondNodeNo in xrange(nodeNo+1, self.G.number_of_nodes()+1):
                if not sigma(self.G.node[nodeNo]['cluster'], self.G.node[secondNodeNo]['cluster']):
                    continue
                else:
                    Aij = self.G[nodeNo][secondNodeNo]['weight']
                    
                    def sumOfAdjacentEdges(nodeNo):
                        sum = 0.0
                        for key, value in self.G[nodeNo].iteritems():
                            if key == 'cluster':
                                continue
                            else:
                                sum += value['weight']
                        return sum
                    
                    ki = sumOfAdjacentEdges(nodeNo)
                    kj = sumOfAdjacentEdges(secondNodeNo)
                    
                    total += Aij - ki*kj/2*m
                    
        return total
    
        
def sigma(cluster1, cluster2):
    if cluster1 == cluster2:
        return 1
    else:
        return 0