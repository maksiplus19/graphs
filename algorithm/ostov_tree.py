from algorithm.connectedness import isConnected
from graph.graph import Graph
import numpy as np


# def prima(graph):
#     if graph.oriented:
#         return "Граф ориентированный"
#     connect = isConnected(graph.to_matrix(), graph.oriented)
#     if connect == "Граф связный":
#         size = graph.size()
#         ostov = [[0]*size for i in range(size)]
#         used = [False]*size
#         ends = ["1"]
#         v = "1"
#         while True:
#             used[int(v) - 1] = True
#             min = np.inf
#             for end in ends:
#                 for to in graph.vertexes[end]:
#                     if graph.vertexes[end][to][0][0] < min and not used[int(to) - 1]:
#                         minto = to
#                         min = graph.vertexes[v][to][0][0]
#             if min == np.inf:
#                 break
#             ostov[int(v) - 1][int(minto) - 1] = min
#             ostov[int(minto) - 1][int(v) - 1] = min
#             v = minto
#
#         gr = Graph.from_matrix(ostov)
#         gr.oriented = graph.oriented
#         return gr
#     else:
#         return "Граф не связный"


def search_min(tr, vizited):  # 1 место для оптимизации
    min = np.inf
    for ind in vizited:
        for index, elem in enumerate(tr[ind]):
            if 0 < elem < min and index not in vizited:
                min = elem  # веса путей
                index2 = index  # индекс города
                index3 = ind
    return [min, index2, index3]


def prima(matr):
    toVisit = [i for i in range(1, len(matr))]  # города кроме начального(0)
    vizited = [0]
    result = [0]  # начнем с минска
    size = len(matr)
    g = [[0]*size for i in range(size)]
    for index in toVisit:
        weight, ind1, ind2 = search_min(matr, vizited)
        g[ind1][ind2] = weight
        g[ind2][ind1] = weight
        result.append(weight)  # в результат будут заноситься веса
        vizited.append(ind1)  # содержит карту пути

    gr = Graph.from_matrix(g)
    gr.oriented = False
    return gr


def kruscal(graph):
    size = graph.size()
    edges = []
    for v in graph.vertexes:
        for to in graph.vertexes[v]:
            edge = []
            edge.append(graph.vertexes[v][to][0][0])
            edge.append(int(v) - 1)
            edge.append(int(to) - 1)
            edges.append(edge)

    print(edges)
    for i in edges:
        for j in edges:
            if i[0] == j[0] and i[1] == j[2] and i[2] == j[1] and i != j:
                edges.remove(j)
    edges.sort()

    tree = []
    cost = 0
    g = [[0]*size for i in range(size)]
    for i in range(size):
        tree.append(i)
    for i in range(len(edges)):
        a = edges[i][1]
        b = edges[i][2]
        l = edges[i][0]
        if tree[a] != tree[b]:
            cost += l
            g[a][b] = l
            g[b][a] = l
            old_id = tree[b]
            new_id = tree[a]
            for j in range(size):
                if tree[j] == old_id:
                    tree[j] = new_id

    gr = Graph.from_matrix(g)
    gr.oriented = graph.oriented

    return gr
