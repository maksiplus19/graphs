from algorithm.dijkstra_and_other import floydWorshel
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


def dfs(v, before, used, g, comp):
    if before == -1 or str(before+1) in g.vertexes[str(v+1)]:
        used[v] = True
        # print(g.vertexes[str(before + 1)][str(v + 1)])
        comp.append(str(v+1))
    else:
        return
    for key in g.vertexes[str(v+1)]:
        if not used[int(key) - 1]:
            dfs(int(key) - 1, v, used, g, comp)


def find_comps(graph):
    size = graph.size()
    used = []
    comps = []
    for i in range(size):
        used.append(False)
    for i in range(size):
        if not used[i]:
            comp = []
            dfs(i, -1, used, graph, comp)
            comps.append(comp)

    return comps
