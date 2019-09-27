from copy import copy

from graph.vertex import Vertex


class Graph:
    ADD_VERTEX = 1
    ADD_EDGE = 2
    DEL_VERTEX = 3
    DEL_EDGE = 4
    MOVE_VERTEX = 5
    GRAPH_CLEAR = 6
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
        self.oriented = False
        self.__vertex_counter = 0
        self.__history = []
        self.__history_counter = 0

    def add_edge(self, v_from: str, v_to: str, weight: int = 1, save: bool = True):
        if self.vertexes.get(v_from) is not None and self.vertexes.get(v_to) is not None:
            if save:
                # данное условие необходимо для того, что не было повторного сохранения при откате
                # или повторении действия, т.к. оно уже сохранено
                self.save_action(self.ADD_EDGE, vertex_name=v_from, following_vertex_name=v_to, weight=weight)

            # если еще список ребер еще не создан, то создаем его
            if self.vertexes[v_from].get(v_to) is None:
                self.vertexes[v_from][v_to] = []
            # добавляем ребро
            self.vertexes[v_from][v_to].append(weight)
            # сортируем, чтобы ребро с меньшим весом было первым
            self.vertexes[v_from][v_to].sort()
        else:
            raise Exception('No vertex for adding edge')

    def add_vertex(self, name: str, x: int, y: int, save: bool = True):
        if self.vertexes_coordinates.get(name) is None:
            if save:
                # данное условие необходимо для того, что не было повторного сохранения при откате
                # или повторении действия, т.к. оно уже сохранено
                self.save_action(self.ADD_VERTEX, vertex_name=name, x=x, y=y)

            self.vertexes_coordinates[name] = Vertex(name, x, y)
            self.vertexes[name] = {}

    def del_edge(self, v_from: str, v_to: str, weight: int, save: bool = True):
        if self.vertexes.get(v_from) is not None and self.vertexes.get(v_to) is not None:
            if save:
                # данное условие необходимо для того, что не было повторного сохранения при откате
                # или повторении действия, т.к. оно уже сохранено
                self.save_action(self.DEL_EDGE, vertex_name=v_from, following_vertex_name=v_to, weight=weight)

            arr = self.vertexes[v_from][v_to]
            arr.pop(arr.index(weight))

    def del_vertex(self, name: str, save: bool = True):
        if self.vertexes_coordinates.get(name):
            if save:
                # данное условие необходимо для того, что не было повторного сохранения при откате
                # или повторении действия, т.к. оно уже сохранено
                v = self.vertexes_coordinates[name]
                related_vertex = {}
                # сохраняем все ребра, которые идут в удаляемую вершину
                for v_from, adjacency_dict in self.vertexes.items():
                    if adjacency_dict.get(name) is not None:
                        related_vertex[v_from] = adjacency_dict[name]
                self.save_action(self.DEL_VERTEX, vertex_name=name, x=v.x, y=v.y, vertex_row=self.vertexes[name])

            self.vertexes_coordinates.pop(name)
            self.vertexes.pop(name)
            for item in self.vertexes.values():
                if name in item:
                    item.pop(name)

    def clear(self):
        self.vertexes.clear()
        self.vertexes_coordinates.clear()
        self.__vertex_counter = 0
        self.__history.clear()
        self.__history_counter = 0

    def undo(self):
        # если нечего отменять выходим
        if self.__history_counter == 0:
            return False

        # достаем данные из истории
        act_list = self.__history[self.__history_counter - 1]

        # выполняем действие обратное выполненому
        if self.ADD_EDGE == act_list[0]:
            self.del_edge(act_list[1], act_list[2], act_list[3], False)
        elif self.ADD_VERTEX == act_list[0]:
            self.del_vertex(act_list[1], False)
            self.set_vertexes_counter(int(self.get_new_vertex_name())-1)
        elif self.DEL_EDGE == act_list[0]:
            self.add_edge(act_list[1], act_list[2], act_list[3], False)
        elif self.DEL_VERTEX == act_list[0]:
            self.vertexes_coordinates[act_list[1]] = Vertex(act_list[1], act_list[2], act_list[3])
            self.vertexes[act_list[1]] = copy(act_list[4])
            for v_name, w_list in act_list[5].items():
                self.vertexes[v_name][act_list[1]] = copy(w_list)

        # сдвигаем счетчик действия/состояния на пердыдущее
        self.__history_counter -= 1
        return True

    def redo(self):
        # если не было откатов, то нечего повторять
        if len(self.__history) == self.__history_counter:
            return False
        # если счетчик событий больше, чтем есть событий - ошибка
        elif len(self.__history) < self.__history_counter:
            raise Exception(f'Length of history array less than history counter\n'
                            f'len = {len(self.__history)}\n'
                            f'history_num = {self.__history_counter}')

        # сохраняем данные события
        act_list = self.__history[self.__history_counter]

        # просто повторение действий
        if self.ADD_EDGE == act_list[0]:
            self.add_edge(act_list[1], act_list[2], act_list[3], False)
        elif self.ADD_VERTEX == act_list[0]:
            self.add_vertex(act_list[1], act_list[2], act_list[3], False)
            self.set_vertexes_counter(int(self.get_new_vertex_name()) + 1)
        elif self.DEL_EDGE == act_list[0]:
            self.del_edge(act_list[1], act_list[2], act_list[3], False)
        elif self.DEL_VERTEX == act_list[0]:
            self.del_vertex(act_list[1], False)

        self.__history_counter += 1
        return True

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
        while len(self.__history) > self.__history_counter:
            self.__history.pop()

        # добавление вершины
        if self.ADD_VERTEX == action_code:
            if vertex_name is None or x is None or y is None:
                raise Exception('ADD_VERTEX error. Some of arguments are None')
            self.__history.append([action_code, vertex_name, x, y])

        # добавление ребра
        elif self.ADD_EDGE == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None:
                raise Exception('ADD_EDGE error. Some of arguments are None')
            self.__history.append([action_code, vertex_name, following_vertex_name, weight])

        # удаление ребра
        elif self.DEL_EDGE == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None:
                raise Exception('DEL_EDGE error. Some of arguments are None')
            self.__history.append([action_code, vertex_name, following_vertex_name, weight])

        # удаление вершины
        elif self.DEL_VERTEX == action_code:
            if vertex_name is None or x is None or y is None or vertex_row is None or related_vertex is None:
                raise Exception('DEL_VERTEX error. Some of arguments are None')
            self.__history.append([action_code, vertex_name, x, y, copy(vertex_row), copy(related_vertex)])

        # после добавления действия счетчик устанавливается на последнее действие
        self.__history_counter = len(self.__history)
        # удаляем самое старое действие, если их больше установленного
        if len(self.__history) > self.HISTORY_REC_NUM:
            self.__history.pop(0)

    def get_new_vertex_name(self) -> str:
        self.__vertex_counter += 1
        return str(self.__vertex_counter - 1)

    def set_vertexes_counter(self, value: int):
        self.__vertex_counter = value
