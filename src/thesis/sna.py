'''
Created on 03-08-2010

@author: ymir
'''
import networkx as nx
from thesis import logger


class FileType:
    unknown = 0
    VOTING_RING = 1

class GraphMaker:
    '''
    Provides methods for reading/writing files
    '''
    
    path = ""
    file_type = FileType.unknown
    graph = nx.Graph()
    
    def __init__(self, path, file_type = FileType.VOTING_RING):
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
        
        logger.info("Weight: max " + repr(self.maxWeight) + " and min " + repr(self.minWeight))

    
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
        
        logger.info("Data sliced with threshold " + repr(threshold) + ", edges " + repr(self.graph.number_of_edges()))
  
    
    def nativeCliquer(self):
        cliques = list(nx.find_cliques(self.graph))
        logger.info("Cliques found:")
        import pprint
        pprint.pprint(cliques)
 
    def prettyPlotter(self, d=None, l=None, filename=None):
        if d:
            clusters = max(d.values())
            nodeList = [None]*clusters
            for k in d.keys():
                if not nx.utils.is_list_of_ints(nodeList[d[k]]):
                    nodeList[d[k]] = []
                nodeList[d[k]].append(k)
        else:
            nodeList = l
            
        colorList = [0] * len(self.graph.nodes())
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

        
        


    
    def blodelAlgorithm(self):
        from lib import blondel
        
        partition = blondel.best_partition(self.graph)
        # returns dict of nodes with cluster number values
        logger.info("Blondel partition done")
        
        import pprint
        pprint.pprint(partition)
        
        return partition

    def newmanAlgorithm(self):
        from lib import newman
        (Q, partition) = newman.detect_communities(self.graph)
        # returns list o lists (each list for community) as a second tuple member
        logger.info("Newman partition done")
        
        print "Q: ", Q  
        import pprint
        pprint.pprint(partition)   
        
        return partition 
    
    def aaronNewmanAlgorithm(self):
        from lib import aaron_newman
        
        (maxQ, partition, tree, treeRoot) = aaron_newman.communityStructureNewman(self.graph)
        # returns list o lists (each list for community) as a second tuple member
        logger.info("Aaron-Newman partition done")
        
        import pprint
        pprint.pprint(partition)
        
        return partition    
