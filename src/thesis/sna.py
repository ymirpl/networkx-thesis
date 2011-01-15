# -*- encoding: utf-8 -*-
'''
@created_at: 03-08-2010

@author: Marcin Mincer
'''
from __future__ import division
import networkx as nx
from thesis import logger


import time                                                
def timeit(method):
    """
    Dekorator wypisujący na standardowe wyjście czas działania dekorowanej funkcji w milisekundach
    
    @return: Czas działanie funkcji 
    """

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
    """
    Zawiera metody generujące dane głosowań, w których bierze udział klika złośliwie głosujących.
    """
    
    path = ''
    def __init__(self, path):
        """
        Konstruktor.
        @param path: ścieżka do pliku, w którym będą zapisane wygnerowane dane głosownia
        """
        self.path = path
        
        
    def generate(self, number = 1, size = 5, target_size = 5, legal_target_size = 10,VOTERS=1000, OBJECTS=200, bad_hideout=False, slice_level = 0):
        """
        Metoda generuje dane głosowania (listę obiektów wraz z indetyfikatorami głosujących, którzy oddali głos na dany obiekt) i zapisuje je do pliku
        określonego w self.path.
        
        @param number: liczba klik
        @param size: rozmiar kliki
        @param target_size: liczba obiektów, na które głosują członkowie kliki
        @param legal_target_size: średnie liczba obiektów, na które głosują uczciwi głosujący
        @param VOTERS: liczba głosujących
        @param OBJECTS: liczba obiektów
        @type bad_hideout: boolean
        @param bad_hideout: parametr mówu o tym, czy członkowie kliki nie głosują na obiekty nie będące ich zadanym celem. 
        """ 
        
        additional_votes = legal_target_size - target_size
        if additional_votes < 0:
            additional_votes = 0
        
        objects = [[] for i in xrange(OBJECTS)] # każdy obiekt ma listę swoich głosujących
        
        import random
        self.voting_rings = [[] for i in xrange(number)]
        for i in xrange(number):
            for j in xrange(size):
                voter = str(random.randint(0, VOTERS))
                while voter in self.voting_rings[i]:
                    voter = str(random.randint(0, VOTERS))
                self.voting_rings[i].append(voter)
                   
        
        # członkowie kliki głosują na swoje cele
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
        
        
        # logger.debug("Non voting cntr is %d" % nonVotingCntr)
        logger.debug("Kliki to:")
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
    """
    Dostarcza metod do czytania/pisania sieci
    """
    
    path = ""
    file_type = FileType.unknown
    graph = nx.Graph()
    
    def __init__(self, path = None, file_type = FileType.VOTING_RING):
        """
        Konstruktor. 
        
        @param path: ścieżka do pliku
        @param file_type: format pliku. W tej wersji obsługiwany jedynie format FileType.VOTING_RING
        """
        if path:
            self.path = path
        self.file_type = file_type
    
    
    def makeGraph(self):
        """
        Tworzy sieć według autorskiej metody wczytując dane o głosowaniu z pliku.
        
        @rtype: networkx.Graph
        @return: Wczytana sieć.
        """
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
            
            logger.info("# Sieć załadowana, węzłów: "  + repr(self.graph.number_of_nodes()) + ", krawędzi: " + repr(self.graph.number_of_edges()))
            return self.graph
    
    def addEdges(self, voters):
        """
        Wykorzystywane przez L{makeGraph} do tworzenia krawędzi na podstawie informacji o oddanych głosach. 
        
        @see: makeGraph
        @param voters: lista głosujących na dany obiekt
        """
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
    """
    Klasa dostarcza metody służącę do wykrywania klik złośliwych głosujących za pomocą autorskiego algorytmu.
    """
    
    graph = nx.Graph()
    minWeight = 0
    maxWeight = 0
    weight_dist = {}


    def __init__(self, graph):
        """
        Konstruktor.
        
        @type graph: networkx.Graph
        @param graph: sieć, stworzona na podstawie informacji o głosowaniach
        """
        self.graph = graph

    def calculateMinMax(self):
        """
        Metoda pomocnicza. Zapisuje do pliku dziennika informacje o największej i najmniejszej wadze krawędzi w sieci.
        """
        
        minEdge = min(self.graph.edges(data=True), key=lambda node: node[2]['weight'])
        self.minWeight = self.graph.get_edge_data(*minEdge[:2])['weight']
        maxEdge = max(self.graph.edges(data=True), key=lambda node: node[2]['weight'])
        self.maxWeight = self.graph.get_edge_data(*maxEdge[:2])['weight']
        
        logger.debug("Waga: max " + repr(self.maxWeight) + " and min " + repr(self.minWeight))

    
    def sliceGraph(self, threshold):
        """
        Metoda służy do odfiltrowania z sieci połączeń o zbyt dużej wadze (świadczących o luźnych związkach pomiędzy węzłami).
        
        Jeżeli dawaj użytkownicy brali udział wspólnie w mniejszej ilości głosowań, niż określa parametr threshold, to krawędź pomiędzy węzłami 
        reprezentującymi tych użytkowników jest usuwana. Następnie usuwane są wszystkie węzły, których stopień jest równy 0 
        (nie są połączone z żadnymi innymi węzłami)
        
        @type threshold: number
        @param threshold: Wartość progu. Minimalna liczba głosowań, w których użytkownicy musieli brać wspólnie udział, aby w sieci istniała krawędź ich łącząca.  
        """

        def filter(edge):
            if edge[2]['weight'] < threshold:
                self.graph.remove_edge(*edge[:2])
                
        map(filter, self.graph.edges(data=True))
        
        # usuń odłączone węzły
        def filterNodes(node):
            if self.graph.degree(node) == 0:
                self.graph.remove_node(node)
                
        map(filterNodes, self.graph.nodes())
        
        # następuje przeliczenie wartości wag krawędzi. Wagi otrzymują docelową wartość, czyli taką, gdzie bardziej związane węzły są połączone
        # krawędzią o mniejszej wadze. W tym celu wagom zostaje przypisana wartość waga = 1/liczba_wspolnych_glosowan 
        def invertWeight(edge):
            try:
                edge[2]['weight'] = int(100/edge[2]['weight'])
            except:
                edge[2]['weight'] = float('Inf')
                logger.error("Błąd przy wyliczaniu wagi krawędzi, ustawiono nieskończoność!!")
        
#        def nullifyWeight(edge):
#            edge[2]['weight'] = 1
        
        map(invertWeight, self.graph.edges(data=True))
#        map(nullifyWeight, self.graph.edges(data=True))
        
        logger.debug("Wykonano filtrowanie z poziomem odcięcia: " + repr(threshold) + ", krawędzi " + repr(self.graph.number_of_edges()) + ", węzłów " + repr(self.graph.number_of_nodes()))
  
    
    def nativeCliquer(self):
        """
        Wykorzystuje metodę znajdowania klik z biblioteki NetworkX. 
        
        Metoda ta nie wykorzystuje algorytmów grupowania, wyznacza jedynie k-kliki. Nie jest to właściwe podejście do problemu.
        """
        cliques = list(nx.find_cliques(self.graph))
        logger.info("Kliki wyznaczone:")
        import pprint
        pprint.pprint(cliques)
 
    def prettyPlotter(self, l=None, filename=None):
        """
        Metod służy do rysowania grafu reprezentującego sieć, w którym węzły należące do tej samej grupy są oznaczone jednym kolorem.
        
        @type l: list
        @param l: lista list węzłów podzielonych na grupy
        @param filename: nazwa pliku PNG z wynikowym obrazem
        """
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
        """
        Metoda zwraca członków noGroups wyznaczonych grup, zaczynając od najmniej licznej. 
        
        @param lists: lista list węzłów podzielonych na grupy
        @param noGroups: liczba grup, których członkowie będą zwróceni
        
        @rtype: list
        @return: lista członków noGroups najmniej licznych grup
        """
        lists.sort(key=len)
        retList = []

        for i in xrange(min(noGroups, len(lists))):
            retList.extend(lists[i])
        
        return retList
        
    
    def smartGetFristNGroups(self, lists, noGroups=2):
        """
        Metoda zwraca członków noGroups wyznaczonych grup, zaczynając od najmniej licznej. 
        Jeżeli zwrócone węzły stanowią mniej niż 10% populacji, metoda zwraca członków noGroups+1 grup. 
        
        @param lists: lista list węzłów podzielonych na grupy
        @param noGroups: liczba grup, których członkowie będą zwróceni
        
        @rtype: list
        @return: lista członków kilki najmniej licznych grup, stanowiących powyżej 10% populacji
        """
        lists.sort(key=len)
        retList = []
        for i in xrange(min(noGroups, len(lists))):
            retList.extend(lists[i])
        
        while len(retList)/len(self.graph) < 0.1:
            # if this still lower then 10% of population, get more groups
            i += 1
            try:
                retList.extend(lists[i])
            except:
                logger.error("To byłą ostatani grupa! Zwrócono  %f procent." % (len(retList)/len(self.graph)))
                
        return retList
    
    @timeit
    def blondelAlgorithm(self):
        """
        Metoda wykonuje grupowanie za pomocą algorytmu Blodela et al.
        @rtype: list
        @return: lista list z członkami grup
        """
        from lib import blondel
        
        d = blondel.best_partition(self.graph)
        # zwraca słownik węzłów z numerem grupy jako wartość
        logger.debug("Algorytm Blondela wykonany")

        # zamieniamy na listę list
        
        clusters = max(d.values())
        nodeList = [None]*(clusters+1)

        for k in d.keys():
            if not nx.utils.is_list_of_ints(nodeList[d[k]]):
                nodeList[d[k]] = []
            nodeList[d[k]].append(k)
        
        return nodeList
    
    @timeit
    def newmanAlgorithm(self):
        """
        Metoda wykonuje grupowanie za pomocą algorytmu Girvana-Newaman.
        @rtype: list
        @return: lista list z członkami grup
        """
        from lib import newman
        (Q, partition) = newman.detect_communities(self.graph)
        # returns list o lists (each list for community) as a second tuple member
        logger.debug("Newman zrobiony")
        
        return partition 
    
    @timeit
    def causetNewmanAlgorithm(self, verbose=False):
        """
        Metoda wykonuje grupowanie za pomocą algorytmu Caluseta-Newmana
        @rtype: list
        @return: lista list z członkami grup
        """
        from lib import causet_newman
        
        (maxQ, partition, tree, treeRoot) = causet_newman.communityStructureNewman(self.graph)
        # returns list o lists (each list for community) as a second tuple member
        logger.debug("Causet-Newman zrobiony")
        
        return partition    
    
    @timeit
    def MCLAlgorithm(self, inflation=3.3):
        """
        Metoda wykonuje grupowanie za pomocą algorytmu MCL
        
        @param inflation: wartość współczynnika inflacji algorytmu MCL
        @requires: program MCL w ścieżce wykonywalnej 
        @rtype: list
        @return: lista list z członkami grup
        """
        
        try:
            nx.write_weighted_edgelist(self.graph, "/tmp/mcl-input", delimiter="\t")
        except:
            nx.write_edgelist(self.graph, "/tmp/mcl-input", delimiter="\t")
        import os
        logger.debug("Invoking mcl command ...")
        os.system("mcl /tmp/mcl-input --abc -te 2 -I %f -o /tmp/mcl-output" % inflation)
        logger.debug("MCL clustering done")
        
        out_file = open("/tmp/mcl-output", 'r')
        lines = out_file.readlines()
        
        partition = list()
        
        import string
        for line in lines:
            partition.append(map(int, string.split(line)))
        
        return partition
        
