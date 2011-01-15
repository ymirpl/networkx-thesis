'''
Created on 03-08-2010

@author: ymir
'''
from __future__ import division
import networkx as nx
from thesis import logger

# timeit decorator
import time                                                
def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        logger.debug('%r (%r, %r) %.3f sec' %  (method.__name__, args, kw, te-ts))
        return result

    return timed
# end timeit decorator


class FileType:
    unknown = 0
    VOTING_RING = 1
    
class DataMaker:
    '''
    Provides methods for generating data containing voting rings
    '''
    path = ''
    def __init__(self, path):
        self.path = path
        
        
    def generate(self, number = 1, size = 5, target_size = 5, legal_target_size = 10,VOTERS=1000, OBJECTS=200, bad_hideout=False, slice_level = 0):
        '''
        @param number: no of voting rings
        @param size: size of voting rings
        @param target_size: size of voting ring target set
        ''' 
        # TODO Sometimes generated data crashes partitioner, don't know why ;(
        
        additional_votes = legal_target_size - target_size
        if additional_votes < 0:
            additional_votes = 0
        
        objects = [[] for i in xrange(OBJECTS)] # every object has a list of his voters
        
        import random
        self.voting_rings = [[] for i in xrange(number)]
        for i in xrange(number):
            for j in xrange(size):
                voter = str(random.randint(0, VOTERS))
                while voter in self.voting_rings[i]:
                    voter = str(random.randint(0, VOTERS))
                self.voting_rings[i].append(voter)
                   
        
        # voting ringers vote for their objects
        for i in xrange(number):
            for j in xrange(target_size):
                target = random.randint(0, OBJECTS-1)
                objects[target].extend(self.voting_rings[i])
              
              
        nonVotingCntr = 0       
        for voter in xrange(VOTERS):
            
            done_voting = False
            
            for ring in self.voting_rings:
                if str(voter) in ring:
                    done_voting = True
                    break

            if done_voting:
                if bad_hideout:
                    nonVotingCntr += 1
                    continue
                else:
                    votes = int(random.gauss(additional_votes, additional_votes/4.0))
            else:
                votes = int(random.gauss(legal_target_size, legal_target_size/4.0))
                    
            for i in xrange(votes):
                target = random.randint(0, OBJECTS-1)
                if not str(voter) in objects[target]:
                    objects[target].append(str(voter))
        
        
        logger.debug("Non voting cntr is %d" % nonVotingCntr)
        logger.debug("Voting rings are:")
        logger.debug(self.voting_rings)
        
        file = open(self.path, 'w')
        o_number = 1
        for o in objects:
            file.write(str(o_number) + "\n")
            file.write(" ".join(o))
            file.write("\n")
            o_number += 1
        file.close()
                

        
        
class GraphMaker:
    '''
    Provides methods for reading/writing files
    '''
    
    path = ""
    file_type = FileType.unknown
    graph = nx.Graph()
    
    def __init__(self, path = None, file_type = FileType.VOTING_RING):
        if path:
            self.path = path
        self.file_type = file_type
    
    
    def makeGraph(self):
        if self.file_type == FileType.VOTING_RING:
            i = 0
            voters = []
            with open(self.path) as file:
                for line in file:
                    if not i % 2 == 0: # voters line
                        voters = [int(v) for v in line.split()]
                        # voting for same item increases edge weight between all of voters by 1
                        self.graph.add_nodes_from(voters)
                        self.addEdges(voters)
                    
                    i += 1
            
            logger.info("Graph loaded, nodes: "  + repr(self.graph.number_of_nodes()) + ", edges: " + repr(self.graph.number_of_edges()))
            return self.graph
    
    def addEdges(self, voters):
        edges = []
        for v in voters:
            for rb in voters[voters.index(v) + 1:]:
                edges.append((v, rb))
        
        self.graph.add_edges_from(edges)
        for edge in edges:
            try:
                self.graph[edge[0]][edge[1]]['weight'] += 1
            except KeyError:
                self.graph[edge[0]][edge[1]]['weight'] = 1
                
                       

class Cliquer(object):
    '''
    classdocs
    '''
    graph = nx.Graph()
    minWeight = 0
    maxWeight = 0
    weight_dist = {}


    def __init__(self, graph):
        self.graph = graph

    def calculateMinMax(self):
        # calulate min/max w
        
        minEdge = min(self.graph.edges(data=True), key=lambda node: node[2]['weight'])
        self.minWeight = self.graph.get_edge_data(*minEdge[:2])['weight']
        maxEdge = max(self.graph.edges(data=True), key=lambda node: node[2]['weight'])
        self.maxWeight = self.graph.get_edge_data(*maxEdge[:2])['weight']
        
        logger.debug("Weight: max " + repr(self.maxWeight) + " and min " + repr(self.minWeight))

    
    def sliceGraph(self, threshold):

        def filter(edge):
            if edge[2]['weight'] < threshold:
                self.graph.remove_edge(*edge[:2])
                
        map(filter, self.graph.edges(data=True))
        
        # remove disconnected nodes
        def filterNodes(node):
            if self.graph.degree(node) == 0:
                self.graph.remove_node(node)
                
        map(filterNodes, self.graph.nodes())
        
        # we have to change weights to 1/weight, so that stronger connected nodes appears to be closer for cclustering algorithms
        def invertWeight(edge):
            try:
                edge[2]['weight'] = int(100/edge[2]['weight'])
            except:
                edge[2]['weight'] = float('Inf')
                logger.error("Exception in weight inverting, infinity set")
        
        def nullifyWeight(edge):
            edge[2]['weight'] = 1
        
        map(invertWeight, self.graph.edges(data=True))
#        map(nullifyWeight, self.graph.edges(data=True))
        
        logger.debug("Data sliced with threshold " + repr(threshold) + ", edges " + repr(self.graph.number_of_edges()) + ", nodes " + repr(self.graph.number_of_nodes()))
  
    
    def nativeCliquer(self):
        '''
        honestly -- useless
        '''
        cliques = list(nx.find_cliques(self.graph))
        logger.info("Cliques found:")
        import pprint
        pprint.pprint(cliques)
 
    def prettyPlotter(self, l=None, filename=None):
        nodeList = l
            
        colorList = [0] * self.graph.number_of_nodes()
        for nbunch in nodeList:
            for n in nbunch:
                colorList[self.graph.nodes().index(n)] = nodeList.index(nbunch)
        import matplotlib.pyplot as plt
        pos = nx.graphviz_layout(self.graph, prog='neato')
        nx.draw(self.graph, pos, node_color=colorList, with_labels=False)
        if filename:
            plt.savefig(filename)
        else:
            plt.show()
            
    def getSuspectedGroups(self, lists, noGroups=2):
        lists.sort(key=len)
        retList = []

        for i in xrange(min(noGroups, len(lists))):
            retList.extend(lists[i])
        
        return retList
        
    
    def smartGetFristNGroups(self, lists, noGroups=2):
        lists.sort(key=len)
        # return as one big lists
        retList = []
        for i in xrange(min(noGroups, len(lists))):
            retList.extend(lists[i])
        
        while len(retList)/len(self.graph) < 0.1:
            # if this still lower then 10% of population, get more groups
            i += 1
            try:
                retList.extend(lists[i])
            except:
                logger.debug("This was last group! Population is now %f ." % (len(retList)/len(self.graph)))
                
        return retList
    
    @timeit
    def blondelAlgorithm(self, verbose=False):
        from lib import blondel
        
        d = blondel.best_partition(self.graph)
        # returns dict of nodes with cluster number values
        logger.debug("Blondel partition done")

        # change it to list of lists
        
        clusters = max(d.values())
        nodeList = [None]*(clusters+1)

        for k in d.keys():
            if not nx.utils.is_list_of_ints(nodeList[d[k]]):
                nodeList[d[k]] = []
            nodeList[d[k]].append(k)
        
        if verbose:
            self.getSuspectedGroups(nodeList, verbose['groups'])    
        
        return nodeList
    
    @timeit
    def newmanAlgorithm(self, verbose=False):
        from lib import newman
        (Q, partition) = newman.detect_communities(self.graph)
        # returns list o lists (each list for community) as a second tuple member
        logger.info("Newman partition done")
        
        if verbose:
            logger.info("Q: %f" % Q)  
            self.getSuspectedGroups(partition, verbose['groups'])    
        
        return partition 
    
    @timeit
    def causetNewmanAlgorithm(self, verbose=False):
        from lib import causet_newman
        
        (maxQ, partition, tree, treeRoot) = causet_newman.communityStructureNewman(self.graph)
        # returns list o lists (each list for community) as a second tuple member
        logger.info("Causet-Newman partition done")
        
        if verbose:
            self.getSuspectedGroups(partition, verbose['groups'])    
        
        return partition    
    
    @timeit
    def MCLAlgorithm(self, inflation=3.3, verbose=False):
        '''
        requires installed mcl in system bin path
        '''
        
        try:
            nx.write_weighted_edgelist(self.graph, "/tmp/mcl-input", delimiter="\t")
        except:
            nx.write_edgelist(self.graph, "/tmp/mcl-input", delimiter="\t")
        import os
        logger.info("Invoking mcl command ...")
        os.system("mcl /tmp/mcl-input --abc -te 2 -I %f -o /tmp/mcl-output" % inflation)
        logger.info("MCL clustering done")
        
        out_file = open("/tmp/mcl-output", 'r')
        lines = out_file.readlines()
        
        partition = list()
        
        import string
        for line in lines:
            partition.append(map(int, string.split(line)))
        
        if verbose:
           self.getSuspectedGroups(partition, verbose['groups'])   

        return partition
        
        
        
        

        
