'''
Created on 03-10-2010

@author: ymir
'''


import networkx as nx
from thesis import sna
from thesis import logger
from lib import  karate_graph


def karateClub():
    karateG = karate_graph.karate_graph()
    cq = sna.Cliquer(karateG)
    
    logger.info("Karate Graph experiment... ")
    partition = cq.blondelAlgorithm()
    cq.prettyPlotter(l=partition, filename="karate_blondel.png")
    
    partition = cq.newmanAlgorithm()
    cq.prettyPlotter(l=partition, filename="karate_newman.png")
    
    
    partition = cq.causetNewmanAlgorithm()
    cq.prettyPlotter(l=partition, filename="karate_causet_newman.png")
    
    partition = cq.MCLAlgorithm(2.0)
    cq.prettyPlotter(l=partition, filename="karate_MCL.png")
    
    logger.info("Karate Graph experiment done")
    
def sixtyOne(sliceLevels = [3], plot=False):
    gm = sna.GraphMaker("/home/ymir/eclipse/networkx-thesis/voting_ring.txt")
    gm.makeGraph()
    
    
    for sliceLevel in sliceLevels:
        cq = sna.Cliquer(gm.graph)
        cq.sliceGraph(sliceLevel)
        
        partition = cq.blondelAlgorithm(verbose={'groups':2})
        if plot:
            cq.prettyPlotter(l=partition)
        
#        partition = cq.newmanAlgorithm(verbose=True)
#        if plot:
#            cq.prettyPlotter(l=partition)
#        
        partition = cq.causetNewmanAlgorithm(verbose={'groups':2})
        if plot:
            cq.prettyPlotter(l=partition)
        
        partition = cq.MCLAlgorithm(verbose={'groups':2})
        if plot:
            cq.prettyPlotter(l=partition)
            

def generated(sliceLevels = [3], plot=False):
    dm = sna.DataMaker("/home/ymir/eclipse/networkx-thesis/testing-ring.txt")
    dm.generate(number = 1, size = 25, target_size = 10, legible_target_size = 10, VOTERS=5000, OBJECTS=1000, bad_hideout=False)
    gm = sna.GraphMaker("/home/ymir/eclipse/networkx-thesis/testing-ring.txt")
    gm.makeGraph()
    
    
    for sliceLevel in sliceLevels:
#        for edge in gm.graph.edges(data=True):
#            print edge

        
        cq = sna.Cliquer(gm.graph)      
        cq.sliceGraph(sliceLevel)
        
#        for edge in cq.graph.edges(data=True):
#            print edge       
         
        partition = cq.blondelAlgorithm(verbose={'groups':10})
        if plot:
            cq.prettyPlotter(l=partition)
        
        #        partition = cq.newmanAlgorithm(verbose=True)
        #        if plot:
        #            cq.prettyPlotter(l=partition)
        #        
#        partition = cq.causetNewmanAlgorithm(verbose={'groups':10})
#        if plot:
#            cq.prettyPlotter(l=partition)
        
        partition = cq.MCLAlgorithm(inflation=5, verbose={'groups':10})
        if plot:
            cq.prettyPlotter(l=partition)


        
        
        
    
    