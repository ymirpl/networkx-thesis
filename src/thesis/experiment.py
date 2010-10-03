'''
Created on 03-10-2010

@author: ymir
'''


import networkx as nx
from thesis import sna
from thesis import logger
from lib import  karate_graph



def assertKarate():
    karateG = karate_graph.karate_graph()
    cq = sna.Cliquer(karateG)
    
    logger.info("Karate Graph assert")
    proper_partition = cq.causetNewmanAlgorithm()
    import pprint
    pprint.pprint(proper_partition)
    
    