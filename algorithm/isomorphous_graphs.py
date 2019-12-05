from typing import List, Optional, Union

import numpy as np

from graph.graph import Graph


def __get_rib_vector(graph: Graph) -> List[int]:
    return list([len(value) if value is not None else 0 for key, value in sorted(graph.vertexes.items(),
                                                                                 key=lambda el: el[0])])


def __get_weight_vector(graph: Graph) -> List[int]:
    res = []
    for v_from, to_dict in graph.vertexes.items():
        s = 0
        for v_to, to_list in to_dict.items():
            s += sum([el[0] for el in to_list])
        res.append(s)
    return sorted(res)


def backtrack(first_matrix: List, second_matrix: List, p_matrix: List, k: int):
    if k > len(second_matrix):
        return p_matrix

    for i in range(len(first_matrix)):
        for j in range(len(p_matrix)):
            p_matrix[k-1][j] = 0
        p_matrix[k-1][i] = 1

        a = cut(second_matrix, k, k)
        b = np.dot(np.dot(cut(p_matrix, k, len(p_matrix)), first_matrix), np.transpose(cut(p_matrix, k, len(p_matrix))))
        b = list([list(el) for el in b])

        if a == b:
            res = backtrack(first_matrix, second_matrix, p_matrix.copy(), k + 1)
            if res is not None:
                return res
    return


def isomorphic(first: Graph, second: Graph) -> str:
    first_vector, second_vector = __get_rib_vector(first), __get_rib_vector(second)

    if len(first_vector) != len(second_vector):
        return 'Сильная неизоморфность\nВектора степеней не равны'

    first_vector.sort()
    second_vector.sort()
    if first_vector != second_vector:
        return f'Сильная неизоморфность\nВектора степеней не равны\n{first_vector}\n{second_vector}'

    first_vector, second_vector = __get_weight_vector(first), __get_weight_vector(second)

    if len(first_vector) != len(second_vector):
        return 'Сильная неизоморфность\nВектора степеней не равны'

    first_vector.sort()
    second_vector.sort()
    if first_vector != second_vector:
        return f'Сильная неизоморфность\nВектора степеней не равны\n{first_vector}\n{second_vector}'

    first_matrix = first.to_matrix(with_weight=True)
    second_matrix = second.to_matrix(with_weight=True)

    size = first.size()
    p = [[0 for i in range(size)] for i in range(size)]
    if backtrack(first_matrix, second_matrix, p, 1) is not None:
        return 'Графы изоморфны'
    else:
        return 'Графы не изоморфны'


def cut(matrix: Union[List, np.array], k, m) -> List:
    size = len(matrix)
    res = [[0 for i in range(size)] for i in range(size)]
    for i in range(k):
        for j in range(m):
            res[i][j] = matrix[i][j]
    return res
