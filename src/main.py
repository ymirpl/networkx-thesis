# coding: utf-8
#!/usr/bin/env python

'''
Created on 02-08-2010

@author: ymir
'''
import networkx as nx
from thesis.experiment import Experiment
from thesis.fb import Facebooker


def testOne():
    e = Experiment()
    e.paramsDict = {'size': 25, 'number': 1, \
                   'legible_target_size': 10, 'target_size': 10, 'VOTERS': 500, 'OBJECTS': 100, 'bad_hideout': False, 'slice_level': 3}
 
    (tuple, xaxis) = e.iterateParam(minValue = 1, maxValue = 4, param="slice_level", step = 1, runsNo = 3, hardGroupsNo = 2)

    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od poziomu odciecia", xlabel = "Poziom odciecia", ylabel = "", file_title = "slbhf", xaxis = xaxis, step = 1)

#    e.paramsDict['bad_hideout'] = True
#    (tuple, xaxis) = e.iterateParam(minValue = 10, maxValue = 40, param="size", hardGroupsNo=2, step = 5, runs = 3)
#
#    e.plotTuple(tuple, xaxis = xaxis, step = 5, caption = "Skutecznosc metody w zaleznosci  od wielkosci kliki", xlabel = "Wielkosc kliki", ylabel = "", file_title = "sizebhf")


def experimentOne():
    e = Experiment()
    e.paramsDict = {'size': 25, 'number': 1, \
                   'legible_target_size': 10, 'target_size': 10, 'VOTERS': 500, 'OBJECTS': 100, 'bad_hideout': False, 'slice_level': 3}
 
    (tuple, xaxis) = e.iterateParam(minValue = 1, maxValue = 4, param="slice_level", step = 1, runsNo = 100)

    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od poziomu odciecia", xlabel = "Poziom odciecia", ylabel = "", file_title = "slbhf", xaxis = xaxis, step = 1)
    
    (tuple, xaxis) = e.iterateParam(minValue = 1, maxValue = 4, param="slice_level", hardGroupsNo=2, step = 1, number = 1, size = 25, \
                   legible_target_size = 10, target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=True, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, caption = "Skutecznosc metody w zaleznosci od poziomu odciecia", xlabel = "Poziom odciecia", ylabel = "", file_title = "slbht")


    (tuple, xaxis) = e.iterateParam(minValue = 10, maxValue = 40, param="size", hardGroupsNo=2, slice_level = 3, step = 5, target_size = 10, number = 1, \
                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=False, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 5, caption = "Skutecznosc metody w zaleznosci  od wielkosci kliki", xlabel = "Wielkosc kliki", ylabel = "", file_title = "sizebhf")

    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="target_size", size = 25, slice_level = 3,  hardGroupsNo=2, step = 3, number = 1, \
                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=False, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 3, caption = "Skutecznosc metody w zaleznosci od celu kliki ", xlabel = "Liczba elementow", ylabel = "", file_title = "tsbhf")
    
    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="target_size", size = 25, slice_level = 3,  hardGroupsNo=2, step = 3, number = 1, \
                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=True, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 3,caption = "Skutecznosc metody w zaleznosci od celu kliki ", xlabel = "Liczba elementow", ylabel = "", file_title = "tsbht")
    
    
    (tuple, xaxis) = e.iterateParam(minValue = 20, maxValue = 100, param="OBJECTS", size = 25, slice_level = 3,  target_size = 10, hardGroupsNo=2, step = 20, number = 1, \
                   legible_target_size = 10, VOTERS=500, bad_hideout=False, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 20, caption = "Skutecznosc metody w zaleznosci od liczby obiektow ", xlabel = "Liczba obiektow", ylabel = "", file_title = "obbhf")
    
    (tuple, xaxis) = e.iterateParam(minValue = 20, maxValue = 100, param="OBJECTS", size = 25, slice_level = 3,  target_size = 10, hardGroupsNo=2, step = 20, number = 1, \
                   legible_target_size = 10, VOTERS=500, bad_hideout=True, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 20, caption = "Skutecznosc metody w zaleznosci od liczby obiektow ", xlabel = "Liczba obiektow", ylabel = "", file_title = "obbht")
    
    
    (tuple, xaxis) = e.iterateParam(minValue = 300, maxValue = 700, param="VOTERS", size = 25, slice_level = 3,  target_size = 10, hardGroupsNo=2, step = 100, number = 1, \
                   legible_target_size = 10, OBJECTS=100, bad_hideout=False, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 100,caption = "Skutecznosc metody w zaleznosci od liczby glosujacych ", xlabel = "Liczba glosujacych", ylabel = "", file_title = "vbhf")
    
    (tuple, xaxis) = e.iterateParam(minValue = 300, maxValue = 700, param="VOTERS", size = 25, slice_level = 3,  target_size = 10, hardGroupsNo=2, step = 100, number = 1, \
                   legible_target_size = 10, OBJECTS=100, bad_hideout=True, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 100,caption = "Skutecznosc metody w zaleznosci od liczby glosujacych ", xlabel = "Liczba glosujacych", ylabel = "", file_title = "vbht")


    (tuple, xaxis) = e.iterateParam(minValue = 3, maxValue = 12, param="legible_target_size ", size = 25, slice_level = 3,  target_size = 10, hardGroupsNo=2, step = 3, number = 1, \
                   VOTERS = 500, OBJECTS=100, bad_hideout=False, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 3,caption = "Skutecznosc metody w zaleznosci od liczby obiektow, na ktore glosuja uczciwi glosujacy ", xlabel = "Liczba obiektow", ylabel = "", file_title = "ltshf")
    
    (tuple, xaxis) = e.iterateParam(minValue = 3,  maxValue = 12, param="legible_target_size ", size = 25, slice_level = 3,  target_size = 10, hardGroupsNo=2, step = 3, number = 1, \
                   VOTERS = 500, OBJECTS=100, bad_hideout=True, runsNo = 100)

    e.plotTuple(tuple, xaxis = xaxis, step = 3,caption = "Skutecznosc metody w zaleznosci od liczby obiektow, na ktore glosuja uczciwi glosujacy ", xlabel = "Liczba obiektow", ylabel = "", file_title = "ltsht")


def testTwo():
    e = Experiment()
    
    (tuple, xaxis) = e.iterateParam(minValue = 10, maxValue = 40, param="size", hardGroupsNo=2, slice_level = 3, target_size = 10, step = 5, number = 1, \
                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=True, runsNo = 10)

    e.plotTuple(tuple, xaxis = xaxis, step = 5, caption = "Skutecznosc metody w zaleznosci  od wielkosci kliki", xlabel = "Wielkosc kliki", ylabel = "", file_title = "sizebht")



if __name__ == '__main__':
#    experimentOne()
    testOne()
    
    from thesis import experiment
#    experiment.karateClub()
#    experiment.sixtyOne()
#    experiment.generated()
#    fb = Facebooker()
#    fb.loadGraph()
#    fb.partitionGraph()





