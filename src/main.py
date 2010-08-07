'''
Created on 02-08-2010

@author: ymir
'''
from thesis import sna

if __name__ == '__main__':
    gm = sna.GraphMaker("/home/ymir/eclipse/networkx-thesis/voting_ring.txt")
    gm.makeGraph()