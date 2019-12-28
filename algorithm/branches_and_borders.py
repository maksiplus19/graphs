# -*- coding: utf-8 -*-
import math
from copy import deepcopy
from typing import List, Tuple, cast, Union

import numpy as np

from graph.graph import Graph
from path_find import __cost


def get_row_min(matrix: List[List[int]], i: int) -> int:
    return min(matrix[i])


def get_column_min(matrix: List[List[int]], i: int) -> int:
    return min(matrix[j][i] for j in range(len(matrix)))


def get_eval(matrix: List[List[int]], row_index: int, column_index: int) -> int:
    row = [matrix[row_index][j] for j in range(len(matrix[row_index]))
           if matrix[row_index][j] and j != column_index]
    if not row or min(row) == math.inf:
        row = [0]

    column = [matrix[i][column_index] for i in range(len(matrix)) if matrix[i][column_index] and i != row_index]
    if not column or min(column) == math.inf:
        column = [0]

    return min(row) + min(column)


def salesman(graph: Graph):
    def get_weight(first: int, second: int):
        if first == second:
            return math.inf
        return int(__cost(graph, str(first + 1), str(second + 1)))

    size = graph.size()
    graph.vertexes = {str(i + 1): {} for i in range(graph.size())}

    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i, size):
            w = get_weight(i, j)
            matrix[i][j] = w
            matrix[j][i] = w
    copy_matrix = deepcopy(matrix)

    print(np.array(matrix))
    path: List[Tuple[int, int]] = []

    r_indexes = {i: i for i in range(size)}
    c_indexes = {i: i for i in range(size)}

    while len(path) != len(copy_matrix) and matrix:
        print(np.array(matrix))
        size = len(matrix)
        rows = [get_row_min(matrix, i) for i in range(size)]

        if math.inf not in rows:
            for i in range(size):
                matrix[i] = list(map(lambda el: el - rows[i], matrix[i]))

        columns = [get_column_min(matrix, i) for i in range(size)]
        if math.inf not in columns:
            for line in matrix:
                for i in range(size):
                    line[i] -= columns[i]

        eval_matrix = [[0] * size for _ in range(size)]
        print(np.array(matrix))

        for i in range(size):
            for j in range(size):
                if not matrix[i][j]:
                    eval_matrix[i][j] = get_eval(matrix, i, j)

        print(set(sum(eval_matrix, [])), {0, math.inf}, set(sum(eval_matrix, [])) == {0, math.inf})
        if set(sum(eval_matrix, [])) == {0}:
            eval_matrix = cast(List[Union[int, float]], eval_matrix)
            c = sum(eval_matrix, []).count(math.inf)

            if c == 0:
                path.append((r_indexes[0] + 1, c_indexes[1] + 1))
            elif c == 1:
                if matrix[0][1] or matrix[1][0] == math.inf:
                    path.append((r_indexes[0] + 1, c_indexes[0] + 1))
                    path.append((r_indexes[1] + 1, c_indexes[1] + 1))
                else:
                    path.append((r_indexes[0] + 1, c_indexes[1] + 1))
                    path.append((r_indexes[1] + 1, c_indexes[0] + 1))
                break
            elif c == 2:
                print('here')
                break
                # if get_column_min(matrix, 0) == math.inf or get_column_min(matrix, 1) == math.inf:

        max_i, max_j, maximum = 0, 0, 0
        for i in range(len(eval_matrix)):
            for j in range(len(eval_matrix)):
                if eval_matrix[i][j] >= maximum:
                    maximum = eval_matrix[i][j]
                    max_i = i
                    max_j = j

        path.append((r_indexes[max_i] + 1, c_indexes[max_j] + 1))
        matrix[max_j][max_i] = math.inf

        matrix.pop(max_i)
        for line in matrix:
            line.pop(max_j)

        for i in r_indexes:
            if i >= max_i:
                r_indexes[i] += 1
        for i in c_indexes:
            if i >= max_j:
                c_indexes[i] += 1
    p = [p[0] for p in path]

    graph.oriented = False
    # v = [v for v in graph.vertexes_coordinates]
    for i in range(len(p)):
        graph.add_edge(str(p[i-1]), str(p[i]), copy_matrix[p[i - 1] - 1][p[i] - 1])


if __name__ == '__main__':
    g = Graph()
    [g.add_vertex(f'{i + 1}') for i in range(4)]
    salesman(g)
