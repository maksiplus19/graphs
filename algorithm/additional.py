from typing import List


def additional(matrix: List[List[int]]) -> List[List[int]]:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i != j:
                matrix[i][j] = int(not matrix[i][j])
    return matrix
