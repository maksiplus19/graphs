from graph.graph import Graph
from algorithm import dijkstra
import numpy as np


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
    leaves = []
    size = graph.size()
    prufer = ""
    for i in range(size):
        graph[str(i+1)]

