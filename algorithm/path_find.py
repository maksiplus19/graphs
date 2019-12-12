from typing import Dict, List, Union
from enum import IntEnum, auto

import numpy as np

from graph.graph import Graph
from graph.vertex import Vertex


class Flags(IntEnum):
    FOUND = auto()
    NOT_FOUND = auto()


def __get_path(parents: dict, v_to: str) -> list:
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
            old_key = key
            key = f'{path[i + 1]}_{path[i]}'
            res[key] = edges[old_key]
    return res


def after_work(graph: Graph, v_from: str, end: str, edges: Dict, parents: Dict, distance: np.array):
    if distance[int(end) - 1] < np.inf:
        p = __get_path(parents, end)
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
    size = graph.size()
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
        key = min(d.items(), key=lambda el: el[1] + __cost(graph, el[0], end))[0]
        d.pop(key)
        return key

    size = graph.size()
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
            p = __get_path(parents, end)
            graph.path = p
            graph.edge_path = __get_edges(p, edges, graph.oriented)
            return distance[int(end) - 1]

        for v_to in graph.vertexes[current_vertex]:
            new_cost = distance[int(current_vertex) - 1] + graph.vertexes[current_vertex][v_to][0][0]
            if v_to in closed and new_cost >= distance[int(v_to) - 1]:
                continue
            if v_to not in queue or new_cost < distance[int(v_to) - 1]:
                parents[v_to] = current_vertex
                distance[int(v_to) - 1] = distance[int(current_vertex) - 1] + graph.vertexes[current_vertex][v_to][0][0]
                edges[f'{current_vertex}_{v_to}'] = graph.vertexes[current_vertex][v_to][0][1]
                if v_to not in queue:
                    queue[v_to] = distance[int(v_to) - 1]

        closed[current_vertex] = True

    return after_work(graph, begin, end, edges, parents, distance)


def __find_edge(graph: Graph, path: List):
    edges = {}
    for i in range(len(path) - 1):
        key = f'{path[i]}_{path[i + 1]}'
        node = graph.vertexes[path[i]][path[i + 1]][0][1]
        edges[key] = node
        if not graph.oriented:
            key = f'{path[i + 1]}_{path[i]}'
            node = graph.vertexes[path[i + 1]][path[i]][1]
            edges[key] = node
    return edges


def __get_distance(graph: Graph, path: List):
    d = 0
    for i in range(1, len(path)):
        d += graph.vertexes[path[i - 1]][path[i]][0][0]
    return d


best_path: List = None


def IDA_star(graph: Graph, begin: str, end: str) -> Union[None, int]:
    global best_path
    best_path = None

    def IDA_search(p: List, g: int, b: int, finish: str) -> int:
        # global best_path
        global best_path
        node = p[-1]
        f = g + int(__cost(graph, node, finish))
        if node == finish:
            return Flags.FOUND
        less = np.inf
        found = False
        for v_to, weight in graph.vertexes[node].items():
            if v_to not in p:
                p.append(v_to)
                t = IDA_search(p, g + weight[0][0], b, finish)
                if t == Flags.FOUND:
                    found = True
                    if best_path is None or (
                            p[-1] == finish and __get_distance(graph, p) < __get_distance(graph, best_path)):
                        best_path = p.copy()
                    p.pop()
                if t < less:
                    less = t
        return Flags.FOUND if found else less

    size = graph.size()
    if size <= 0 or begin not in graph.vertexes or end not in graph.vertexes:
        return None

    bound = int(__cost(graph, begin, end))
    path = [begin]

    status = None
    t = None
    while status is None:
        t = IDA_search(path, 0, bound, end)
        if t == Flags.FOUND:
            status = Flags.FOUND
        if t == np.inf:
            status = Flags.NOT_FOUND
        bound = t

    if status == Flags.NOT_FOUND:
        return None
    else:
        graph.path = best_path
        graph.edge_path = __find_edge(graph, best_path)
        return __get_distance(graph, best_path)
