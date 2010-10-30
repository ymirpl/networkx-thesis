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
    tuple = e.iterateParam(minValue = 1, maxValue = 4, param="slice_level", hardGroupsNo=1, step = 1, number = 1, size = 25, \
                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=False, runsNo = 1)
    
#    tuple = e.compute(hardGroupsNo=1,  number = 1, size = 25, \
#                   legible_target_size = 10, VOTERS=500, OBJECTS=100, bad_hideout=True, sliceLevel = 1, runsNo = 10)
    
    e.plotTuple(tuple, caption = "Wynik w zaleznosci poziomu odciecia", xlabel = "Poziom odciecia", ylabel = "", file_title = "hgn11")
    
