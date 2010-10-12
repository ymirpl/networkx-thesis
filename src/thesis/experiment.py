'''
Created on 03-10-2010

@author: ymir
'''

from __future__ import division
import networkx as nx
from thesis import sna
from thesis import logger
from lib import  karate_graph

class Experiment:
    graph = nx.Graph()
    rings = []
    result = []
    population = 0
    selectGroups = [1,2,3]    
    sliceLevels = [1,2,3,4]
    
    
    def __init__(self, testingDataPath = "/tmp/testing-ring.txt"):
        self.testingDataPath = testingDataPath
        self.dm = sna.DataMaker(self.testingDataPath)
        self.gm = sna.GraphMaker(self.testingDataPath)
        
 
    def compute(self, hardSliceLevel = 0, hardGroupsNo = 0, **kwargs ):
        '''
        @returns Forwards touple (matchRate, popRate) returned by Quality, if hardSilceLevel and hardGroupsNo
        '''
        
        logger.info("Will generate graph with params")
        logger.info(kwargs)
        
        self.dm.generate(**kwargs)
        self.graph = self.gm.makeGraph()
        self.population = self.graph.number_of_nodes()
        self.rings = sum(self.dm.voting_rings, []) # H-H-HHACKISH list flattening
        
        if hardSliceLevel:
            self.sliceLevels = [hardSliceLevel]
            
        for sliceLevel in self.sliceLevels:
            logger.info("Slice level: %d" % sliceLevel)
            cq = sna.Cliquer(self.graph)
            cq.sliceGraph(sliceLevel)
            self.result = cq.blondelAlgorithm()
            tuple = self.rateQuality(hardGroupsNo)
            
        if hardGroupsNo and hardSliceLevel:
            return tuple
            
            
    
    def rateQuality(self, hardGroupsNo = 0):
        '''
        @returns touple of matchRate and popRate if hardGroupsNo, for sake of plotting or smth
        '''
        logger.info("###### QUALITY SUMMARY ######")
        
        if hardGroupsNo:
            self.selectGroups = [hardGroupsNo]
        for i in self.selectGroups: # select first i groups
            matchCount = 0
            suspects = self.getFristNGroups(self.result, i)
            
            logger.debug("Suspects: ")
            logger.debug(suspects)
            
            for v in self.rings:
                if int(v) in suspects:
                    matchCount += 1
            
            matchRate = matchCount/len(self.rings) * 100.0
            popRate = len(suspects)/self.population * 100.0
            
            logger.info("Taking first %d groups match rate is %f. These groups are %f  of users population." % (i, matchRate, popRate))
        
        if hardGroupsNo:
            return (matchRate, popRate)
            
            
    
    def iterateParam(self, minValue = 10, maxValue = 25, step = 5, param = "target_size", hardSliceLevel = 0, hardGroupsNo = 0, **kwargs):
        '''
        @return Hard version returns tuple of two list, so that you can make some pretty plots =D
        '''
        
        kwargs[param] = minValue
        
        matchRates = []
        popRates = []
        
        while kwargs[param] <= maxValue:
            logger.info("Will iterate over %s : now it's %d:" % (param, kwargs[param]))
            tuple = self.compute(hardSliceLevel = hardSliceLevel, hardGroupsNo = hardGroupsNo, **kwargs)
            kwargs[param] += step
            
            if hardSliceLevel and hardGroupsNo:
                matchRates.append(tuple[0])
                popRates.append(tuple[1])
            
            
        if hardSliceLevel and hardGroupsNo:
            return (matchRates, popRates)

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


        
        
        
    
    