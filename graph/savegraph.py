import json

from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtWidgets import QGraphicsScene

from graph.graph import Graph
import numpy as np


class SaveGraph:
    @staticmethod
    def save(graph: Graph, file_name: str):
        with open(file_name, "w") as file:
            graph_dict = {'vertexes': graph.vertexes}
            coordinates = [v.to_dict() for v in graph.vertexes_coordinates.values()]
            graph_dict['coordinates'] = coordinates
            graph_dict['oriented'] = graph.oriented
            graph_dict['weighted'] = graph.weighted
            json.dump(graph_dict, file)

    @staticmethod
    def save_as_vertexes_list(graph: Graph, file_name: str):
        with open(file_name, "w") as file:
            vertexes = 'Vertex{'
            for key in sorted(graph.vertexes_coordinates):
                vertexes += key + '(' + str(graph.vertexes_coordinates[key].x) + ',' +\
                                 str(graph.vertexes_coordinates[key].y) + ')|'
            vertexes = vertexes[:-1]
            vertexes += '}'
            file.write(vertexes)

    @staticmethod
    def save_as_incidence_matrix(graph: Graph, file_name: str):
        with open(file_name, "w") as file:
            inc_matrix = []
            n = len(graph.vertexes_coordinates)
            for v_from, to_dict in graph.vertexes.items():
                v_from = int(v_from)
                for v_to, to_list in to_dict.items():
                    v_to = int(v_to)
                    for weight in to_list:
                        data = [0.]*n
                        data[v_from] = -weight
                        data[v_to] = weight
                        inv_data = [inv_data * -1 for inv_data in data]
                        if inv_data in inc_matrix:
                            for i in data:
                                if i < 0:
                                    data[data.index(i)] = i*-1
                            inc_matrix[inc_matrix.index(inv_data)] = data
                        else:
                            inc_matrix.append(data)
            file.write(str(np.matrix(inc_matrix)))

    @staticmethod
    def save_as_ribs_list(graph: Graph, file_name: str):
        with open(file_name, "w") as file:
            ribs = 'Edges{'
            count = 0
            oriented = int(graph.oriented)
            for v_from, to_dict in graph.vertexes.items():
                if not to_dict:
                    continue
                for v_to, to_list in to_dict.items():
                    for weight in to_list:
                        count += 1
                        ribs += f'{count} ({weight}, {v_from}, {v_to}, {oriented})|'
            if ribs[len(ribs)-1] != '{':
                ribs = ribs[:-1]
            ribs += '}'
            file.write(ribs)

    @staticmethod
    def save_as_adjacency_matrix(graph: Graph, file_name: str):
        with open(file_name, "w") as file:
            n = len(graph.vertexes_coordinates)
            adj_matrix = np.zeros((n, n))
            print(graph.vertexes.items())
            for v_from, to_dict in graph.vertexes.items():
                for v_to, to_list in to_dict.items():
                    for weight in to_list:
                        adj_matrix[int(v_from) - 1][int(v_to) - 1] += weight
                        # if graph.oriented:
                        #     adj_matrix[int(v_from)-1][int(v_to)-1] += weight
                        #     # adj_matrix[int(v_to)-1][int(v_from)-1] += weight
                        # else:
                        #     adj_matrix[int(v_from) - 1][int(v_to) - 1] += weight/2
                        #     adj_matrix[int(v_to) - 1][int(v_from) - 1] += weight/2
            file.write(str(adj_matrix))

    @staticmethod
    def save_as_image(file_name: str, scene: QGraphicsScene):
        image = QImage(scene.width(), scene.height(), QImage.Format_ARGB32_Premultiplied)
        image.fill(QColor(255, 255, 255).toRgb())
        painter = QPainter(image)
        scene.render(painter)
        painter.end()
        image.save(file_name)
