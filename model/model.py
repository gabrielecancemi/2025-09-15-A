import copy
from datetime import date

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._g = nx.Graph()
        self._idPiloti = dict()
        self.lista = []
        self.range = 1000

    def getAnni(self):
        return DAO.getAllYears()

    def creaGrafo(self, anno1, anno2):
        self._g.clear()
        self._idPiloti = dict()

        print(self.dimGrafo())
        piloti = DAO.getPiloti(anno1, anno2)
        for p in piloti:
            p.age = date.today().year - p.dob.year
            self._idPiloti[p.driverId] = p
        self._g.add_nodes_from(piloti)
        print(self.dimGrafo())
        archi = DAO.getArchi(anno1, anno2)
        for a in archi:
            p1 = self._idPiloti[a[0]]
            p2 = self._idPiloti[a[1]]
            w = a[2]
            self._g.add_edge(p1, p2, weight=w)

    def dimGrafo(self):
        return len(self._g.nodes), len(self._g.edges)

    def archiMaggiori(self):
        archi = []
        for e in self._g.edges:
            w = self._g[e[0]][e[1]]["weight"]
            archi.append((e[0], e[1], w))
        archi.sort(key=lambda x: x[2], reverse=True)
        if len(archi) >= 3:
            l = 3
        else:
            l = len(archi)
        return archi[0:l]

    def compConnesse(self):
        comp = list(nx.connected_components(self._g))
        comp.sort(key=lambda x: len(x), reverse=True)
        maggiore = []
        if len(comp) > 0:
            maggiore = comp[0]
        ordinata = []
        for m in maggiore:
            ordinata.append((m, self._g.degree(m)))
        ordinata.sort(key=lambda x: x[1], reverse=True)

        return len(comp), maggiore, ordinata

    def cercaPiloti(self, k):
        self.lista = []
        self.range = 1000
        for n in self._g.nodes:
            self.ricorsione([n], 1000, k)


        return self.lista, self.range, min(p.dob.year for p in self.lista), max(p.dob.year for p in self.lista)

    def ricorsione(self, parziale, range_ac, k):

        if len(parziale) == k:
            if self.range > range_ac:
                self.range = range_ac
                self.lista = copy.deepcopy(parziale)
        else:
            for n in self._g.nodes:
                parziale.append(n)
                range_new = self.check(parziale)
                if range_new is not None:
                    self.ricorsione(parziale, range_new, k)
                parziale.pop()

    def check(self, parziale):
        if parziale[-1] in parziale[0:-1]:
            return None

        for p in parziale[0:-1]:
            if nx.has_path(self._g, parziale[-1], p):
                return None

        range_new = int(max(p.age for p in parziale)) - int(min(p.age for p in parziale))
        if range_new > self.range:
            return None

        return range_new