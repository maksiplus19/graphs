import json
import random
import numpy as np
from graph.graph import Graph
from graph.vertex import Vertex


class LoadGraph:
    """Статический класс для загрузки графа"""
    @staticmethod
    def __split_file(file_name: str) -> (str, str):
        """Метод принимает на вход имя файла, читает файл, удаляя комментарии. Возврящает две строки до и после '||'"""
        with open(file_name, "r") as file:
            # проходим по файлу построчно и отделяем коментарии, а затем склеиваем обратно
            text = ''.join([line.split('%')[0] for line in file])
        if '||' in text:
            # если есть координаты
            return text.split('||', maxsplit=1)
        else:
            # если координат нет
            return text, None

    @staticmethod
    def load(graph: Graph, file_name: str):
        graph.clear()
        # получаем данные из файла
        vertexes, v_coordinates = LoadGraph.__split_file(file_name)

        # десериализуем вершены-ребра
        graph.vertexes = json.loads(vertexes)
        # устанавливаем счетчик вершин
        graph.set_vertexes_counter(len(graph.vertexes))
        # загружем данные о координатах или генерируем, если их нет
        if v_coordinates is not None:
            v_coordinates = json.loads(v_coordinates)
            for d in v_coordinates:
                graph.vertexes_coordinates[d['name']] = Vertex(d['name'], d['x'], d['y'])
        else:
            for v in graph.vertexes:
                graph.vertexes_coordinates[v] = Vertex(v, random.randint(0, 100), random.randint(0, 100))


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

    def __isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def load_from_adjacency_matrix(graph: Graph, file_name: str):
        matrix1 = []
        with open(file_name, mode='r') as file:
            for line in file:
                data = []
                for weights in line:
                    if LoadGraph.__isfloat(weights):
                        data.append(weights)
                matrix1.append(data)
            matrix1 = [x for x in matrix1 if x != []]
            for i in range(len(matrix1)):
                for j in range(len(matrix1[i])):
                    if matrix[i][j] != '0' and i != []:
                        graph.add_vertex(str(i), random.randint(-50, 100), random.randint(0, 100))
                        graph.add_vertex(str(j), random.randint(-50, 100), random.randint(0, 100))
                        graph.add_edge(str(i), str(j), int(matrix1[i][j]))


    @staticmethod
    def load_from_incidence_matrix(graph: Graph, file_name: str):
        matrix = []
        with open(file_name, mode='r') as file:
            for line in file:
                data = []
                for weights in line:
                    if LoadGraph.__isfloat(weights):
                        data.append(weights)
                matrix.append(data)
            matrix = [x for x in matrix if x != []]
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if matrix[i][j] != '0' and i != []:
                        graph.add_vertex(str(i), random.randint(-50, 100), random.randint(-50, 100))
                        graph.add_vertex(str(j), random.randint(-50, 100), random.randint(0, 100))
                        graph.add_edge(str(i), str(j), int(matrix[i][j]))



    @staticmethod
    def load_from_ribs_list(graph: Graph, file_name: str):
        graph.clear()
        with open(file_name, mode='r') as file:
            for line in file:
                name = ''
                params = []
                for index in line:
                    if index == '{':
                        value = ''
                    if index.isdigit():
                        value += index
                    if index == '(':
                        name = value
                        value = ''
                    if index == ',':
                        params.append(value)
                        value = ''
                    if index == ')':
                        params.append(value)
                        print(params, name)
                        value = ''
                        graph.add_vertex(params[1], random.randint(0, 100), random.randint(0, 100))
                        graph.add_vertex(params[2], random.randint(0, 100), random.randint(0, 100))
                        graph.add_edge(params[1], params[2], int(params[0]))
                        graph.add_edge(params[2], params[1], int(params[0]))
                        graph.oriented = bool(int(params[3]))
                        params = []
        graph.set_vertexes_counter(len(graph.vertexes))

    @staticmethod
    def load_from_arc_list(graph: Graph, file_name: str):
        graph.clear()
        with open(file_name, mode='r') as file:
            for line in file:
                name = ''
                x = ''
                for index in line:
                    if index == '{':
                        value = ''
                    if index.isdigit() or index == '.' or index == '-':
                        value += index
                    if index == ',':
                        x = value
                        value = ''
                    if index == '(':
                        name = value
                        value = ''
                    if index == ')':
                        graph.add_vertex(name, float(x), float(value))
                        value = ''
