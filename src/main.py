# coding: utf-8
#!/usr/bin/env python

'''
Created on 02-08-2010

@author: ymir
'''
import networkx as nx
from thesis.experiment import Experiment
from thesis.fb import Facebooker


def experimentOne():
    e = Experiment()
    e.paramsDict = {'size': 25, 'number': 1, \
                   'legible_target_size': 10, 'target_size': 10, 'VOTERS': 500, 'OBJECTS': 100, 'bad_hideout': False, 'slice_level': 3}


    (tuple, xaxis) = e.iterateParam(minValue = 1, maxValue = 4, param="slice_level", step = 1, runsNo = 100, hardGroupsNo = 2)
    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od poziomu odciecia", xlabel = "Poziom odciecia", ylabel = "", file_title = "slbhf", xaxis = xaxis, step = 1)
    
    e.paramsDict['bad_hideout'] = True    
    (tuple, xaxis) = e.iterateParam(minValue = 1, maxValue = 4, param="slice_level", step = 1, runsNo = 100, hardGroupsNo = 2)
    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od poziomu odciecia", xlabel = "Poziom odciecia", ylabel = "", file_title = "slbht", xaxis = xaxis, step = 1)


    e.paramsDict['bad_hideout'] = False    
    (tuple, xaxis) = e.iterateParam(minValue = 10, maxValue = 40, param="size", hardGroupsNo=2, step = 5, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 5, caption = "Skutecznosc metody w zaleznosci  od wielkosci kliki", xlabel = "Wielkosc kliki", ylabel = "", file_title = "sizebhf")

    e.paramsDict['bad_hideout'] = True    
    (tuple, xaxis) = e.iterateParam(minValue = 10, maxValue = 40, param="size", hardGroupsNo=2, step = 5, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 5, caption = "Skutecznosc metody w zaleznosci  od wielkosci kliki", xlabel = "Wielkosc kliki", ylabel = "", file_title = "sizebht")
    
    e.paramsDict['bad_hideout'] = False    
    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="target_size", hardGroupsNo=2, step = 3, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 3, caption = "Skutecznosc metody w zaleznosci od celu kliki ", xlabel = "Liczba elementow", ylabel = "", file_title = "tsbhf")
    
    e.paramsDict['bad_hideout'] = True
    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="target_size", hardGroupsNo=2, step = 3, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 3, caption = "Skutecznosc metody w zaleznosci od celu kliki ", xlabel = "Liczba elementow", ylabel = "", file_title = "tsbht")
    

    e.paramsDict['bad_hideout'] = False   
    (tuple, xaxis) = e.iterateParam(minValue = 20, maxValue = 100, param="OBJECTS", hardGroupsNo=2, step = 20, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 20, caption = "Skutecznosc metody w zaleznosci od liczby obiektow ", xlabel = "Liczba obiektow", ylabel = "", file_title = "obbhf")

    e.paramsDict['bad_hideout'] = True   
    (tuple, xaxis) = e.iterateParam(minValue = 20, maxValue = 100, param="OBJECTS", hardGroupsNo=2, step = 20, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 20, caption = "Skutecznosc metody w zaleznosci od liczby obiektow ", xlabel = "Liczba obiektow", ylabel = "", file_title = "obbht")
    
    
    e.paramsDict['bad_hideout'] = False  
    (tuple, xaxis) = e.iterateParam(minValue = 300, maxValue = 700, param="VOTERS", hardGroupsNo=2, step = 100, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 100,caption = "Skutecznosc metody w zaleznosci od liczby glosujacych ", xlabel = "Liczba glosujacych", ylabel = "", file_title = "vbhf")
    e.paramsDict['bad_hideout'] = True  
    (tuple, xaxis) = e.iterateParam(minValue = 300, maxValue = 700, param="VOTERS", hardGroupsNo=2, step = 100, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 100,caption = "Skutecznosc metody w zaleznosci od liczby glosujacych ", xlabel = "Liczba glosujacych", ylabel = "", file_title = "vbht")
    
    e.paramsDict['bad_hideout'] = False 
    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="legible_target_size ", step = 3, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 3,caption = "Skutecznosc metody w zaleznosci od liczby obiektow, na ktore glosuja uczciwi glosujacy ", xlabel = "Liczba obiektow", ylabel = "", file_title = "ltshf")
    e.paramsDict['bad_hideout'] = True 
    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="legible_target_size ", step = 3, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 3,caption = "Skutecznosc metody w zaleznosci od liczby obiektow, na ktore glosuja uczciwi glosujacy ", xlabel = "Liczba obiektow", ylabel = "", file_title = "ltsht")


def experimentOneCorrection():
    e = Experiment()
    e.paramsDict = {'size': 25, 'number': 1, \
                   'legible_target_size': 10, 'target_size': 10, 'VOTERS': 500, 'OBJECTS': 100, 'bad_hideout': False, 'slice_level': 3}


    e.paramsDict['bad_hideout'] = False 
    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="legible_target_size", step = 3, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 3,caption = "Skutecznosc metody w zaleznosci od liczby obiektow, na ktore glosuja uczciwi glosujacy ", xlabel = "Liczba obiektow", ylabel = "", file_title = "ltshf")
    e.paramsDict['bad_hideout'] = True 
    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="legible_target_size", step = 3, runsNo = 100)
    e.plotTuple(tuple, xaxis = xaxis, step = 3,caption = "Skutecznosc metody w zaleznosci od liczby obiektow, na ktore glosuja uczciwi glosujacy ", xlabel = "Liczba obiektow", ylabel = "", file_title = "ltsht")

    

def testTwo():
    e = Experiment()
    
    (tuple, xaxis) = e.iterateParam(minValue = 10, maxValue = 40, param="size", hardGroupsNo=2, slice_level = 3, target_size = 10, step = 5, number = 1, \
                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=True, runsNo = 10)

    e.plotTuple(tuple, xaxis = xaxis, step = 5, caption = "Skutecznosc metody w zaleznosci  od wielkosci kliki", xlabel = "Wielkosc kliki", ylabel = "", file_title = "sizebht")

def fbExperiment():
    fb = Facebooker()
    fb.loadGraph()
    fb.partitionGraph()
    fb.ratePartition()
#    fb.computeMeasures()
#    fb.loadMeasures()
#    fb.graphMeasure('clustering', True)
#    fb.graphMeasure('betweeness', True)
#    fb.graphMeasure('degree', True)
#    fb.graphMeasure('closeness', True)
#    fb.graphMeasure('eigenvector', True)
#    print fb.centrality['avg_clustering'] 
#    print fb.centrality['avg_shortest_path'] 
        
    


if __name__ == '__main__':
#    fbExperiment()
    experimentOne()
    
    from thesis import experiment
#    experiment.karateClub()
    experiment.sixtyOne()
#    experiment.generated()






