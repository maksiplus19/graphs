from typing import Dict, List, Union
from enum import IntEnum, auto

import numpy as np
import copy

from graph.graph import Graph
from graph.vertex import Vertex


def dijkstra(begin: str, matr, oriented):
    size = len(matr)
    matrix = copy.deepcopy(matr)

    for i in range(size):
        for j in range(size):
            if matrix[i][j] == 0:
                matrix[i][j] = np.inf
            if not oriented:
                matrix[i][j] = matrix[i][j]//2

    valid = np.repeat(True, size)
    weight = np.repeat(np.inf, size)
    weight[int(begin) - 1] = 0
    for i in range(size):
        min_weight = np.inf
        id_min_weight = -1
        for j in range(size):
            if valid[j] and weight[j] < min_weight and i is not j:
                min_weight = weight[j]
                id_min_weight = j
        for j in range(size):
            if weight[id_min_weight] + matrix[id_min_weight][j] < weight[j]:
                weight[j] = weight[id_min_weight] + matrix[id_min_weight][j]
        valid[id_min_weight] = False

    # for i in range(len(weight)):
    #     if weight[] == np.inf:
    #         weight[i] = 0

    return weight


def floydWorshel(matr, oriented):
    matrix = copy.deepcopy(matr)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0 and i != j:
                matrix[i][j] = np.inf
            if not oriented:
                matrix[i][j] = matrix[i][j] / 2

    for k in range(len(matrix)):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

    return matrix


def bellmanFord(graph: Graph, begin: str):
    size = graph.size()
    dist = np.repeat(np.inf, size)
    dist[int(begin) - 1] = 0
    for k in range(1, size):
        for i in graph.vertexes.keys():
            for j in graph.vertexes[i].keys():
                if dist[int(i)-1] + graph.vertexes[i][j][0][0] < dist[int(j)-1]:
                    dist[int(j) - 1] = dist[int(i)-1] + graph.vertexes[i][j][0][0]

    print(dist)
    return dist



