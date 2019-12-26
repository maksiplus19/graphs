from algorithm.dijkstra_and_other import floydWorshel
from typing import Dict, List, Union
import numpy as np


def isConnected(matrix, oriented):
    if not oriented:
        matrix_dist = floydWorshel(matrix, oriented)
        for i in range(len(matrix_dist)):
            for j in range(len(matrix_dist[i])):
                if matrix_dist[i][j] == np.inf and matrix_dist[j][i] == np.inf:
                    return "Граф не связный"
        return "Граф связный"
    else:
        matrix_dist = floydWorshel(matrix, oriented)
        isConnect = True
        for i in range(len(matrix_dist)):
            for j in range(len(matrix_dist[i])):
                if matrix_dist[i][j] == np.inf:
                    isConnect = False
        if isConnect:
            return "Граф сильно связный"
        not_oriented_matrix = [[0]*len(matrix) for i in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] != 0:
                    not_oriented_matrix[i][j] = matrix[i][j]
                    not_oriented_matrix[j][i] = matrix[i][j]
                elif matrix[j][i] == 0:
                    not_oriented_matrix[i][j] = 0
                    not_oriented_matrix[j][i] = 0
        if isConnected(not_oriented_matrix, False) is "Граф связный":
            return "Граф слабо связный"
        return "Граф не связный"


def find_comps(graph):
    def dfs(v, used, g, comp, before: int = -1):
        if before == -1:
            used[v] = True
            comp.append(str(v + 1))
        else:
            return
        for key in g.vertexes[str(v + 1)]:
            if not used[int(key) - 1]:
                dfs(int(key) - 1, used, g, comp, v)
    size = graph.size()
    used = []
    comps = []
    for i in range(size):
        used.append(False)
    for i in range(size):
        if not used[i]:
            comp = []
            dfs(i, used, graph, comp)
            comps.append(comp)

    return comps


def find_bridges(graph):
    def dfs(v, used, g, tin, fup, timer, bridges, hinges, before: int = -1):
        if before == -1 or str(before + 1) in g.vertexes[str(v + 1)]:
            used[v] = True
            timer += 1
            tin[v] = fup[v] = timer
            children = 0
        else:
            return
        for key in g.vertexes[str(v + 1)]:
            if key == str(before + 1):
                continue
            if used[int(key) - 1]:
                fup[v] = min(fup[v], tin[int(key) - 1])
            else:
                dfs(int(key) - 1, used, g, tin, fup, timer, bridges, hinges, v)
                fup[v] = min(fup[v], fup[int(key) - 1])
                if fup[int(key) - 1] > tin[v]:
                    bridges.append(str(v + 1) + " - " + key)
                if fup[int(key) - 1] >= tin[v] and before != -1:
                    hinges.append(str(v+1))
        if before == -1 and children > 1:
            hinges.append(str(v+1))

    bridges = []
    hinges = []
    timer = 0
    size = graph.size()
    used = []
    tin = []
    fup = []
    for i in range(size):
        used.append(False)
        tin.append(np.inf)
        fup.append(np.inf)
    for i in range(size):
        if not used[i]:
            dfs(i, used, graph, tin, fup, timer, bridges, hinges)

    return bridges, hinges
