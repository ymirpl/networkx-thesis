from simplejson import *
from urllib2 import *
from xml.dom import minidom
from xml import dom
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
        friends = loads(urlopen('https://graph.facebook.com/me/friends?access_token='+TOKEN).read())
    
        for friend in friends['data']:
            self.graph.add_node(int(friend['id']), {'name': friend['name']})
            self.graph.add_edge(self.myId, int(friend['id']))
            
            
            foaf  = minidom.parse(urlopen('https://api.facebook.com/method/friends.getMutualFriends?target_uid='+friend['id']+'&source_uid=1244349170&access_token='+TOKEN))
            for f in foaf.getElementsByTagName("uid"):
                self.graph.add_edge(int(f.firstChild.nodeValue), int(friend['id']))
                
        self.saveGraph()
                
    def saveGraph(self, filename = 'fb.gpickle'):
        nx.write_gpickle(self.graph, filename)
        
    def loadGraph(self, filename = 'fb.gpickle'):
        self.graph = nx.read_gpickle(filename)
    
    def draw(self):
        import matplotlib.pyplot as plt
        nx.draw(self.graph)
        plt.show()
            

if __name__ == "__main__":
    fb = Facebooker()
    fb.loadGraph()
    fb.draw()

        
        
    