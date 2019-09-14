import json
from graph.graph import Graph

class LoadGraph:
    """Статический класс для загрузки графа"""

    @staticmethod
    def load(graph: Graph, file_name: str):
        with open(file_name, "r") as file:
            graph.vertexes = json.load(file)

    @staticmethod
    def load_from_adjacency_list(graph: Graph, file_name: str):
        # # сбрасываем старую матрицу
        # graph.vertexes = {}
        # # максимальный номер вершины, чтобы позже выровнять матрицу до этого размера
        # max_vertex_num = 0
        # with open(file_name, mode='r') as file:
        #     # построчное чтение файла
        #     for line in file:
        #         # убираем комментарии
        #         line = line.split('%', maxsplit=2)[0]
        #         # разделяем строку на номера вершин
        #         vertices = line.split(' ')
        #         if len(vertices) % 2 == 0:
        #             raise Exception('Wrong file content')
        #         if len(vertices) == 0:
        #             continue
        #         if len(vertices) == 1:
        #             self.adjacency_matrix.append([])
        #         # сохраняем первую вершину и преобразуем вершины с весами в числа
        #         try:
        #             vertices = [int(v) for v in vertices]
        #         except ValueError:
        #             self.adjacency_matrix = []
        #             return
        #         v = vertices[0]
        #         # self.adjacency_matrix.append([])
        #         if v > max_vertex_num:
        #             for i in range(v - max_vertex_num + 1):
        #                 self.adjacency_matrix.append([])
        #             max_vertex_num = v
        #         if len(self.adjacency_matrix[v]) < v:
        #             self.adjacency_matrix[v].extend([math.inf] * (v - len(self.adjacency_matrix[v]) + 1))
        #         # добавляем смежные вершины
        #         for i in range(1, len(vertices), 2):
        #             # сохраняем максимальный номер вершины
        #             if vertices[i] > max_vertex_num:
        #                 max_vertex_num = vertices[i]
        #
        #             # добовляем пустые элементы если размер меньше, чем максимальный номер вершины
        #             while len(self.adjacency_matrix) - 1 < max_vertex_num:
        #                 self.adjacency_matrix.append([])
        #             while len(self.adjacency_matrix[v]) - 1 < max_vertex_num:
        #                 self.adjacency_matrix[v].append(math.inf)
        #
        #             # сохраняем веса в матрицу
        #             self.adjacency_matrix[v][vertices[i]] = vertices[i + 1]
        #
        # while len(self.adjacency_matrix) - 1 < max_vertex_num:
        #     self.adjacency_matrix.append([])
        # for i in range(len(self.adjacency_matrix)):
        #     if len(self.adjacency_matrix[i]) - 1 < max_vertex_num:
        #         self.adjacency_matrix[i].extend([math.inf] * (max_vertex_num - len(self.adjacency_matrix[i]) + 1))
        pass

    @staticmethod
    def load_from_adjacency_matrix(graph: Graph, file_name: str):
        matrix = []
        with open(file_name, mode='r') as file:
            for line in file:
                # разделяем строку на веса по пробелу
                weights = line.split(' ')
                # преобразуем строки в числа и сразу добавляем в матрицу
                matrix.append([int(w) for w in weights])
        # далее надо сохранить информацию из матрицы в словарь

    @staticmethod
    def load_from_incidence_matrix(graph: Graph, filr_name: str):
        pass

    @staticmethod
    def load_from_arc_list(graph: Graph, file_name: str):
        pass
