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
    e.iterateParam(minValue = 1, maxValue = 5, param="target_size", hardSliceLevel=2, step = 1, number = 1, size = 25, \
                   legible_target_size = 10, VOTERS=5000, OBJECTS=1000, bad_hideout=True)
    
