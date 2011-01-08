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
    vertexNo = 0
    paramsDict = {'size': 10, 'number': 1, 'legible_target_size': 10, \
                  'target_size': 10, 'VOTERS': 500, 'OBJECTS': 100, 'bad_hideout': False, 'slice_level': 3}
    
    
    
    def __init__(self, testingDataPath = "/tmp/testing-ring.txt"):
        self.testingDataPath = testingDataPath
        self.dm = sna.DataMaker(self.testingDataPath)
        self.gm = sna.GraphMaker(self.testingDataPath)
        
 
    def compute(self, hardGroupsNo = 0, runsNo = 1):
        '''
        @returns Forwards touple (matchRate, popRate) returned by Quality, if hardSilceLevel and hardGroupsNo
        '''
        
        
        logger.info("Will generate graph with params")
        logger.info(self.paramsDict)
        logger.info("Will do %d runs" % runsNo )
        

        
        logger.info("Slice is level: %d" % self.paramsDict['slice_level'])
        matchRate = 0.0
        matchRateList = []
        popRate = 0.0
        suspectsRate = 0.0
        
        
        near100Rate = 0.0 
  
        for run in xrange(runsNo):
            self.dm.generate(**self.paramsDict)
            self.graph = self.gm.makeGraph()
            self.rings = sum(self.dm.voting_rings, []) # H-H-HHACKISH list flattening
            self.vertexNo = len(self.graph)

            self.cq = sna.Cliquer(self.graph)
            self.cq.sliceGraph(self.paramsDict['slice_level'])
            self.result = self.cq.blondelAlgorithm()
            
            tuple = self.rateQuality(hardGroupsNo)
            
            matchRate += tuple[0]
            matchRateList.append(tuple[0])
            popRate += tuple[1]
            suspectsRate += tuple[2] 
             
            # fourth quality marker 
            if tuple[0] > 90:
                near100Rate += 1
            logger.debug(near100Rate)

        matchRateAvg = float(matchRate/float(runsNo))
        
        # compute variance
        matchRateList = map(lambda rate: (rate - matchRateAvg)**2, matchRateList)
        matchRateVariance = 1.0/runsNo * sum(matchRateList) 
                    
        
        # we have to aggregate tuple for runsNo
        tuple = (float(matchRate/float(runsNo)), float(popRate / float(runsNo)), float(suspectsRate / float(runsNo)), float(near100Rate / float(runsNo))*100.0)
        logger.info("After % d runs result is" % runsNo)
        logger.info(tuple)
        logger.info("For params")
        logger.info(self.paramsDict)
        logger.info("Variance")
        logger.info(matchRateVariance)
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
            popRate = len(suspects)/self.vertexNo * 100.0
            suspectsRate = matchCount/len(suspects) * 100.0
            
            logger.info("Taking first %d groups match rate is %f. These groups are %f  of users population." % (i, matchRate, popRate))
        
        return (matchRate, popRate, suspectsRate)
            
            
    
    def iterateParam(self, minValue = 10, maxValue = 25, step = 5, param = "target_size", hardGroupsNo = 0, runsNo = 100):
        '''
        @return Hard version returns tuple of two list, so that you can make some pretty plots =D
        '''
        
        oldDictValue = self.paramsDict[param]
        self.paramsDict[param] = minValue
        
        matchRates = []
        popRates = []
        suspectRates = []
        near100Rates = []
        xaxis = []
        
        
        while self.paramsDict[param] <= maxValue:
            logger.info("Will iterate over %s : now it's %d:" % (param, self.paramsDict[param]))
            tuple = self.compute(hardGroupsNo = hardGroupsNo, runsNo = runsNo)
            xaxis.append(self.paramsDict[param]) 
            self.paramsDict[param] += step
            
            if hardGroupsNo:
                matchRates.append(tuple[0])
                popRates.append(tuple[1])
                suspectRates.append(tuple[2])
                near100Rates.append(tuple[3])
            
        
        self.paramsDict[param] = oldDictValue
        
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
        near100 = Gnuplot.Data(xaxis, tuple[3], title='procent wykryc powyzej 90%', with_="points lt 3 lw 6 lc 6")
        
        
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
        g.hardcopy(file_title + '.eps', eps=True)
        
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
    
def sixtyOne(sliceLevels = [3]):
    gm = sna.GraphMaker("/home/ymir/eclipse/networkx-thesis/voting_ring.txt")
    gm.makeGraph()
    
    
    for sliceLevel in sliceLevels:
        cq = sna.Cliquer(gm.graph)
        nodesNo = cq.graph.number_of_nodes()
        cq.sliceGraph(sliceLevel)
        
        partition = cq.blondelAlgorithm()
        suspects = cq.smartGetFristNGroups(partition, 2)
        suspects_no = len(suspects)
        
        logger.info("############### THESIXTYONE EXPERIMENT ##################")
        logger.info("There is %d suspects, what is  %f percent of total population." % (suspects_no, (suspects_no / nodesNo ) * 100.0) )
        logger.info("Suspects are: ")
        logger.info(suspects)
        logger.info("End of suspectes.")
        
            

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


        
        
        
    
    