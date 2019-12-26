from graph.graph import Graph
from algorithm import dijkstra
from algorithm.connectedness import isConnected
import numpy as np
import networkx as nx


def dfs(v, used, g, p=-1):
    used[v] = True
    for to in g.vertexes[str(v+1)]:
        if not used[int(to) - 1]:
            return dfs(int(to) - 1, used, g, v)
        elif int(to) - 1 != p:
            return True
    return False


def isCycled(graph):
    used = [False]*graph.size()
    for v in graph.vertexes:
        if dfs(int(v) - 1, used, graph):
            return True
        used = [False] * graph.size()
    return False


def find_center(graph):
    if isConnected(graph.to_matrix(), graph.oriented) == "Граф не связный":
        return "Граф не связный", None
    size = graph.size()
    ecscentr = []
    centres = []
    for i in range(size):
        dist = dijkstra(str(i + 1), graph.to_matrix())
        ecscentr.append(max(dist))
    r = min(ecscentr)
    for i in range(len(ecscentr)):
        if r == ecscentr[i]:
            centres.append(str(i+1))

    return centres, r


def to_prufer(graph):
    if graph.oriented:
        return False
    leaves = []
    size = graph.size()
    killed = [False] * size
    degrees = []
    for i in range(size):
        degrees.append(len(graph.vertexes[str(i+1)]))
        if degrees[i] == 1:
            leaves.append(i)
    leaves.sort()
    result = []
    for i in range(size-2):
        leaf = leaves[0]
        leaves.pop(0)
        killed[leaf] = True
        for j in graph.vertexes[str(leaf+1)]:
            if not killed[int(j) - 1]:
                v = int(j) - 1
        result.append(v+1)
        degrees[v] -= 1
        if degrees[v] == 1:
            leaves.append(v)
            leaves.sort()
    return result



def find_mincycle(graph):
    # size = graph.size()
    # mincycle = []
    # mincycle.append(np.inf)
    # matr = graph.to_matrix()
    # dist = graph.to_matrix()
    # for i in range(size):
    #     for j in range(size):
    #         if matr[i][j] == 0:
    #             matr[i][j] = dist[i][j] = np.inf
    # for k in range(size):
    #     for i in range(k):
    #         for j in range(i):
    #             mincycle[0] = min(mincycle[0], dist[i][j] + matr[j][k] + matr[k][i])
    #
    #     for i in range(size):
    #         for j in range(i):
    #             temp = dist[i][k] + dist[k][j]
    #             if temp < dist[i][j]:
    #                 dist[i][j] = dist[j][i] = temp

    # if graph.oriented:
    #     mincycle -= 1
    g = nx.Graph()
    nx.Graph()
    size = graph.size()
    matr = graph.to_matrix()
    for i in range(1, size + 1):
        g.add_node(i)
        for j in range(1, size + 1):
            if matr[i - 1][j - 1] is not 0:
                g.add_edge(i, j)
    return nx.minimum_cycle_basis(g)[0]
    # return mincycle

