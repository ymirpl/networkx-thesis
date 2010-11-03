import networkx as nx

FB_API_KEY = "ca00488bed6f966941788ddca65823ca"
FB_SECRET =  "0d950a306c96374ec2b09d113190cb09"
FB_APP_ID = "152284658119481"
FB_CODE = "917aefd01a1c2bac3e1d478f-1244349170|NSedJegWuBgi7ZcFk77WmWQgL8g"
TOKEN = "152284658119481|917aefd01a1c2bac3e1d478f-1244349170|oejQMHFngbBNJCdGUXFfmkE9ZJo"


class Facebooker:
    
    graph = nx.Graph()
    myId = '0'
    
    def __init__(self):
        self.graph.add_node(self.myId, {'name': 'Marcin Mincer'})
    
    def fetchGraph(self):
        from simplejson import loads
        from urllib2 import urlopen
        from xml.dom import minidom
        
        friends = loads(urlopen('https://graph.facebook.com/me/friends?access_token='+TOKEN).read())
    
        for friend in friends['data']:
            self.graph.add_node(friend['id'], {'name': friend['name']})
            self.graph.add_edge(self.myId, friend['id'])
            
            
            foaf  = minidom.parse(urlopen('https://api.facebook.com/method/friends.getMutualFriends?target_uid='+friend['id']+'&source_uid=1244349170&access_token='+TOKEN))
            for f in foaf.getElementsByTagName("uid"):
                self.graph.add_edge(f.firstChild.nodeValue, friend['id'])
                
        self.saveGraph()
                
    def saveGraph(self, filename = 'fb.gpickle'):
        nx.write_gpickle(self.graph, filename)
        
    def loadGraph(self, filename = 'fb.gpickle'):
        self.graph = nx.read_gpickle(filename)
        
        # ok, redo this shitty graph
        
        
    
    def draw(self):
#        from pygraphviz import *
#        A = nx.to_agraph(self.graph)
#        A.draw('star.png',prog="circo")
#        import matplotlib.pyplot as plt
#        nx.draw(self.graph)
#        plt.show()
        dict = nx.closeness_vitality(self.graph, False, True)
        print dict
            

if __name__ == "__main__":
    fb = Facebooker()
#    fb.fetchGraph()
#    fb.saveGraph()
    fb.loadGraph()
    fb.draw()

        
        
    
