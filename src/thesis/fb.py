# encoding: utf-8
"""
@author: Marcin Mincer, IAiIS
"""

from thesis import logger
from thesis.sna import timeit
import networkx as nx

FB_API_KEY = "ca00488bed6f966941788ddca65823ca"
FB_SECRET =  "0d950a306c96374ec2b09d113190cb09"
FB_APP_ID = "152284658119481"
FB_CODE = "917aefd01a1c2bac3e1d478f-1244349170|NSedJegWuBgi7ZcFk77WmWQgL8g"
TOKEN = "152284658119481|917aefd01a1c2bac3e1d478f-1244349170|oejQMHFngbBNJCdGUXFfmkE9ZJo"

# podział wykonany przeze mnie
handPartition = [[100000648559579, 100000568166299, 1083970911, 100001151564860, 100000650966699], # awf 
                 [100000865749997, 100000028449750, 100001045601749, 100000243669458, 100000081887173, 1162622890, 1547725220, 100000416738692, 766967667, 100000548456815, 1054225249, 1796057946, 0, 1812844057, 100000796855344, 100000251476023, 670774349, 100000195247193, 574613122, 100000177233035, 100000950045344, 100001401545390, 1563941552, 100000072241347, 100000665913030, 1579834588, 100000115366354, 100000875089655, 1605019392, 100000072977670, 1682210082, 1255764264, 100000223015724, 1130027485], # studia
                 [1456110848, 682314702, 906415022, 100000675199851, 1361434456, 100000511275520, 1500674056, 1341281293, 100000559244304, 1283026463, 1251644963, 1423307828, 100000978972259, 100000359074423, 1145690747, 543900798, 1458353825, 100000500574893, 1218227920, 730325234, 652673267, 100000786148478, 100000844134666, 1374489875, 1438635288, 1334643932, 1674574646], # gim
                 [1177760162, 100000077028249, 100000395817861, 1476711297, 1032966662, 100001240417302, 100000555727570, 100000822290649, 1298798324, 100000159406372, 1779769892], # podstawowka
                 [1436550136, 100001392610551, 100000575211956, 1198502305, 100000943723935, 1040476565, 100000717948818, 100000036955024, 1069035901, 100000050158456, 100000522020215, 1621747250, 1535572062, 100000577456753, 100000761276531, 100000626047119, 100000204317377, 711597283, 100001159501558, 1541512459, 704756495, 1341833543, 100000070382409, 100000586940753], # inni 
                 [100000570911217, 100000241461744, 100000774974437, 1589262813, 1545300898, 100000316434882, 1223122879, 1685006257, 1393333145, 1810313588, 806459762, 100000534391132, 100000916441102, 1196611093, 100000242988059, 1663011364, 1475919878, 1527991374, 100000269880914, 1561663125, 100000237510295, 100000106189989, 1427656367, 1555223217, 1665207509, 1142665486, 100000092777302], # liceum
                 ] 

class Facebooker:
    """
    Klasa z metodami służącymi do eksperymentów na danych pobranych z platformy Facebook
    """
    
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
            
    def graphMeasure(self, measure = 'degree', anonymized_log = False):
        measureValues = self.centrality[measure]
        
        
        filename = measure + ".png"
        
        # print sorted node list on INFO
        nodesDict = dict()
        for node, data in self.graph.nodes_iter(data=True):
            nodesDict[node] = measureValues[node]
        sortedNodes = sorted(nodesDict, key=nodesDict.get, reverse = True)
        
        logger.info("******########*******" + measure + "******########*******")
        for node in sortedNodes:
            if not anonymized_log:
                logger.info(self.graph.node[node]['name'] +" (" + str(self.labels[node]) + "): " + str(nodesDict[node])) # z nazwiskami osob
            else:
                logger.info(str(self.labels[node]) + ": " + str(nodesDict[node])) # same numery
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
        
        # write down partition
        
        for cluster in self.partition:
            members = ""
            for member in cluster:
                members += str(self.labels[member]) + " "
            logger.info(str(self.partition.index(cluster)) + ", " + members)
        
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
        
    
    def ratePartition(self):
        """ Metoda do oceny podziału sieci. Porównuje podział wykonany z wzrocowym i wyznacza procentową skuteczność podziału. 
        """
        result = 0
        maximal_result = 0
        
        
        for index, node in enumerate(self.graph.nodes()):
            for groupNo in self.partition:
                if node in groupNo:
                    nodeComputedGroup = self.partition.index(groupNo)
            for groupNo in handPartition:
                if node in groupNo:
                    nodeOriginalGroup = handPartition.index(groupNo)
                    
            for secondNode in self.graph.nodes()[index+1:]:
                for groupNo in self.partition:
                    if secondNode in groupNo:
                        secondNodeComputedGroup = self.partition.index(groupNo)
                for groupNo in handPartition:
                    if secondNode in groupNo:
                        secondNodeOriginalGroup = handPartition.index(groupNo)
                
                if nodeOriginalGroup == secondNodeOriginalGroup:
                    maximal_result += 1
                if (nodeOriginalGroup == secondNodeOriginalGroup) and (nodeComputedGroup == secondNodeComputedGroup):
                    result += 1

        ret = float(result)/maximal_result * 100.0
        logger.info("# Jakość grupowania FB: " + str(ret) + "%")  
        return ret
        
if __name__ == "__main__":
    fb = Facebooker()
    fb.loadGraph()
    fb.partitionGraph()
    #fb.loadMeasures()
    
