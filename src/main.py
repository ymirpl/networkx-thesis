# coding: utf-8
#!/usr/bin/env python

'''
Created on 02-08-2010

@author: ymir
'''
import networkx as nx
from thesis.experiment import Experiment


if __name__ == '__main__':

#    experiment.karateClub()
#    experiment.sixtyOne()
#    experiment.generated()

    e = Experiment()
 
 
 
    (tuple, xaxis) = e.iterateParam(minValue = 1, maxValue = 4, param="slice_level", hardGroupsNo=1, step = 1, number = 1, size = 25, \
                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=False, runsNo = 1)

    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od poziomu odciecia", xlabel = "Poziom odciecia", ylabel = "", file_title = "slbhf", xaxis = xaxis, step = 1)
    
#    tuple = e.iterateParam(minValue = 1, maxValue = 4, param="slice_level", hardGroupsNo=1, step = 1, number = 1, size = 25, \
#                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=True, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od poziomu odciecia", xlabel = "Poziom odciecia", ylabel = "", file_title = "slbht")
#
#
#    
#    
#    
#    tuple = e.iterateParam(minValue = 10, maxValue = 40, param="size", hardGroupsNo=1, slice_level = 3, step = 5, number = 1, \
#                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=False, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci  od wielkosci kliki", xlabel = "Wielkosc kliki", ylabel = "", file_title = "sizebhf")
#
#    tuple = e.iterateParam(minValue = 10, maxValue = 40, param="size", hardGroupsNo=1, slice_level = 3, step = 5, number = 1, \
#                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=True, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci  od wielkosci kliki", xlabel = "Wielkosc kliki", ylabel = "", file_title = "sizebht")
#
#
#
#
#
#    tuple = e.iterateParam(minValue = 3, maxValue = 12, param="target_size", size = 25, slice_level = 3,  hardGroupsNo=1, step = 3, number = 1, \
#                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=False, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od celu kliki ", xlabel = "Liczba elementow", ylabel = "", file_title = "tsbhf")
#    
#    tuple = e.iterateParam(minValue = 3, maxValue = 12, param="target_size", size = 25, slice_level = 3,  hardGroupsNo=1, step = 3, number = 1, \
#                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=True, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od celu kliki ", xlabel = "Liczba elementow", ylabel = "", file_title = "tsbht")
#    
#    
#    
#    
#    
#    
#    
#    tuple = e.iterateParam(minValue = 20, maxValue = 100, param="OBJECTS", size = 25, slice_level = 3,  hardGroupsNo=1, step = 20, number = 1, \
#                   legible_target_size = 10, VOTERS=500, target_size = 5, bad_hideout=False, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od liczby obiektow ", xlabel = "Liczba obiektow", ylabel = "", file_title = "obbhf")
#    
#    tuple = e.iterateParam(minValue = 20, maxValue = 100, param="OBJECTS", size = 25, slice_level = 3,  hardGroupsNo=1, step = 20, number = 1, \
#                   legible_target_size = 10, VOTERS=500, target_size = 5, bad_hideout=True, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od liczby obiektow ", xlabel = "Liczba obiektow", ylabel = "", file_title = "obbht")
#    
#    
#    
#    
#    
#    
#    
#    tuple = e.iterateParam(minValue = 300, maxValue = 700, param="VOTERS", size = 25, slice_level = 3,  hardGroupsNo=1, step = 100, number = 1, \
#                   legible_target_size = 10, OBJECTS=100, target_size = 5, bad_hideout=False, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od liczby glosujacych ", xlabel = "Liczba glosujacych", ylabel = "", file_title = "vbhf")
#    
#    tuple = e.iterateParam(minValue = 300, maxValue = 700, param="VOTERS", size = 25, slice_level = 3,  hardGroupsNo=1, step = 100, number = 1, \
#                   legible_target_size = 10, OBJECTS=100, target_size = 5, bad_hideout=True, runsNo = 80)
#
#    e.plotTuple(tuple, caption = "Skutecznosc metody w zaleznosci od liczby glosujacych ", xlabel = "Liczba glosujacych", ylabel = "", file_title = "vbht")

