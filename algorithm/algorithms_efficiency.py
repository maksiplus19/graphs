# -*- coding: utf-8 -*-
"""
в серединах левой и правой сторон
в противоположных углах
ы центре квадрата и в середине нижней стороны
произвольные вершины
"""
import random
import time
from datetime import datetime
from typing import Tuple, Dict

import numpy as np

import algorithm
from graph.graph import Graph
from graph.savegraph import SaveGraph
from ui.sourse.graphicsvertex import VERTEX_RADIUS
from ui.sourse.qgraphview import QGraphView

SPACE = 10

neighbor_dict: Dict[int, Tuple[int, int]] = {
    9: (-2, -2), 10: (-1, -2), 11: (0, -2), 12: (1, -2), 13: (2, -2),
    24: (-2, -1), 1: (-1, -1), 2: (0, -1), 3: (1, -1), 14: (2, -1),
    23: (-2, 0), 8: (-1, 0), 4: (1, 0), 15: (2, 0,),
    22: (-2, 1), 7: (-1, 1), 6: (0, 1), 5: (1, 1), 16: (2, 1),
    21: (-2, 2), 20: (-1, 2), 19: (0, 2), 18: (1, 2), 17: (2, 2)
}

neighbor_keys = list(neighbor_dict.keys())


def generate(size: int = 10000) -> Graph:
    size = int(np.sqrt(size) ** 2)
    vertexes = np.arange(1, size + 1).reshape((int(np.sqrt(size)), int(np.sqrt(size)))).tolist()

    graph = Graph()
    graph.oriented = False

    for i in range(len(vertexes)):
        for j in range(len(vertexes)):
            x = (VERTEX_RADIUS * j + SPACE * (j - 1))
            y = (VERTEX_RADIUS * i + SPACE * (i - 1))
            graph.add_vertex(str(vertexes[i][j]), x, y, shadowed=True)

    for i in range(len(vertexes)):
        for j in range(len(vertexes)):
            neighbor = neighbor_keys.copy()
            for k in range(4):
                move = None
                while move is None:
                    choice = random.choice(neighbor)
                    move = neighbor_dict[choice]
                    neighbor.pop(neighbor.index(choice))
                    if i + move[0] < 0 or j + move[1] < 0:
                        move = None
                        continue
                    try:
                        vertexes[i + move[0]][j + move[1]]
                    except IndexError:
                        move = None

                v1 = graph.vertexes_coordinates[str(vertexes[i][j])]
                v2 = graph.vertexes_coordinates[str(vertexes[i + move[0]][j + move[1]])]
                dist = int(np.sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2))

                graph.add_edge(v1.name, v2.name, dist, shadowed=True)

    return graph


def compare_efficiency(widget):
    graph = generate(10000)

    begins = ['5501', '1', '5555', f'{random.randint(1, 10000)}']
    ends = ['5600', '10000', '9955', f'{random.randint(1, 10000)}']

    # begins = [f'{random.randint(1, 10000)}']
    # ends = [f'{random.randint(1, 10000)}']

    # begins = ['1', '1251', '1275', f'{random.randint(1, 2500)}']
    # ends = ['2500', '1300', '2475', f'{random.randint(1, 2500)}']

    # begins = ['1'] #, f'{random.randint(1, 64)}']
    # ends = ['64'] #, f'{random.randint(1, 64)}']
    methods = [algorithm.A_star, algorithm.IDA_star, algorithm.BFS, algorithm.dijkstra]
    # methods = [algorithm.IDA_star]
    # methods = [algorithm.A_star, algorithm.BFS, algorithm.dijkstra]

    widget = QGraphView(widget, graph)
    for method in methods:
        print()
        print(method.__name__)
        for begin, end in zip(begins, ends):
            print(f'From: {begin} to {end}')
            t_start = time.time()
            try:
                method(graph, begin, end)
            except Exception as e:
                print(e)
                continue
            t_end = time.time()
            print(f'Time: {int(t_end - t_start)}')
            print(f'Path({len(graph.path)}): {graph.path}')
            widget.drawGraph(True)
            print(f'C:\\Users\\viktor\\PycharmProjects\\graphs\\{method.__name__}_'
                  f'{int((t_end - t_start) * 1000)}ms_from{begin}to{end}_'
                  f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
            SaveGraph.save_as_image(f'C:\\Users\\viktor\\PycharmProjects\\graphs\\{method.__name__}_'
                                    f'{int((t_end - t_start) * 1000)}ms_from{begin}to{end}_'
                                    f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png', widget.scene)


if __name__ == '__main__':
    pass
