import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMap = {}
        for v in self._nodes:
            self._idMap[v.object_id] = v
        self._bestPath = []
        self._bestCost = 0

    def getOptPath(self, source, lun):
        self._bestPath = []
        self._bestCost = 0

        parziale = [source]

        for n in self._graph.neighbors(source):
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

        # se arrvo qui allora parziale può ancora ammetetere nuovi nodi
        for n in self._graph.neighbors(parziale[-1]):

            parziale.append(n)
            self._ricorsione(parziale, lun)
            parziale.pop()



    def costo(self, listObjects):
        totCosto =0
        for i in range(0, len(listObjects)-1):
            totCosto += self._graph[listObjects[i]][listObjects[i+1]["weight"]]

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
        succ = nx.dfs_successors(self._graph, source).values()#
        res = []#
        for s in succ:#
            res.extend(s) # non facciamo l'append
        print("Size connessa con modo 1:", len(succ.values()))

        # modo 2 conto i predecessori
        pred = nx.dfs_predecessors(self._graph, source)
        print("Size connessa con modo 2:", len(pred.values()))

        # modo 3 per capire chi ha ragione: conto i nodi dell'albero di visita
        dfsTree = nx.dfs_tree(self._graph, source)
        print("Size connessa con modo 3:", len(dfsTree))

        # modo 4 uso il metodo nodes_connected_components
        conn = nx.node_connected_component(self._graph, source)
        print("Size connessa con modo 4:", len(conn))

        return len(conn) # uno dei quattro( 1 e 2 devo agg 1)




    def hasNode(self,idInput): # verifica se c'è  id nel grafo
        #return self._idMap[idInput] is self._graph
        return idInput in self._idMap



    def buildGraph(self):

        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges()

    def addEdgesV1(self):# ci mette tantissimo
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u, v)
                if (peso != None):
                    self._graph.add_edge(u, v, weight=peso)

    def addAllEdges(self):

        allEdges = DAO.getAllArchi(self._idMap)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getNumNodes(self):
        return len(self._graph.nodes)
    def getNumEdges(self):
        return len(self._graph.edges)
    def getIdMap(self):
        return self._idMap
    def getObjectFromId(self,id):
        return self._idMap[id]