from algorithm.additional import additional
from algorithm.isomorphous_graphs import isomorphic
from graph.graph import Graph
import boost_py as boost

from ui.sourse.graphicsedge import GraphicsEdge
import networkx as nx


def isPlanary(graph:Graph):

    for v1_from in graph.vertexes:
        x1_from = graph.vertexes_coordinates[v1_from].x
        y1_from = graph.vertexes_coordinates[v1_from].y
        for v1_to in graph.vertexes[v1_from]:
            x1_to = graph.vertexes_coordinates[v1_to].x
            y1_to = graph.vertexes_coordinates[v1_to].y
            x1_node = graph.vertexes[v1_from][v1_to][0][1].x
            y1_node = graph.vertexes[v1_from][v1_to][0][1].y
            for v2_from in graph.vertexes:
                x2_from = graph.vertexes_coordinates[v2_from].x
                y2_from = graph.vertexes_coordinates[v2_from].y
                for v2_to in graph.vertexes[v2_from]:
                    x2_to = graph.vertexes_coordinates[v2_to].x
                    y2_to = graph.vertexes_coordinates[v2_to].y
                    x2_node = graph.vertexes[v2_from][v2_to][0][1].x
                    y2_node = graph.vertexes[v2_from][v2_to][0][1].y
                    if x1_to == x2_to and x1_from == x2_from and y1_to == y2_to and y1_from == y2_from:
                        break

                    a1_from = y1_from - y1_node
                    b1_from = x1_from - x1_node
                    c1_from = x1_from * y1_node - x1_node * y1_from

                    a1_to = y1_node - y1_to
                    b1_to = x1_node - x1_to
                    c1_to = x1_node * y1_to - x1_to * y1_node

                    a2_from = y2_from - y2_node
                    b2_from = x2_from - x2_node
                    c2_from = x2_from * y2_node - x2_node * y2_from

                    a2_to = y2_node - y2_to
                    b2_to = x2_node - x2_to
                    c2_to = x2_node * y2_to - x2_to * y2_node

                    det1 = a1_from * b2_from - a2_from * b1_from
                    det2 = a1_from * b2_to - a2_to * b1_from
                    det3 = a1_to * b2_from - a2_from * b1_to
                    det4 = a1_to * b2_to - a2_to * b1_to

                    x1 = (b1_from * c2_from - b2_from * c1_from) / det1
                    y1 = (a2_from * c1_from - a1_from * c2_from) / det1

                    x2 = (b1_from * c2_to - b2_to * c1_from) / det2
                    y2 = (a2_to * c1_from - a1_from * c2_to) / det2

                    x3 = (b1_to * c2_from - b2_from * c1_to) / det3
                    y3 = (a2_from * c1_to - a1_to * c2_from) / det3

                    x4 = (b1_to * c2_to - b2_to * c1_to) / det4
                    y4 = (a2_to * c1_to - a1_to * c2_to) / det4

                    print(x1, y1)
                    print(x2, y2)
                    print(x3, y3)
                    print(x4, y4)

    g = nx.Graph()
    nx.Graph()
    size = graph.size()
    matr = graph.to_matrix()
    for i in range(1, size+1):
        g.add_node(i)
        for j in range(1, size+1):
            if matr[i-1][j-1] is not 0:
                g.add_edge(i, j)

    print(nx.check_planarity(g))

