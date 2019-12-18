"""This module implements the graph coloring algorithm"""

from typing import Dict, List, Tuple, Optional

from PyQt5.QtGui import QColor

from graph.graph import Graph


def __get_degrees(graph: Graph) -> List[Tuple[str, int]]:
    """Method return vector of vertexes degrees sorted in descending order"""
    degrees: List[Tuple[str, int]] = []
    for v_from, to_dict in graph.vertexes.items():
        degrees.append((v_from, sum([1 for to_list in to_dict.values() if len(to_list)])))
    return sorted(degrees, key=lambda el: el[1], reverse=True)


def coloring(graph: Graph) -> Optional[int]:
    """The algorithm for coloring a graph"""
    if graph.size() == 0:
        return 0
    if not sum((sum(graph.to_matrix(with_weight=False), []))):
        for v in graph.vertexes_coordinates.values():
            v.color = generate_color(1)
        return 1
    colors: Dict[str, int] = {}
    degrees: List[Tuple[str, int]] = __get_degrees(graph)
    colors[degrees[0][0]] = 1

    while len(colors) != len(degrees):
        for vertex_name, _ in degrees:
            neighbor_colors = [
                colors.get(name) for name in graph.vertexes[vertex_name]
                if colors.get(name) is not None
            ]
            if not neighbor_colors:
                neighbor_colors = [0]
            color = 0
            for i in range(1, max(neighbor_colors) + 2):
                if i not in neighbor_colors:
                    color = i
                    break
            colors[vertex_name] = color

    for vertex in graph.vertexes_coordinates.values():
        vertex.color = generate_color(colors[vertex.name])

    return max(colors.values())


def generate_color(seed: int) -> QColor:
    """Key-based color generation method"""
    return QColor(seed * 101 % 255, seed * 211 % 255, seed * 307 % 255)
