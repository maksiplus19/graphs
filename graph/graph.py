from copy import copy

from graph.vertex import Vertex


class Graph:
    ADD_VERTEX = 1
    ADD_EDGE = 2
    DEL_VERTEX = 3
    DEL_EDGE = 4
    MOVE_VERTEX = 5
    HISTORY_REC_NUM = 10
    """Класс графа"""
    def __init__(self):
        # Граф хранится в виде словаря.
        # Каждой вершине соответсвуеет словарь вершин,
        # до которых есть дуги и список их весов
        # vertexes = dict(name, dict(name, list))
        self.vertexes = {}
        # vertexes_coordinates = dict(name, Vertex)
        self.vertexes_coordinates = {}
        self.__history = []
        self.__history_num = 0

    def add_edge(self, v_from: str, v_to: str, weight: int = 1):
        if self.vertexes.get(v_from) is not None and self.vertexes.get(v_to) is not None:
            self.vertexes[v_from][v_to].append(weight)
            self.vertexes[v_from][v_to].sort()
        else:
            raise Exception('No vertex for adding edge')

    def add_vertex(self, name: str, x: int, y: int):
        if self.vertexes_coordinates.get(name) is None:
            self.vertexes_coordinates[name] = Vertex(name, x, y)
            self.vertexes[name] = {}

    def del_edge(self, v_from: str, v_to: str, weight: int):
        if self.vertexes.get(v_from) is not None and self.vertexes.get(v_to) is not None:
            arr = self.vertexes[v_from][v_to]
            arr.pop(arr.index(weight))

    def del_vertex(self, name: str):
        if self.vertexes_coordinates.get(name):
            self.vertexes_coordinates.pop(name)
            self.vertexes.pop(name)
            for item in self.vertexes.values():
                if name in item:
                    item.pop(name)

    def clear(self):
        self.vertexes.clear()
        self.vertexes_coordinates.clear()

    def undo(self):
        if self.__history_num == 0:
            return

        act_list = self.__history[self.__history_num]

        if self.ADD_EDGE == act_list[0]:
            self.del_edge(act_list[1], act_list[2], act_list[3])
        elif self.ADD_VERTEX == act_list[0]:
            self.del_vertex(act_list[1])
        elif self.DEL_EDGE == act_list[0]:
            self.add_edge(act_list[1], act_list[2], act_list[3])
        elif self.DEL_VERTEX == act_list[0]:
            # [action_code, vertex_name, x, y, copy(vertex_row), copy(related_vertex)]
            self.vertexes_coordinates[act_list[1]] = Vertex(act_list[1], act_list[2], act_list[3])
            self.vertexes[act_list[1]] = copy(act_list[4])
            for v_name, w_list in act_list[5].items():
                self.vertexes[v_name][act_list[1]] = copy(w_list)

        self.__history_num -= 1

    def next(self):
        pass

    def save_action(self, action_code: int, vertex_name: str = None, following_vertex_name: str = None,
                    weight: int = None, x: int = None, y: int = None, vertex_row: dict = None,
                    related_vertex: dict = None):
        """
            СОХРАНЯТЬ ДО ИЗМЕНЕНИЯ ОБЪЕКТОВ

            Метод пердназначен для сохранения действий на графом
            action_code - код выполненой операции каждой операции требуютя свои аргументы

            ADD_VERTEX нужно только имя вершины (vertex_name)

            ADD_EDGE нужны начальная вершина (vertex_name) и имя конечной вершины(following_vertex_name),
            а также вес ребра (weight)

            DEL_EDGE нужны начальная вершина (vertex_name) и имя конечной вершины(following_vertex_name),
            а также вес ребра (weight)

            DEL_VERTEX нужны имя удаляемой вершины (vertex_name), строка и словаря вершин (vertex_row),
            координаты вершины (x, y), а также словарь от каких вершин шли ребра к удаляемой (related_vertex:
            dict = {name, list}, где name это имя вершины от которой идут ребра, а list список весов этих ребер
        """
        # если был возврат, то нужно удалить последующие действия
        while len(self.__history) > self.__history_num:
            self.__history.pop()

        if self.ADD_VERTEX == action_code:
            if vertex_name is None or x is None or y is None:
                raise Exception('ADD_VERTEX error. Some of arguments are None')
            self.__history.append([action_code, x, y])

        elif self.ADD_EDGE == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None:
                raise Exception('ADD_EDGE error. Some of arguments are None')
            self.__history.append([action_code, vertex_name, following_vertex_name, weight])

        elif self.DEL_EDGE == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None:
                raise Exception('DEL_EDGE error. Some of arguments are None')
            self.__history.append([action_code, vertex_name, following_vertex_name, weight])

        elif self.DEL_VERTEX == action_code:
            if vertex_name is None or x is None or y is None or vertex_row is None or related_vertex is None:
                raise Exception('DEL_VERTEX error. Some of arguments are None')
            self.__history.append([action_code, vertex_name, x, y, copy(vertex_row), copy(related_vertex)])

        self.__history_num += 1
        if len(self.__history) > self.HISTORY_REC_NUM:
            self.__history.pop(0)
