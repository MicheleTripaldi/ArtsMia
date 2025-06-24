import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._artObject = None
        self._grafo = nx.Graph()
        self._idMap = {}

        self._bestPath = []
        self._bestCost = 0


    def getOptPath(self, source, lun):
        self._bestPath = []
        self._bestCost = 0

        parziale = [source]

        for n in self._grafo.neighbors(source):
            if parziale[-0].classification == n.classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

        return self._bestPath, self._bestCost


    def _ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            # allora parziale ha la lunghezza desiderata,
            # verifico se è una soluzione migliore,
            # ed in ogni caso esco
            if self.costo(parziale) > self._bestCost:
                self._bestCost = self.costo(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        # se arrivo qui, allora parziale può ancora ammettere altri nodi
        for n in self._grafo.neighbors(parziale[-1]):
            if parziale[-0].classification == n.classification and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()


    def costo(self, listObjects):
        totCosto = 0
        for i in range(0, len(listObjects) - 1):
            totCosto += self._grafo[listObjects[i]][listObjects[i + 1]]["weight"]
        return totCosto

    def getInfoConnessa(self, idInput):
        """
        Identifica la componente connessa che contiene  idInput
        e ne restituisce la dimensione DFS serve peer cercare le connessioni
        """
        if not self.hasNode(idInput):
            return None
        source = self._idMap[idInput]

        # Modo 1 : conto i successori ## adesso anche questo  giusto
        succ = nx.dfs_successors(self._grafo, source).values()#
        res = []#
        for s in succ:#
            res.extend(s) # non facciamo l'append
        #print("Size connessa con modo 1: ", len(res)+1)

        # modo 2 conto i predecessori
        pred = nx.dfs_predecessors(self._grafo, source)
        #print("Size connessa con modo 2:", len(pred.values())+1)

        # modo 3 per capire chi ha ragione: conto i nodi dell'albero di visita
        dfsTree = nx.dfs_tree(self._grafo, source)
        #print("Size connessa con modo 3:", len(dfsTree))

        # modo 4 uso il metodo nodes_connected_components
        conn = nx.node_connected_component(self._grafo, source)
        print("Size connessa con modo 4:", len(conn))

        return len(conn) # uno dei quattro( 1 e 2 devo agg 1)


    def hasNode(self,idInput): # verifica se c'è  id nel grafo
        return idInput in self._idMap



    def buildGraph(self):
        self._grafo.clear()
        self._artObject = DAO.getAllNodes()
        for o in self._artObject:
            self._idMap[o.object_id] = o

        self._grafo.add_nodes_from(self._artObject)
        self.addAllEdges()

    def addAllEdges(self):
        edges = DAO.getAllArchi(self._idMap)

        for ed in edges:
            self._grafo.add_edge(ed.nodo1, ed.nodo2, weight = ed.peso)


    def getNumNodes(self):
        return len(self._grafo.nodes)
    def getNumEdges(self):
        return len(self._grafo.edges)
    def getIdMap(self):
        return
    def getObjectFromId(self,id):
        return