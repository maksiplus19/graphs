import json

from graph.graph import Graph
import numpy as np


class SaveGraph:

    @staticmethod
    def save(graph: Graph, file_name: str):
        with open(file_name, "w") as file:
            json.dump(graph.vertexes, file)
            v_c = json.dumps([v.to_dict() for v in graph.vertexes_coordinates.values()])
            file.write(f'|{v_c}')


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
                print(to_dict.items())
                v_from = int(v_from)
                for v_to, to_list in to_dict.items():
                    v_to = int(v_to)
                    for weight in to_list:
                        data = [0]*n
                        data[v_from] = -weight
                        data[v_to] = weight
                        inc_matrix.append(data)
            file.write(str(inc_matrix))

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
            for v_from, to_dict in graph.vertexes.items():
                print(to_dict.items())
                for v_to, to_list in to_dict.items():
                    for weight in to_list:
                        adj_matrix[int(v_from)][int(v_to)] += weight
            file.write(str(adj_matrix))
