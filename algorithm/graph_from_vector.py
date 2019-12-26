from typing import List, Dict, Any, Optional

from algorithm.complex2_from_vector import check_extreme_2d


def last_not_zero(vector: List[int]) -> Optional[int]:
    for i, degree in enumerate(reversed(vector)):
        if degree:
            return len(vector) - i - 1
    return None


def get_max(vector: List[int], delta: int, index: int) -> List[int]:
    res = []
    for _ in range(delta):
        m = max(vector[index + 1:])
        i = len(vector) - vector[::-1].index(m) - 1
        res.append(i)
        vector[i] = 0
    return res


def restore_from_vector(vector: List[int]) -> Dict[str, Any]:
    index = 0
    edges = []
    res: Dict[str, Any] = {'complete': True}

    print(vector)
    while vector[index]:
        last = last_not_zero(vector)
        delta = min(vector[index], len(vector[index + 1:last + 1]))
        if delta != len(vector[index + 1:last + 1]):
            res['complete'] = False

        for i in get_max(vector.copy(), delta, index):
            vector[i] -= 1
            edges.append((str(index + 1), str(i + 1)))

        vector[index] -= delta

        print(vector)

        if not vector[index]:
            index += 1

    if len(edges):
        res['edges'] = edges

    matrix = [[0] * len(vector) for _ in range(len(vector))]
    for l, r in edges:
        l = int(l) - 1
        r = int(r) - 1
        matrix[l][r] = 1
        matrix[r][l] = 1

    res['extreme'] = check_extreme_2d(matrix)
    if res['extreme']:
        base = []
        for i in range(len(matrix) // 2):
            for j in range(i + 1, len(matrix)):
                if i == j or not matrix[i][j]:
                    continue
                if (j == len(matrix) - 1 and not matrix[i + 1][j]) \
                        or (j < len(matrix) - 1 and matrix[i][j] and not matrix[i][j + 1] and not matrix[i + 1][j]):
                    base.append((i + 1, j + 1))
        res['base'] = base

    return res


if __name__ == '__main__':
    # v = [6, 4, 4, 3, 3, 2, 2]
    v = [6, 4, 4, 3, 3, 1, 1]
    print(restore_from_vector(v))
