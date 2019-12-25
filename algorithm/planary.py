from algorithm.additional import additional
from algorithm.isomorphous_graphs import isomorphic
from graph.graph import Graph
import boost
from ui.sourse.graphicsedge import GraphicsEdge


def isPlanary(matrix, graph:Graph):
    for v1_from in graph.vertexes:
        x1_from = graph.vertexes_coordinates[v1_from].x
        y1_from = graph.vertexes_coordinates[v1_from].y
        for v1_to in graph.vertexes[v1_from]:
            x1_to = graph.vertexes_coordinates[v1_to].x
            y1_to = graph.vertexes_coordinates[v1_to].y
            for v2_from in graph.vertexes:
                x2_from = graph.vertexes_coordinates[v2_from].x
                y2_from = graph.vertexes_coordinates[v2_from].y
                for v2_to in graph.vertexes[v2_from]:
                    x2_to = graph.vertexes_coordinates[v2_to].x
                    y2_to = graph.vertexes_coordinates[v2_to].y
                    node = graph.


    boost.boyer_myrvold_planarity_test()
