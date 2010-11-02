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
    selectGroups = [2,3,4]    
    sliceLevels = [1,2,3,4]
    
    
    def __init__(self, testingDataPath = "/tmp/testing-ring.txt"):
        self.testingDataPath = testingDataPath
        self.dm = sna.DataMaker(self.testingDataPath)
        self.gm = sna.GraphMaker(self.testingDataPath)
        
 
    def compute(self, hardGroupsNo = 0, runsNo = 1, **kwargs ):
        '''
        @returns Forwards touple (matchRate, popRate) returned by Quality, if hardSilceLevel and hardGroupsNo
        '''
        
        
        logger.info("Will generate graph with params")
        logger.info(kwargs)
        logger.info("Will do %d runs" % runsNo )
        

        
        sliceLevel = kwargs['slice_level']
        logger.info("Slice is level: %d" % sliceLevel)
        del kwargs['slice_level']
        
        matchRate = 0.0
        popRate = 0.0
        suspectsRate = 0.0
        
        
        near100Rate = 0.0 
  
        for run in xrange(runsNo):
            self.dm.generate(**kwargs)
            self.graph = self.gm.makeGraph()
            self.rings = sum(self.dm.voting_rings, []) # H-H-HHACKISH list flattening

            logger.debug("Voting rings are")
            logger.debug(self.rings)
            
            self.cq = sna.Cliquer(self.graph)
            self.cq.sliceGraph(sliceLevel)
            self.result = self.cq.blondelAlgorithm()
            
            tuple = self.rateQuality(hardGroupsNo)
            
            matchRate += tuple[0]
            popRate += tuple[1]
            suspectsRate += tuple[2] 
             
            # fourth quality marker 
            if tuple[0] > 0.9:
                near100Rate += 1
            logger.debug(near100Rate)
            
        logger.info("Done run %d of %d" % (run, runsNo))     
        logger.debug(near100Rate)       
        logger.debug(float(near100Rate / float(runsNo))*100.0)
        
        # we have to aggregate tuple for runsNo
        tuple = (float(matchRate / float(runsNo)), float(popRate / float(runsNo)), float(suspectsRate / float(runsNo)), float(near100Rate / float(runsNo))*100.0)
        logger.info("After % d runs result is" % runsNo)
        logger.info(tuple)
        logger.info(" ------------------- END --------------------")
    
        return tuple
    
    def rateQuality(self, hardGroupsNo = 0):
        '''
        @returns touple of matchRate and popRate if hardGroupsNo, for sake of plotting or smth
        '''
        if hardGroupsNo:
            self.selectGroups = [hardGroupsNo]
        for i in self.selectGroups: # select first i groups
            matchCount = 0
            # suspects = self.cq.smartGetFristNGroups(self.result, i)
            suspects = self.cq.getSuspectedGroups(self.result, i)
            
            logger.debug("Suspects: ")
            logger.debug(suspects)
            
            for v in self.rings:
                if int(v) in suspects:
                    matchCount += 1
            
            matchRate = matchCount/len(self.rings) * 100.0
            popRate = len(suspects)/len(self.graph) * 100.0
            suspectsRate = matchCount/len(suspects) * 100.0
            
            logger.info("Taking first %d groups match rate is %f. These groups are %f  of users population." % (i, matchRate, popRate))
        
        return (matchRate, popRate, suspectsRate)
            
            
    
    def iterateParam(self, minValue = 10, maxValue = 25, step = 5, param = "target_size", hardGroupsNo = 0, **kwargs):
        '''
        @return Hard version returns tuple of two list, so that you can make some pretty plots =D
        '''
        
        kwargs[param] = minValue
        
        matchRates = []
        popRates = []
        suspectRates = []
        near100Rates = []
        xaxis = []
        
        
        while kwargs[param] <= maxValue:
            logger.info("Will iterate over %s : now it's %d:" % (param, kwargs[param]))
            tuple = self.compute(hardGroupsNo = hardGroupsNo, **kwargs)
            xaxis.append(kwargs[param]) 
            kwargs[param] += step
            
            if hardGroupsNo:
                matchRates.append(tuple[0])
                popRates.append(tuple[1])
                suspectRates.append(tuple[2])
                near100Rates.append(tuple[3])
            
            
        if hardGroupsNo:
            return ((matchRates, popRates, suspectRates, near100Rates), xaxis)
        
    def plotTuple(self, tuple, caption = "This is experiment", xlabel = "This is x label", ylabel = "This is y label", file_title = "chart", xaxis = [], step = 1):
        
        if not xaxis:
            from numpy import arange
            xaxis = arange(0,len(tuple[0]),1)

        logger.info("############# Plotting tuples ################")
        logger.info(tuple)
        
        import Gnuplot
        g = Gnuplot.Gnuplot()
        suspects = Gnuplot.Data(xaxis, tuple[0], title ='procent wykrytych zlosliwych glosujacych', with_="points lt 1 lw 6 lc 1")
        population = Gnuplot.Data(xaxis, tuple[1], title='podejrzany procent populacji', with_="points lt 4 lw 6 lc 3")
        suspectsR = Gnuplot.Data(xaxis, tuple[2], title='procent zlosliwych glosujacych wsrod podejrzanych', with_="points lt 2 lw 6 lc 4")
        near100 = Gnuplot.Data(xaxis, tuple[3], title='procent wykryc powyzej 90%', with_="points lt 3 lw 6 lc 5")
        
        
        g.title(caption)
        g.xlabel(xlabel)
        g.ylabel(ylabel)
        g('set xtics ' + repr(step))
        g('set grid')
        g('set size 1.3,1.3')
        
        maxs = []
        maxs.append(max(tuple[0]))
        maxs.append(max(tuple[1]))
        maxs.append(max(tuple[2]))
        maxs.append(max(tuple[3]))
        max_y = max(maxs)
        
        g('set yrange [ 0 : ' + repr(max_y+10) + ' ]')
        g.plot(suspects, population, suspectsR, near100)
        #g.plot(suspects, population, suspectsR)
        g.hardcopy(file_title + '.ps', enhanced=1, color=1)
        
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
    dm.generate(number = 1, size = 25, target_size = 10, legible_target_size = 10, VOTERS=5000, OBJECTS=1000, bad_hideout=True)
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


        
        
        
    
    