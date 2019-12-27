from copy import deepcopy
from typing import List, Optional, Tuple, Dict, cast
from algorithm.complex2_from_vector import aggregator

import numpy as np

Triples = List[Tuple[int, int, int]]

def addition_complex2(vector: List[int]):
    complex2 = aggregator(vector)
    cube = deepcopy(complex2['cube'])
    Triples = []
    print(cube)
    for i in range(len(cube)):
        for j in range(len(cube[i])):
            for k in range(len(cube[i][j])):
                cube[i][j][k] = 1 if cube[i][j][k] == 0 else 0
                if cube[i][j][k] == 1 and cube[i][k][j] == 1 and cube[k][i][j] == 1 and cube[k][j][i] == 1 and cube[j][i][k] == 1 and cube[j][k][i] == 1:
                    Triples.append((i+1, j+1, k+1))

    result: Dict = {'triples': complex2['triples'], 'addition_triples': Triples}
    print(cube)
    return result
