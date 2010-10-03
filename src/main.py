#!/usr/bin/env python

'''
Created on 02-08-2010

@author: ymir
'''
import networkx as nx
from thesis import sna
from thesis import test_blondel
from thesis import experiment


if __name__ == '__main__':
#    test_blondel.test_main()

    experiment.assertKarate()

#    gm = sna.GraphMaker("/home/ymir/eclipse/networkx-thesis/voting_ring.txt")
#    gm.makeGraph()
#    cl = sna.Cliquer(gm.graph)
#    cl.sliceGraph(3)
#    pp = cl.MCLAlgorithm()
#    cl.prettyPlotter(l=pp, filename="n.png")

    

#    dm = sna.DataMaker("/home/ymir/eclipse/networkx-thesis/testing-ring.txt")
#    dm.generate()
#
#    
#    cl = sna.Cliquer(gm.graph)
#    cl.sliceGraph(3)
##    cl.nativeCliquer()
##    cl = sna.Cliquer(nx.erdos_renyi_graph(30, 0.05))
##    pp = cl.blodelAlgorithm()
##    cl.prettyPlotter(d=pp)
##    pp = cl.newmanAlgorithm()
##    cl.prettyPlotter(l=pp, filename="n.png")
#    pp = cl.causetNewmanAlgorithm()
#    cl.prettyPlotter(l=pp)