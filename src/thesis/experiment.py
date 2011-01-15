# -*- encoding: utf-8 -*-

'''
Stworzono: 03-10-2010
@author: Marcin Mincer, IAiIS
'''

from __future__ import division
import networkx as nx
from thesis import sna
from thesis import logger
from lib import  karate_graph

class Experiment:
    """
    Klasa zwierająca metody wykonujące eksperymenty mające na celu ocenę skuteczności autorskiej metody wykrywania klik złośliwie głosujących. 
    """
    
    graph = nx.Graph()
    rings = []
    result = []
    population = 0
    selectGroups = [2,3,4]    
    sliceLevels = [1,2,3,4]
    vertexNo = 0
    paramsDict = {'size': 10, 'number': 1, 'legal_target_size': 10, \
                  'target_size': 10, 'VOTERS': 500, 'OBJECTS': 100, 'bad_hideout': False, 'slice_level': 3}
    
    
    
    def __init__(self, testingDataPath = "/tmp/testing-ring.txt"):
        """
        Konstruktor
        @param testingDataPath: ścieżka do pliku z testowymi danymi o głosowaniu
        @type testingDataPath: text
        """
        
        self.testingDataPath = testingDataPath
        self.dm = sna.DataMaker(self.testingDataPath)
        self.gm = sna.GraphMaker(self.testingDataPath)
        
 
    def compute(self, hardGroupsNo = 0, runsNo = 1):
        '''
        Metoda wykonuje określoną w L{runsNo} liczbę uruchomień algorytmu, zwaraca średnią arytmetyczną wskaźników jakości. 

        @type hardGroupsNo: number
        @param hardGroupsNo: liczba grup (począwszy od najmniej licznej), których członkowie są uważania za podjerzanych
        @rtype: tuple
        @return: Zwraca krotkę (matchRate, popRate, suspectsRate, near100rate), która zwiera średnią arytmetyczną z wartości wyznaczonych przez metodę L{rateQuality}.  
        '''
        
        
        logger.info("# Parametry generatora")
        logger.info("# " + str(self.paramsDict))
        logger.info("# Liczba prób: %d" % runsNo )
        

        
        logger.info("# Poziom odcięcia: %d" % self.paramsDict['slice_level'])
        matchRate = 0.0
        matchRateList = []
        popRate = 0.0
        suspectsRate = 0.0
        
        
        near100Rate = 0.0 
  
        for run in xrange(runsNo):
            self.dm.generate(**self.paramsDict)
            self.graph = self.gm.makeGraph()
            self.rings = sum(self.dm.voting_rings, []) # H-H-HHACKISH spłaszczenie listy list
            self.vertexNo = len(self.graph)

            self.cq = sna.Cliquer(self.graph)
            self.cq.sliceGraph(self.paramsDict['slice_level'])
            self.result = self.cq.blondelAlgorithm()
            
            tuple = self.rateQuality(hardGroupsNo)
            
            matchRate += tuple[0]
            matchRateList.append(tuple[0])
            popRate += tuple[1]
            suspectsRate += tuple[2] 
             
            # czwarty wskaźnik jakości
            if tuple[0] > 90:
                near100Rate += 1
            logger.debug(near100Rate)

        matchRateAvg = float(matchRate/float(runsNo))
        
        # obliczenie wariancji matchRate
        matchRateList = map(lambda rate: (rate - matchRateAvg)**2, matchRateList)
        matchRateVariance = 1.0/runsNo * sum(matchRateList) 
                    
        
        # wyznaczanie średnich arytmetycznych
        tuple = (float(matchRate/float(runsNo)), float(popRate / float(runsNo)), float(suspectsRate / float(runsNo)), float(near100Rate / float(runsNo))*100.0)
        logger.info("# Po  % d uruchomieniach (procent wykrytych; procent populacji podjerzewany; procent faktycznych wśród podejrzewanych; procent podejść, gdzie wykryto powyżej 90%" % runsNo)
        logger.info(tuple)
        logger.info("# Dla parametrów generatora: ")
        logger.info(self.paramsDict)
        logger.info("# Wariancja porcentu wykrytych")
        logger.info(matchRateVariance)
        logger.info("# ------------------- KONIEC --------------------")
    
        return tuple
    
    def rateQuality(self, hardGroupsNo = 0):
        '''
        Wyznacza wskaźniki jakości działania metody autorskiej

        @type hardGroupsNo: number
        @param hardGroupsNo: liczba kolejnych (od najmniej licznej) grup, których członkowie będą uznani za podjerzanych
        
        @rtype: tuple
        @return: Krotka matchRate i popRate
        '''
        if hardGroupsNo:
            self.selectGroups = [hardGroupsNo]
        for i in self.selectGroups: # pobierz pierwszych i grup
            matchCount = 0
            # suspects = self.cq.smartGetFristNGroups(self.result, i)
            suspects = self.cq.getSuspectedGroups(self.result, i)
            
            logger.debug("# Podejrzani: ")
            logger.debug("# " + str(suspects))
            
            for v in self.rings:
                if int(v) in suspects:
                    matchCount += 1
            
            matchRate = matchCount/len(self.rings) * 100.0
            popRate = len(suspects)/self.vertexNo * 100.0
            suspectsRate = matchCount/len(suspects) * 100.0
            
            logger.info("%d, %f, %f" % (i, matchRate, popRate)) # liczba grup, procent wykrytych, procent podejrzewanje populacji
        
        return (matchRate, popRate, suspectsRate)
            
            
    
    def iterateParam(self, minValue = 10, maxValue = 25, step = 5, param = "target_size", hardGroupsNo = 0, runsNo = 100):
        '''
        Służy do przeprowadzania eksperytmentu polegającego na ocenie jakości działania metody przy zmieniającym się jednym parametrze generatora. 
        
        Podawana jest nazwa parametru, wartości minimalna i maksymalna oraz krok, z jakim zmieniania jest wartość. 
        
        @param minValue: wartość startowa parametru
        @param maxValue: wartośc końcowa
        @param step: krok
        @param param: nazwa parametru
        @param hardGroupsNo: liczba grup
        @param runsNo: liczba uruchomień
        
        @rtype: tuple
        @return Krotka zwierające krotkę z wynikami oraz listę argumentów, w celu rysowania wykresów
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
        """
        Metoda rysuje wykres ilustrujący eksperyment
        
        @param tuple: krotka z wynikami
        @param caption: tytuł wykresu
        @param xlabel: tytuł osi poziomej
        @param ylabel: tytuł osi pionowej
        @param file_title: nazwa pliku
        
        @return: W systemie plików pojawia się plik w formacie eps będący zadanym wykresem
        """
        if not xaxis:
            from numpy import arange
            xaxis = arange(0,len(tuple[0]),1)

        logger.info("############# Rysowanie wykresu ################")
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
    
    logger.info("# Karate Graph... ")
    partition = cq.blondelAlgorithm()
    cq.prettyPlotter(l=partition, filename="karate_blondel.png")
    
    partition = cq.newmanAlgorithm()
    cq.prettyPlotter(l=partition, filename="karate_newman.png")
    
    
    partition = cq.causetNewmanAlgorithm()
    cq.prettyPlotter(l=partition, filename="karate_causet_newman.png")
    
    partition = cq.MCLAlgorithm(2.0)
    cq.prettyPlotter(l=partition, filename="karate_MCL.png")
    
    logger.info("# Karate Graph wykonano")
    
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
        
        logger.info("############### EKSPERYMENT THESIXTYONE  ##################")
        logger.info("# O przynależność do kliki jest podejrzanch %d użytkowników, co stanowi  %f\% całej populacji." % (suspects_no, (suspects_no / nodesNo ) * 100.0) )
        logger.info("# Identyfikatory podjerzanych użytkowników: ")
        logger.info(suspects)
        
            

def generated(sliceLevels = [3], plot=False):
    dm = sna.DataMaker("/home/ymir/eclipse/networkx-thesis/testing-ring.txt")
    dm.generate(number = 1, size = 25, target_size = 10, legal_target_size = 10, VOTERS=5000, OBJECTS=1000, bad_hideout=True)
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


        
        
        
    
    