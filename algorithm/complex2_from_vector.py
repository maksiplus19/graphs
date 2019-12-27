from copy import deepcopy
from typing import List, Optional, Tuple, Dict, cast

import numpy as np

Triples = List[Tuple[int, int, int]]


def get_unmarked(marks: Dict[int, bool]) -> int:
    for i, mark in marks.items():
        if not mark:
            return i
    raise IndexError('No unmarked vertexes')


def find_zero_index(vector: List[int]) -> int:
    for i, d in enumerate(reversed(vector)):
        if d:
            return len(vector) - i
    return 0


def get_2complex_from_vector(vector: List[int]) -> Optional[Dict]:
    if not len(vector):
        return None
    if sum(vector) % 3:
        return None

    vertexes = sorted([(i, vector[i]) for i in range(len(vector))], key=lambda el: el[1], reverse=True)
    vertexes = [i for i, _ in vertexes]
    vector.sort(reverse=True)
    marks = {i: False for i in range(len(vector))}
    res: Dict = {}
    index = 0
    for i, degree in enumerate(vector):
        if degree:
            index = i
            break

    marks[index] = True
    res['triples']: Triples = []
    res['complete'] = True

    print(vector)

    while vector[index]:
        try:
            second_vertex = get_unmarked(marks)
        except IndexError as e:
            print(e)
            return None
        zero = find_zero_index(vector)
        delta = min(vector[index], vector[second_vertex], len(vector[second_vertex + 1:zero]))

        if delta < len(vector[second_vertex + 1:zero]):
            res['complete'] = False

        for i in range(zero - delta, zero):
            res['triples'].append((vertexes[index] + 1, vertexes[second_vertex] + 1, vertexes[i] + 1))
            vector[i] -= 1
        vector[index] -= delta
        vector[second_vertex] -= delta

        marks[second_vertex] = True

        if not vector[index] and index < len(vector):
            index = 0
            for i, degree in enumerate(vector):
                if degree:
                    index = i
                    break
            marks = {i: False for i in range(len(vector))}
            for i in range(index + 1):
                marks[i] = True
        print(vector)
    return res


def check_extreme_2complex(triples: Triples) -> Optional[bool]:
    if not len(triples):
        return None

    t = []
    for el in triples:
        t.extend(el)
    size = max(t)

    cube: np.array = np.zeros((size, size, size), dtype=int)
    for el in triples:
        a = el[0] - 1
        b = el[1] - 1
        c = el[2] - 1
        cube[a][b][c] = 1
        cube[a][c][b] = 1
        cube[b][a][c] = 1
        cube[b][c][a] = 1
        cube[c][a][b] = 1
        cube[c][b][a] = 1
    matr = deepcopy(cube)
    cube = cast(list, cube.tolist())

    for i in range(size):
        for j in range(size):
            cube[i][j].pop(i)
    for i in range(size):
        cube[i].pop(i)

    extreme = True
    for i in range(len(cube)):
        extreme &= check_extreme_2d(cube[i])

    return extreme, matr


def get_2complex_base(triples: Triples) -> Triples:
    base: Triples = []
    less = lambda a, b: all(a[j] <= b[j] for j in range(len(a)))
    triples = deepcopy(triples)
    m = triples.pop()
    base.append(m)
    while triples:
        simplex = triples.pop()
        if not less(simplex, m):
            base.append(simplex)
            m = simplex
    base.reverse()
    return base


def check_line(line: List[int]) -> bool:
    return all(line[:find_zero_index(line)])


def get_diag_size(matrix: List[List[int]]) -> int:
    for i, line in enumerate(matrix):
        line = line.copy()
        line[i] = 1
        if 0 in line and line.index(0) != find_zero_index(line):
            return i
    return len(matrix)


def check_extreme_2d(matrix: List[List[int]]) -> bool:
    matrix = deepcopy(matrix)
    for i in range(get_diag_size(matrix)):
        matrix[i][i] = 1

    extreme = True
    for i in range(len(matrix)):
        extreme &= check_line(matrix[i])

    return extreme


def aggregator(vector: List[int]) -> Optional[Dict]:
    result = get_2complex_from_vector(vector)
    if result is None:
        return None
    extreme_and_cube = check_extreme_2complex(result['triples'])
    result['extreme'] = extreme_and_cube[0]
    result['cube'] = extreme_and_cube[1]
    if result['extreme']:
        result['base'] = get_2complex_base(result['triples'])
    return result


if __name__ == '__main__':
    # v = [11, 10, 9, 8, 6, 5, 2]
    # v = [3, 3, 2, 2, 2]
    v = [1, 2, 2, 1]
    d = aggregator(v)
    print(d)
