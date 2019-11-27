from typing import Optional, Dict, List, Union
from enum import IntEnum, auto

import numpy as np

from graph.graph import Graph
from graph.vertex import Vertex

class Flags(IntEnum):
    FOUND = auto()
    NOT_FOUND = auto()


def __get_path(parents: dict, v_from: str, v_to: str) -> list:
    path = []
    vertex = v_to
    while vertex is not None:
        if vertex not in path:
            path.append(vertex)
        vertex = parents[vertex]
    return path


def __get_edges(path: list, edges: Dict[str, Vertex], oriented: bool) -> Dict:
    res = {}
    path = list(reversed(path))
    for i in range(len(path) - 1):
        key = f'{path[i]}_{path[i + 1]}'
        res[key] = edges[key]
        if not oriented:
            key = f'{path[i + 1]}_{path[i]}'
            res[key] = edges[key]
    return res


def after_work(graph: Graph, v_from: str, end: str, edges: Dict, parents: Dict, distance: np.array):
    if distance[int(end) - 1] < np.inf:
        p = __get_path(parents, v_from, end)
        graph.path = p
        graph.edge_path = __get_edges(p, edges, graph.oriented)
    else:
        graph.path = []
        graph.edge_path = {}
    return distance[int(end) - 1]


def BFS(graph: Graph, begin: str, end: str) -> Union[None, int]:
    """
    Поиск пути
    (a) Breadth-First Search для пары указанных вершин;
    """
    size = int(graph.get_new_vertex_name()) - 1
    if size <= 0 or begin not in graph.vertexes or end not in graph.vertexes:
        return None
    queue = [begin]
    viewed = np.zeros(size, dtype=int)
    distance = np.repeat(np.inf, size)
    distance[int(begin) - 1] = 0
    parents = {begin: None}
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
                edges[f'{current_vertex + 1}_{v_to + 1}'] = to_list[0][1]

    return after_work(graph, begin, end, edges, parents, distance)


def __euclid_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def __cost(graph: Graph, v1: str, v2: str) -> float:
    v1 = graph.vertexes_coordinates[v1]
    v2 = graph.vertexes_coordinates[v2]
    return __euclid_distance(v1.x, v1.y, v2.x, v2.y)


def A_star(graph: Graph, begin: str, end: str) -> Union[None, int]:
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
            graph.edge_path = __get_edges(p, edges, graph.oriented)
            return distance[int(end) - 1]

        for v_to in graph.vertexes[current_vertex]:
            new_cost = distance[int(current_vertex) - 1] + __cost(graph, current_vertex, end)
            if v_to in closed and new_cost >= distance[int(v_to) - 1]:
                continue
            if v_to not in opened or new_cost < distance[int(v_to) - 1]:
                parents[v_to] = current_vertex
                distance[int(v_to) - 1] = distance[int(current_vertex) - 1] + graph.vertexes[current_vertex][v_to][0][0]
                edges[f'{current_vertex}_{v_to}'] = graph.vertexes[current_vertex][v_to][0][1]
                if v_to not in queue:
                    queue[v_to] = distance[int(v_to) - 1]

    return after_work(graph, begin, end, edges, parents, distance)


def IDA_search(path: List, g: int, bound: int, graph: Graph, end: str) -> int:
    node = path[-1]
    f = g + int(__cost(graph, node, end))
    if f > bound:
        return f
    if node == end:
        return Flags.FOUND
    less = np.inf
    for v_to, weight in graph.vertexes[node].items():
        if v_to not in path:
            path.append(v_to)
            t = IDA_search(path, g + weight[0][0], bound, graph, end)
            if t == Flags.FOUND:
                return Flags.FOUND
            if t < less:
                less = t
            path.pop()
    return less


def __find_edge(graph: Graph, path: List):
    edges = {}
    for i in range(len(path) - 1):
        key = f'{path[i]}_{path[i + 1]}'
        node = graph.vertexes[path[i]][path[i + 1]][0][1]
        edges[key] = node
        if not graph.oriented:
            key = f'{path[i+1]}_{path[i]}'
            node = graph.vertexes[path[i+1]][path[i]][1]
            edges[key] = node
    return edges


def __get_distance(graph: Graph, path: List):
    d = 0
    for i in range(1, len(path)):
        d += graph.vertexes[path[i-1]][path[i]][0][0]
    return d


def IDA_star(graph: Graph, begin: str, end: str) -> Union[None, int]:
    size = int(graph.get_new_vertex_name()) - 1
    if size <= 0 or begin not in graph.vertexes or end not in graph.vertexes:
        return None

    bound = int(__cost(graph, begin, end))
    path = [begin]

    status = None
    while status is None:
        t = IDA_search(path, 0, bound, graph, end)
        if t == Flags.FOUND:
            status = Flags.FOUND
        if t == np.inf:
            status = Flags.NOT_FOUND
        bound = t

    if status == Flags.NOT_FOUND:
        return None
    else:
        graph.path = path
        graph.edge_path = __find_edge(graph, path)
        return __get_distance(graph, path)
    # обработать восстановить путь
