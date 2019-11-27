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
        # vertexes, v_coordinates = LoadGraph.__split_file(file_name)
        with open(file_name, 'r') as file:
            data = json.load(file)
            try:
                graph.vertexes = data['vertexes']
            except KeyError:
                return False
            # загружем данные о координатах или генерируем, если их нет
            if 'coordinates' in data:
                coordinates = data['coordinates']
                for d in coordinates:
                    graph.vertexes_coordinates[d['name']] = Vertex(d['name'], d['x'], d['y'])
            else:
                for v in graph.vertexes:
                    graph.vertexes_coordinates[v] = Vertex(v, random.randint(0, 100), random.randint(0, 100))
            if 'oriented' in data:
                graph.oriented = data['oriented']
            if 'weighted' in data:
                graph.weighted = data['weighted']
            if 'path' in data:
                graph.path = data['path']
        graph.update()
        return True

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
                    if matrix1[i][j] != '0' and i != []:
                        graph.add_vertex(str(i+1), random.randint(-50, 100), random.randint(0, 100))
                        graph.add_vertex(str(j+1), random.randint(-50, 100), random.randint(0, 100))
                        graph.add_edge(str(i+1), str(j+1), int(matrix1[i][j]))

    @staticmethod
    def load_from_incidence_matrix(graph: Graph, file_name: str):
        matrix = []
        with open(file_name, mode='r') as file:
            data = file.read()
            data = data.replace('.', ',')
            data = data.replace(',]', ']')
            data = data.replace('\n', ',')
            matrix = json.loads(data)
            for line in matrix:
                for i in range(len(line)):
                    if line[i] < 0:
                        v_from = i + 1
                        break
                for i in range(len(line)):
                    if line[i] > 0:
                        v_to = i + 1
                        break
                graph.add_vertex(str(v_from))
                graph.add_vertex(str(v_to))
                graph.add_edge(str(v_from), str(v_to), v_to)

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
                        graph.add_edge(params[2], params[1], int(params[0]))
                        graph.oriented = bool(int(params[3]))
                        params = []

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
