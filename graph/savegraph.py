import json

from graph.graph import Graph


class SaveGraph:
    @staticmethod
    def save(graph: Graph, file_name: str):
        with open(file_name, "w") as file:
            json.dump(graph.vertexes, file)

    @staticmethod
    def save_as_adjacency_list(graph: Graph, file_name: str):
        pass

    @staticmethod
    def save_as_adjacency_matrix(graph: Graph, file_name: str):
        pass

    @staticmethod
    def save_as_incidence_matrix(graph: Graph, file_name: str):
        pass

    @staticmethod
    def save_as_arc_list(graph: Graph, file_name: str):
        pass
