#!/usr/bin/python

import networkx as nx

class BlondelClusterer(object):
    def __init__(self, Graph):
        self.G = Graph
        # initially every node is in different cluster
        for nodeNo in xrange(1, self.G.number_of_nodes()+1):
            self.G.node[nodeNo]['cluster'] = nodeNo
        self.Q = self.computeQ()
        self.clusters = []

    def computeQ(self):
        
        self.m = 0.5 * sum([data['weight'] for startNode, endNode, data in self.G.edges_iter(data=True)])
        
        total = 0.0
        
        for nodeNo in xrange(1, self.G.number_of_nodes()+1):
            for secondNodeNo in xrange(nodeNo+1, self.G.number_of_nodes()+1):
                if not sigma(self.G.node[nodeNo]['cluster'], self.G.node[secondNodeNo]['cluster']):
                    continue
                else:
                    Aij = self.G[nodeNo][secondNodeNo]['weight']
                    

                    
                    ki = self.sumOfAdjacentEdges(nodeNo)
                    kj = self.sumOfAdjacentEdges(secondNodeNo)
                    
                    total += Aij - ki*kj/2*self.m
                    
        return total
    
        
    def sumOfAdjacentEdges(self, nodeNo, cluster = None):
        sum = 0.0
        for key, value in self.G[nodeNo].iteritems():
                if not cluster or self.G.node[key]['cluster'] == cluster:
                    sum += value['weight']
        return sum


    def phaseOne(self):
        for node, data in self.G.nodes_iter(data=True):
            for buddyNode in self.G[node].iterkeys():
                oldCluster = data['cluster']
                data['cluster'] = self.G.node[buddyNode]['cluster'] # join buddy's cluster
                q = self.computeQ() 
            if q > self.Q:
                self.Q = q
            else:
                data['cluster'] = oldCluster
    
    
    
    
############################################################################    
    # currently deprecated
    def sumOfWeightsInsideCluster(self, cluster):
        copyG = self.G.copy()
        for node, data in copyG.nodes_iter(data=True):
            if data['cluster'] != cluster:
                copyG.remove_node(node)
        
        return sum([data['weight'] for startNode, endNode, data in copyG.edges_iter(data=True)])
        
    # TODO depracated, it may occur faster to compute basic Q again
    def computeDeltaQ(self, node, cluster):
        ki = self.sumOfAdjacentEdges(node)
        ki_in = self.sumOfAdjacentEdges(node, cluster)
        Ein = self.sumOfWeightsInsideCluster(cluster)
        
                
def sigma(cluster1, cluster2):
    if cluster1 == cluster2:
        return 1
    else:
        return 0