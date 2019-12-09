def additional(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0 or i == j:
                matrix[i][j] = 0
            elif matrix[i][j] == 0:
                matrix[i][j] = 1
    return matrix
