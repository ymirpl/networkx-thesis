# encoding: utf-8

from thesis import logger
from thesis.sna import timeit
import networkx as nx

FB_API_KEY = "ca00488bed6f966941788ddca65823ca"
FB_SECRET =  "0d950a306c96374ec2b09d113190cb09"
FB_APP_ID = "152284658119481"
FB_CODE = "917aefd01a1c2bac3e1d478f-1244349170|NSedJegWuBgi7ZcFk77WmWQgL8g"
TOKEN = "152284658119481|917aefd01a1c2bac3e1d478f-1244349170|oejQMHFngbBNJCdGUXFfmkE9ZJo"


class Facebooker:
    
    graph = nx.Graph()
    myId = 0
    labels = dict()
    
    def __init__(self):
        self.graph.add_node(self.myId, {'name': 'Marcin Mincer'})
    
    def fetchGraph(self):
        from simplejson import loads
        from urllib2 import urlopen
        from xml.dom import minidom
        
        friends = loads(urlopen('https://graph.facebook.com/me/friends?access_token='+TOKEN).read())
    
        for friend in friends['data']:
            self.graph.add_node(int(friend['id']), name=friend['name'])
            self.graph.add_edge(self.myId, int(friend['id']))
            
            
            foaf  = minidom.parse(urlopen('https://api.facebook.com/method/friends.getMutualFriends?target_uid='+friend['id']+'&source_uid=1244349170&access_token='+TOKEN))
            for f in foaf.getElementsByTagName("uid"):
                self.graph.add_edge(int(f.firstChild.nodeValue), int(friend['id']))
                
        self.saveGraph()
                
    def saveGraph(self, filename = 'fb.gpickle'):
        nx.write_gpickle(self.graph, filename)
        
    def loadGraph(self, filename = 'fb.gpickle'):
        self.graph = nx.read_gpickle(filename)
        # make normal label numbers
        i = 1
        for node in self.graph:
            self.labels[node] = i
            i += 1 
        logger.debug("Graph loaded, edges: %d, nodes: %d" % (self.graph.number_of_edges(), self.graph.number_of_nodes()))
    
    def draw(self, filename = "fb.png"):
#        from pygraphviz import *
        import matplotlib.pyplot as plt
        nx.draw(self.graph)
        plt.savefig(filename)
    
    @timeit        
    def computeMeasures(self, filename = "measures.pickle"):
        self.centrality = {}
        
        self.centrality['betweeness'] = nx.betweenness_centrality(self.graph)
        self.centrality['degree']  = nx.degree_centrality(self.graph)
        self.centrality['closeness']= nx.closeness_centrality(self.graph)
        self.centrality['eigenvector']  = nx.eigenvector_centrality(self.graph)
        self.centrality['clustering']  = nx.clustering(self.graph)
        self.centrality['avg_clustering'] = nx.average_clustering(self.graph)
        self.centrality['avg_shortest_path'] = nx.average_shortest_path_length(self.graph)
        
        import pickle
        with open(filename, 'wb') as file:
            pickle.dump(self.centrality, file)
        
    def loadMeasures(self, filename =  "measures.pickle"):
        import pickle
        with open(filename, 'rb') as file:
            self.centrality = pickle.load(file)
            
    def graphMeasure(self, measure = 'degree'):
        measureValues = self.centrality[measure]
        
       
        
        filename = measure + ".png"
        
        # print sorted node list on INFO
        nodesDict = dict()
        for node, data in self.graph.nodes_iter(data=True):
            nodesDict[node] = measureValues[node]
        sortedNodes = sorted(nodesDict, key=nodesDict.get, reverse = True)
        
        logger.info(measure)
        for node in sortedNodes:
            logger.info(self.graph.node[node]['name'] +" (" + str(self.labels[node]) + "): " + str(nodesDict[node]))
            # set my value to 0 for better colors
            if self.graph.node[node]['name'] == 'Marcin Mincer':
                measureValues[node] = 0
        
        

        # stupid hack becouse of pygraphviz utf-8 malfunction
        graph_copy = nx.Graph();
        graph_copy.add_nodes_from(self.graph.nodes())
        graph_copy.add_edges_from(self.graph.edges())
        # end stupid hack
        
        pos=nx.pygraphviz_layout(graph_copy,prog='neato')
        for i in pos:
            pos[i] = (pos[i][0]*3, pos[i][1]*3)
        
        import matplotlib.pyplot as plt
        

        
        plt.figure(figsize=(20,20))
        plt.axis('off')
        nx.draw_networkx_edges(self.graph,pos,alpha=0.2)
        nx.draw_networkx_nodes(self.graph, pos, size = 4, with_labels=False, node_color=measureValues.values(), cmap=plt.cm.get_cmap('Spectral'))
        nx.draw_networkx_labels(self.graph, pos, font_size = 10, labels = self.labels)
        plt.colorbar(orientation="horizontal", fraction = 0.04, pad = 0.01, aspect = 16)
        plt.savefig(filename)
        
            
    def partitionGraph(self, filename = "fb_partition.png", method = 'blondelAlgorithm'):
        from thesis.sna import Cliquer
        
        cq = Cliquer(self.graph)
        function = getattr(cq, method)
        self.partition = function()
        
        # partition done, making colors
        # making graph
        
        nodeList = self.partition
        colorList = [0] * self.graph.number_of_nodes()

        for nbunch in nodeList:
            for n in nbunch:
                colorList[self.graph.nodes().index(n)] = nodeList.index(nbunch)

        import matplotlib.pyplot as plt
        
        # stupid hack becouse of pygraphviz utf-8 malfunction
        graph_copy = nx.Graph();
        graph_copy.add_nodes_from(self.graph.nodes())
        graph_copy.add_edges_from(self.graph.edges())
        # end stupid hack
        
        
        pos=nx.pygraphviz_layout(graph_copy,prog='neato')
        for i in pos:
            pos[i] = (pos[i][0]*3, pos[i][1]*3)
        
        
        plt.figure(figsize=(20,20))
        plt.axis('off')
        nx.draw_networkx_edges(self.graph,pos,alpha=0.2)
        nx.draw_networkx_nodes(self.graph, pos, size = 4, node_color=colorList, with_labels=False)
        nx.draw_networkx_labels(self.graph, pos, font_size = 10, labels = self.labels)
        
        plt.savefig(filename)
        
        
                    

if __name__ == "__main__":
    fb = Facebooker()
#    fb.fetchGraph()
#    fb.saveGraph()
    fb.loadGraph()
    fb.partitionGraph()
    fb.loadMeasures()
    
