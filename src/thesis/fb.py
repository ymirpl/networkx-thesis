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
        
        import pickle
        with open(filename, 'wb') as file:
            pickle.dump(self.centrality, file)
        
    def loadMeasures(self, filename =  "measures.pickle"):
        import pickle
        with open(filename, 'rb') as file:
            self.centrality = pickle.load(file)
        
                    

if __name__ == "__main__":
    fb = Facebooker()
    fb.fetchGraph()
    fb.saveGraph()
    
