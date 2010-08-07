'''
Created on 02-08-2010

@author: ymir
'''
import networkx as nx
from thesis import sna

if __name__ == '__main__':

    gm = sna.GraphMaker("/home/ymir/eclipse/networkx-thesis/voting_ring.txt")
    gm.makeGraph()
    
    cl = sna.Cliquer(gm.graph)
    cl.sliceGraph(15)
#    cl.nativeCliquer()
    cl.graph = nx.erdos_renyi_graph(30, 0.05)
    cl.blodelAlgorithm()
    cl.newmanAlgorithm()
    cl.aaronNewmanAlgorithm()