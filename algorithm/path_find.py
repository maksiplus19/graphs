from copy import copy
from typing import Optional, Dict, List, Union

import numpy as np

from graph.graph import Graph


def __get_path(parents: dict, v_from: str, v_to: str) -> list:
    path = []
    vertex = v_to
    while vertex is not None:
        if vertex not in path:
            path.append(vertex)
        vertex = parents[vertex]
    return path


def __get_edges(path: list, edges: dict) -> dict:
    res = {}
    path = list(reversed(path))
    for i in range(len(path) - 1):
        key = f'{path[i]}_{path[i + 1]}'
        res[key] = edges[key]
    return res


def BFS(graph: Graph, v_from: str, end: str) -> Union[None, int]:
    """
    Поиск пути
    (a) Breadth-First Search для пары указанных вершин;
    """
    # graph = copy(graph)
    size = int(graph.get_new_vertex_name()) - 1
    if size <= 0 or v_from not in graph.vertexes or end not in graph.vertexes:
        return None
    queue = [v_from]
    viewed = np.zeros(size, dtype=int)
    distance = np.repeat(np.inf, size)
    distance[int(v_from) - 1] = 0
    parents = {v_from: None}
    edges = {}

    while queue:
        current_vertex = queue.pop(0)
        current_vertex = int(current_vertex) - 1
        viewed[current_vertex] = True

        for v_to, to_list in graph.vertexes[str(current_vertex + 1)].items():
            v_to = int(v_to) - 1
            edge = to_list[0][0]
            if not viewed[v_to] and v_to not in queue:
                queue.append(str(v_to + 1))

            if distance[current_vertex] + edge < distance[v_to]:
                distance[v_to] = distance[current_vertex] + edge
                parents[str(v_to + 1)] = str(current_vertex + 1)
                edges[f'{current_vertex + 1}_{v_to + 1}'] = edge

    if distance[int(end) - 1] < np.inf:
        # return {'path': get_path(parents, v_from, end), 'distance': distance[end]}
        p = __get_path(parents, v_from, end)
        graph.path = p
        graph.edge_path = __get_edges(p, edges)
    else:
        graph.path = []
        graph.edge_path = {}
    return distance[int(end) - 1]


def __euclid_distance(x1: float, y1: float, x2: float, y2: float):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def __cost(graph: Graph, v1: str, v2: str):
    v1 = graph.vertexes_coordinates[v1]
    v2 = graph.vertexes_coordinates[v2]
    return __euclid_distance(v1.x, v1.y, v2.x, v2.y)


def A_star(graph: Graph, begin: str, end: str):
    def get_min(d: dict):
        key = min(d.items(), key=lambda el: el[1])[0]
        d.pop(key)
        return key

    size = int(graph.get_new_vertex_name()) - 1
    if size <= 0 or begin not in graph.vertexes or end not in graph.vertexes:
        return None
    opened, closed, parents, edges, queue = {}, {}, {}, {}, {}
    opened[begin] = True
    distance = np.repeat([np.inf], size)
    distance[int(begin) - 1] = 0
    parents[begin] = None
    queue[begin] = 0

    while queue:
        current_vertex = get_min(queue)

        if current_vertex == end:
            p = __get_path(parents, begin, end)
            graph.path = p
            graph.edge_path = __get_edges(p, edges)
            return distance[int(end) - 1]

        for v_to in graph.vertexes[current_vertex]:
            new_cost = distance[int(current_vertex) - 1] + __cost(graph, current_vertex, v_to)
            if v_to in closed and new_cost >= distance[int(v_to) - 1]:
                continue
            if v_to not in opened or new_cost < distance[int(v_to) - 1]:
                parents[v_to] = current_vertex
                distance[int(v_to) - 1] = distance[int(current_vertex) - 1] + graph.vertexes[current_vertex][v_to][0][0]
                edges[f'{current_vertex}_{v_to}'] = graph.vertexes[current_vertex][v_to][0][0]
                if v_to not in queue:
                    queue[v_to] = distance[int(v_to) - 1]

    if distance[int(end) - 1] < np.inf:
        p = __get_path(parents, begin, end)
        graph.path = p
        graph.edge_path = __get_edges(p, edges)
    else:
        graph.path = []
        graph.edge_path = {}
    return distance[int(end) - 1]
