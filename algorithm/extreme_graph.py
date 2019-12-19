from typing import List, Tuple, Optional, Dict

import algorithm
from graph.graph import Graph

Base = List[Tuple[str, str]]


def translate_base(s: str) -> Optional[Base]:
    if s[-1] == '\n':
        s = s[:-1]
    s = s.split(sep='\n')

    # проеврека на существование пробелов
    if not all([el.count(' ') for el in s]):
        return None
    base = []
    for el in s:
        el = el.split(' ')
        # проверка на 2 элемента, что эти элементы являются числами и что левый меньше правого
        if len(el) != 2 or not el[0].isdigit() or not el[1].isdigit() or int(el[0]) >= int(el[1]):
            return None
        else:
            base.append((el[0], el[1]))
    return base


def add_base_part(m, base_part):
    for i in range(len(base_part)):
        for j in range(len(base_part[i])):
            m[i][j] = 1
            m[j][i] = 1


def get_matrix_from_base(base: Base, size: int) -> List[List[int]]:
    m = [[0] * size for i in range(size)]
    for base_el in base:
        base_part = [[1] * int(base_el[1]) for i in range(int(base_el[0]))]
        add_base_part(m, base_part)
    return m


def get_max(base: Base) -> int:
    base = [(int(el[0]), int(el[1])) for el in base]
    l = []
    for el in base:
        l.extend(el)
    return max(l)


def extreme(base1: str, base2: str) -> Optional[Dict[str, Graph]]:
    base1, base2 = translate_base(base1), translate_base(base2)
    if base1 is None or base2 is None:
        return None
    size, size2 = get_max(base1), get_max(base2)
    if size != size2:
        return None
    m1 = get_matrix_from_base(base1, size)
    m2 = get_matrix_from_base(base2, size)

    res = {
        'add1': Graph.from_matrix(algorithm.additional(m1)),
        'add2': Graph.from_matrix(algorithm.additional(m2)),
        'union': Graph.from_matrix(algorithm.binary_operation_with_matrix(m1, m2, 'or')),
        'and': Graph.from_matrix(algorithm.binary_operation_with_matrix(m1, m2, 'and')),
        'aminusb': Graph.from_matrix(algorithm.binary_operation_with_matrix(m1, m2, 'minus')),
        'bminusa': Graph.from_matrix(algorithm.binary_operation_with_matrix(m2, m1, 'minus')),
    }

    for name, graph in res.items():
        print(name)
        print('Рёбра')
        degree = {str(i): 0 for i in range(1, graph.size() + 1)}
        for v_from, to_dict in graph.vertexes.items():
            for v_to, to_list in graph.vertexes[v_from].items():
                print(f'"{v_from}" -> "{v_to}" ({to_list[0][0]})')
                degree[v_from] += 1
        print('Вектор степеней')
        print([d for d in degree.values()])

        matrix = graph.to_matrix()
        base = []
        if algorithm.complex2_from_vector.check_extreme_2d(matrix):
            for i in range(len(matrix) // 2):
                for j in range(i + 1, len(matrix)):
                    if i == j or not matrix[i][j]:
                        continue
                    if (j == len(matrix) - 1 and not matrix[i + 1][j]) \
                            or (j < len(matrix) - 1 and matrix[i][j] and not matrix[i][j + 1] and not matrix[i + 1][j]):
                        base.append((i + 1, j + 1))
        print('База')
        print(base)
        print()

    return res
