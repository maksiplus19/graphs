from algorithm.additional import additional
from algorithm.isomorphous_graphs import isomorphic
from graph.graph import Graph

def isPlanary(matrix, graph:Graph):
    radius=1 #здесь должен быть радиус
    diametr=1 #здесь должен быть диаметр
    additional_matrix = additional(matrix)
    graph_new = graph.from_matrix(matrix)
    isFull = True
    isPlanary = True
    graph
    for i in range(len(additional_matrix)):
        for j in range(len(additional_matrix[i])):
            if additional_matrix[i][j]!=0:
                isFull= False
                break
    if matrix.size == 5 and isFull:
        isPlanary=False
    elif matrix.size == 6 and radius == 2 and diametr == 2:
        isPlanary = False # еще какое - то условие?

