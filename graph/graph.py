import random
from copy import copy
from typing import Dict, List

from PyQt5.QtCore import QObject, pyqtSignal

from graph.vertex import Vertex


def edited(method):
    def warped(self, *args):
        method(self, *args)
        self.saved = False

    return warped


class Graph:
    """Класс графа"""

    ADD_VERTEX = 1
    ADD_EDGE = 2
    DEL_VERTEX = 3
    DEL_EDGE = 4
    MOVE_VERTEX = 5
    GRAPH_CLEAR = 6
    SET_EDGE = 7
    SET_ALL_EDGES = 8
    DEL_ALL_EDGES = 9
    HISTORY_REC_NUM = 10
    CHANGE_ORIENT = 11

    class __Signals(QObject):
        # сигнал, который будет отправляться при изменении графа
        update = pyqtSignal()

    def __init__(self):
        # Граф хранится в виде словаря.
        # Каждой вершине соответсвуеет словарь вершин,
        # до которых есть дуги и список их весов
        self.vertexes: Dict[str, Dict[str, (int, Vertex)]] = {}
        # vertexes_coordinates = dict(name, Vertex)
        self.vertexes_coordinates: Dict[str, Vertex] = {}
        self.oriented = True
        self.weighted = True
        self.saved = True
        self.__history: List[List] = []
        self.__history_counter = 0
        self.signals = self.__Signals()

    @edited
    def add_edge(self, v_from: str, v_to: str, weight: int = 1, node: Vertex = None, __save: bool = True):
        if v_from in self.vertexes and v_to in self.vertexes:
            if node is None:
                node = self.create_node(v_from, v_to)
            if __save:
                # данное условие необходимо для того, что не было повторного сохранения при откате
                # или повторении действия, т.к. оно уже сохранено
                self.save_action(self.ADD_EDGE, vertex_name=v_from, following_vertex_name=v_to,
                                 weight=weight, node=node)

            # если еще список ребер еще не создан, то создаем его
            if v_to not in self.vertexes[v_from]:
                self.vertexes[v_from][v_to] = []
            # добавляем ребро
            self.vertexes[v_from][v_to].append([weight, node])
            # сортируем, чтобы ребро с меньшим весом было первым
            self.vertexes[v_from][v_to].sort(key=lambda el: el[0])
            if not self.oriented:
                if v_from not in self.vertexes[v_to]:
                    self.vertexes[v_to][v_from] = []
                self.vertexes[v_to][v_from].append([weight, node])
                self.vertexes[v_to][v_from].sort(key=lambda el: el[0])
            self.signals.update.emit()
        else:
            raise Exception('No vertex for adding edge')

    @edited
    def add_vertex(self, name: str, x: float = None, y: float = None, __save: bool = True):
        if name not in self.vertexes_coordinates:
            if x is None:
                x = random.randint(-100, 100)
            if y is None:
                y = random.randint(-100, 100)
            if __save:
                # данное условие необходимо для того, что не было повторного сохранения при откате
                # или повторении действия, т.к. оно уже сохранено
                self.save_action(self.ADD_VERTEX, vertex_name=name, x=x, y=y)

            self.vertexes_coordinates[name] = Vertex(name, x, y)
            self.vertexes[name] = {}
            self.signals.update.emit()

    @edited
    def del_edge(self, v_from: str, v_to: str, weight: int = 1, node: Vertex = None, __save: bool = True):
        if v_from in self.vertexes and v_to in self.vertexes[v_from]:
            arr = self.vertexes[v_from][v_to]
            helper = [el[0] for el in arr]
            if weight in helper:
                if node is None:
                    index = helper.index(weight)
                else:
                    index = [el[1] for el in arr].index(node)
                if __save:
                    # данное условие необходимо для того, что не было повторного сохранения при откате
                    # или повторении действия, т.к. оно уже сохранено
                    self.save_action(self.DEL_EDGE, vertex_name=v_from, following_vertex_name=v_to, weight=weight,
                                     node=arr[index][1])
                arr.pop(index)
            self.signals.update.emit()

    @edited
    def del_all_edges(self, v_from: str, v_to: str, __save: bool = True):
        if v_from in self.vertexes and v_to in self.vertexes[v_from]:
            if __save:
                # данное условие необходимо для того, что не было повторного сохранения при откате
                # или повторении действия, т.к. оно уже сохранено
                self.save_action(self.DEL_ALL_EDGES, vertex_name=v_from, following_vertex_name=v_to,
                                 edges=self.vertexes[v_from][v_to])
            self.vertexes[v_from].pop(v_to)
            self.signals.update.emit()

    @edited
    def set_all_edges(self, v_from: str, v_to: str, weight: int, __save: bool = True):
        if v_from in self.vertexes and v_to in self.vertexes:
            node = self.create_node(v_from, v_to)
            if __save:
                self.save_action(Graph.SET_ALL_EDGES, vertex_name=v_from, following_vertex_name=v_to,
                                 edges=self.vertexes[v_from].get(v_to), weight=weight, node=node)
            self.vertexes[v_from][v_to] = [(weight, node)]
            self.signals.update.emit()

    @edited
    def set_edge(self, v_from: str, v_to: str, old_weight: int, new_weight: int, __save: bool = True):
        pass
        # if v_from in self.vertexes and v_to in self.vertexes[v_from]:
        #     node = Vertex('node', self.vertexes_coordinates[v_from].x -
        #                   (self.vertexes_coordinates[v_from].x - self.vertexes_coordinates[v_to].x) / 2 -
        #                   random.randint(-50, 50),
        #                   self.vertexes_coordinates[v_from].y -
        #                   (self.vertexes_coordinates[v_from].y - self.vertexes_coordinates[v_to].y) / 2 -
        #                   random.randint(-50, 50))
        #     arr = self.vertexes[v_from][v_to]
        #     helper = [el[0] for el in arr]
        #     if old_weight in helper:
        #         if __save:
        #             self.save_action(self.SET_EDGE, vertex_name=v_from, following_vertex_name=v_to,
        #                              weight=old_weight, new_weight=new_weight)
        #         arr[arr.index(old_weight)] = new_weight
        #         self.signals.update.emit()

    @edited
    def del_vertex(self, name: str, __save: bool = True):
        if name in self.vertexes_coordinates:
            if __save:
                # данное условие необходимо для того, что не было повторного сохранения при откате
                # или повторении действия, т.к. оно уже сохранено
                v = self.vertexes_coordinates[name]
                related_vertex = {}
                # сохраняем все ребра, которые идут в удаляемую вершину
                for v_from, adjacency_dict in self.vertexes.items():
                    if name in adjacency_dict:
                        related_vertex[v_from] = adjacency_dict[name]
                self.save_action(self.DEL_VERTEX, vertex_name=name, x=v.x, y=v.y, vertex_row=self.vertexes[name],
                                 related_vertex=related_vertex)

            self.vertexes_coordinates.pop(name)
            self.vertexes.pop(name)
            for item in self.vertexes.values():
                if name in item:
                    item.pop(name)
            self.signals.update.emit()

    @edited
    def change_orient(self, v_from: str, v_to: str, weight: int, node: Vertex, __save: bool = True):
        if v_from in self.vertexes and v_to in self.vertexes[v_from]:
            arr = self.vertexes[v_from][v_to]
            helper = [el[0] for el in arr]
            if weight in helper:
                if node is None:
                    index = helper.index(weight)
                else:
                    index = [el[1] for el in arr].index(node)
                if __save:
                    # данное условие необходимо для того, что не было повторного сохранения при откате
                    # или повторении действия, т.к. оно уже сохранено
                    self.save_action(self.CHANGE_ORIENT, vertex_name=v_from, following_vertex_name=v_to, weight=weight,
                                     node=arr[index][1])

            self.del_edge(v_from, v_to, weight, node, False)
            self.add_edge(v_to, v_from, weight, node, False)
            if not self.vertexes[v_from][v_to]:
                self.vertexes[v_from].pop(v_to)
            # arr = self.vertexes[v_from][v_to]
            # helper = [el[0] for el in arr]
            # if weight in helper:
            #     if node is None:
            #         index = helper.index(weight)
            #     else:
            #         index = [el[1] for el in arr].index(node)
            #     if __save:
            #         # данное условие необходимо для того, что не было повторного сохранения при откате
            #         # или повторении действия, т.к. оно уже сохранено
            #         self.save_action(self.CHANGE_ORIENT, vertex_name=v_from, following_vertex_name=v_to, weight=weight,
            #                          node=arr[index][1])
            #     if v_from in self.vertexes[v_to]:
            #         self.vertexes[v_to][v_from].append(arr.pop(index))
            #         self.vertexes[v_to][v_from].sort(key=lambda el: el[0])
            #         if not arr:
            #             self.vertexes[v_from].pop(v_to)
            #     else:
            #         self.vertexes[v_to][v_from] = [arr.pop(index)]
            #         if len(self.vertexes[v_from][v_to]) == 0:
            #             self.vertexes[v_from].pop(v_to)
            # self.signals.update.emit()

    def clear(self):
        self.vertexes.clear()
        self.vertexes_coordinates.clear()
        self.__history.clear()
        self.__history_counter = 0
        self.signals.update.emit()

    def undo(self):
        # если нечего отменять выходим
        if self.__history_counter == 0:
            return False

        # достаем данные из истории
        act_list = self.__history[self.__history_counter - 1]

        # выполняем действие обратное выполненому
        if self.ADD_EDGE == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, weight, node]
            self.del_edge(act_list[1], act_list[2], act_list[3], act_list[4], False)
            if not self.oriented:
                self.del_edge(act_list[2], act_list[1], act_list[3], act_list[4], False)
        elif self.ADD_VERTEX == act_list[0]:
            # [action_code, vertex_name, x, y]
            self.del_vertex(act_list[1], False)
        elif self.DEL_EDGE == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, weight, node]
            self.add_edge(act_list[1], act_list[2], act_list[3], act_list[4], False)
        elif self.DEL_VERTEX == act_list[0]:
            # [action_code, vertex_name, x, y, copy(vertex_row), copy(related_vertex)]
            self.vertexes_coordinates[act_list[1]] = Vertex(act_list[1], act_list[2], act_list[3])
            self.vertexes[act_list[1]] = copy(act_list[4])
            for v_name, w_list in act_list[5].items():
                self.vertexes[v_name][act_list[1]] = copy(w_list)
        elif self.SET_ALL_EDGES == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, copy(edges), weight, node]
            if act_list[3] is not None:
                self.vertexes[act_list[1]][act_list[2]] = act_list[3]
                if not self.oriented:
                    self.vertexes[act_list[2]][act_list[1]] = act_list[3]
            else:
                self.vertexes[act_list[1]].pop(act_list[2])
                if not self.oriented and act_list[1] in self.vertexes[act_list[2]]:
                    self.vertexes[act_list[2]].pop(act_list[1])
        elif self.SET_EDGE == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, weight, new_weight]
            self.set_edge(act_list[1], act_list[2], act_list[4], act_list[3], False)
            if not self.oriented:
                self.set_edge(act_list[2], act_list[1], act_list[4], act_list[3], False)
        elif self.DEL_ALL_EDGES == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, edges]
            self.vertexes[act_list[1]][act_list[2]] = act_list[3]
            if not self.oriented:
                self.vertexes[act_list[2]][act_list[1]] = act_list[3]
        elif self.CHANGE_ORIENT == act_list[0]:
            self.change_orient(act_list[2], act_list[1], act_list[3], act_list[4], False)

        # сдвигаем счетчик действия/состояния на пердыдущее
        self.__history_counter -= 1
        self.signals.update.emit()
        return True

    def redo(self):
        # если не было откатов, то нечего повторять
        if len(self.__history) == self.__history_counter:
            return False
        # если счетчик событий больше
        elif len(self.__history) < self.__history_counter:
            return False

        # сохраняем данные события
        act_list = self.__history[self.__history_counter]

        # просто повторение действий
        if self.ADD_EDGE == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, weight, node]
            self.add_edge(act_list[1], act_list[2], act_list[3], act_list[4], False)
            if not self.oriented:
                self.add_edge(act_list[2], act_list[1], act_list[3], act_list[4], False)
        elif self.ADD_VERTEX == act_list[0]:
            # [action_code, vertex_name, x, y]
            self.add_vertex(act_list[1], act_list[2], act_list[3], False)
        elif self.DEL_EDGE == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, weight, node]
            self.del_edge(act_list[1], act_list[2], act_list[3], act_list[4], False)
        elif self.DEL_VERTEX == act_list[0]:
            # [action_code, vertex_name, x, y, copy(vertex_row), copy(related_vertex)]
            self.del_vertex(act_list[1], False)
        elif self.SET_ALL_EDGES == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, copy(edges), weight, node]
            self.vertexes[act_list[1]][act_list[2]] = [(act_list[4], act_list[5])]
            if not self.oriented:
                self.vertexes[act_list[2]][act_list[1]] = [(act_list[4], act_list[5])]
        # elif self.SET_EDGE == act_list[0]:
        #     # [action_code, vertex_name, following_vertex_name, weight, new_weight]
        #     self.set_edge(act_list[1], act_list[2], act_list[3], act_list[4], False)
        #     if not self.oriented:
        #         self.set_edge(act_list[2], act_list[1], act_list[3], act_list[4], False)
        elif self.DEL_ALL_EDGES == act_list[0]:
            # [action_code, vertex_name, following_vertex_name, edges]
            self.del_all_edges(act_list[1], act_list[2], False)
            if not self.oriented:
                self.del_all_edges(act_list[2], act_list[1], False)
        elif self.CHANGE_ORIENT == act_list[0]:
            self.change_orient(act_list[1], act_list[2], act_list[3], act_list[4], False)

        self.__history_counter += 1
        self.signals.update.emit()
        return True

    def save_action(self, action_code: int, vertex_name: str = None, following_vertex_name: str = None,
                    weight: int = None, x: float = None, y: float = None, vertex_row: dict = None,
                    related_vertex: dict = None, edges: list = None, new_weight: int = None, node: Vertex = None):
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
                raise Exception('Saving ADD_VERTEX error. Some of arguments is None')
            self.__history.append([action_code, vertex_name, x, y])

        # добавление ребра
        elif self.ADD_EDGE == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None or node is None:
                raise Exception('Saving ADD_EDGE error. Some of arguments is None')
            self.__history.append([action_code, vertex_name, following_vertex_name, weight, node])

        # удаление ребра
        elif self.DEL_EDGE == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None or node is None:
                raise Exception('Saving DEL_EDGE error. Some of arguments is None')
            self.__history.append([action_code, vertex_name, following_vertex_name, weight, node])

        # удаление вершины
        elif self.DEL_VERTEX == action_code:
            if vertex_name is None or x is None or y is None or vertex_row is None or related_vertex is None:
                raise Exception('Saving DEL_VERTEX error. Some of arguments is None')
            self.__history.append([action_code, vertex_name, x, y, copy(vertex_row), copy(related_vertex)])

        # изменение/установка веса ребра
        elif self.SET_EDGE == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None or new_weight is None:
                raise Exception('Saving SET_EDGE error. Some of arguments is None')
            self.__history.append([action_code, vertex_name, following_vertex_name, weight, new_weight])

        # замена всех ребр на одно
        elif self.SET_ALL_EDGES == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None or node is None:
                raise Exception('Saving SET_ALL_EDGE error. Some of arguments is None')
            self.__history.append([action_code, vertex_name, following_vertex_name, copy(edges), weight, node])

        # удаление всех ребер
        elif self.DEL_ALL_EDGES == action_code:
            if vertex_name is None or following_vertex_name is None or edges is None:
                raise Exception('Saving DEL_ALL_EDGES error. Some of arguments is None')
            self.__history.append([action_code, vertex_name, following_vertex_name, edges])

        # изменение направления ребра
        elif self.CHANGE_ORIENT == action_code:
            if vertex_name is None or following_vertex_name is None or weight is None or node is None:
                raise Exception('Saving CHANGE_ORIENT error. Some of arguments is None')
            self.__history.append([action_code, vertex_name, following_vertex_name, weight, node])

        # удаляем самое старое действие, если их больше установленного
        if len(self.__history) > self.HISTORY_REC_NUM:
            self.__history.pop(0)

        # после добавления действия счетчик устанавливается на последнее действие
        self.__history_counter = len(self.__history)

    def get_new_vertex_name(self) -> str:
        if len(self.vertexes) == 0:
            return '1'
        return str(int(sorted(self.vertexes, key=lambda el: int(el))[-1]) + 1)

    def update(self):
        self.signals.update.emit()

    def create_node(self, v_from: str, v_to: str):
        return Vertex('node', self.vertexes_coordinates[v_from].x -
                      (self.vertexes_coordinates[v_from].x - self.vertexes_coordinates[v_to].x) / 2 -
                      random.randint(-50, 50),
                      self.vertexes_coordinates[v_from].y -
                      (self.vertexes_coordinates[v_from].y - self.vertexes_coordinates[v_to].y) / 2 -
                      random.randint(-50, 50))

    def restore(self):
        for v_from, to_dict in self.vertexes.items():
            for v_to, to_list in to_dict.items():
                to_dict[v_to] = [(weight, self.create_node(v_from, v_to)) for weight in to_list]
