from algorithm.connectedness import isConnected
from graph.graph import Graph
import numpy as np


def prima(graph):
    if graph.oriented:
        return "Граф ориентированный"
    connect = isConnected(graph.to_matrix(), graph.oriented)
    if connect == "Граф связный":
        size = graph.size()
        ostov = [[0]*size for i in range(size)]
        used = [False]*size
        v = "1"
        while True:
            used[int(v) - 1] = True
            min = np.inf
            for to in graph.vertexes[v]:
                if graph.vertexes[v][to][0][0] < min and not used[int(to) - 1]:
                    minto = to
                    min = graph.vertexes[v][to][0][0]
            if min == np.inf:
                break
            ostov[int(v) - 1][int(minto) - 1] = min
            ostov[int(minto) - 1][int(v) - 1] = min
            v = minto

        gr = Graph.from_matrix(ostov)
        gr.oriented = graph.oriented
        return gr
    else:
        return "Граф не связный"
