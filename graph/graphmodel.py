from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel, QModelIndex

from graph.graph import Graph


class GraphModel(QAbstractTableModel):
    def __init__(self, graph: Graph = None):
        super().__init__()
        self.graph = graph
        self.matrix = []
        self.graphToMatrix()

    def setGraph(self, graph: Graph):
        self.graph = graph
        self.graphToMatrix()
        self.modelReset.emit()

    def graphToMatrix(self):
        """
            Метод для преобразования графа в матрицу смежности и обновления модели
        """
        if self.graph is None:
            return
        if not self.graph.vertexes_coordinates:
            self.matrix = [[None]]
            self.modelReset.emit()
            return
        n = int(sorted(self.graph.vertexes, key=lambda el: int(el))[-1])
        if n > 0:
            # преобразование графа в матрицу смежности
            self.matrix = [[0] * n for i in range(n)]
            for v_from, to_dict in self.graph.vertexes.items():
                v_from = int(v_from)
                for v_to, to_list in to_dict.items():
                    v_to = int(v_to)
                    for weight, node in to_list:
                        if self.graph.oriented:
                            self.matrix[v_from - 1][v_to - 1] += weight
                        else:
                            self.matrix[v_from - 1][v_to - 1] += weight
                            self.matrix[v_to - 1][v_from - 1] += weight
            # сообраем вьюхе, что модель обновилась
            self.modelReset.emit()

    def rowCount(self, parent=None, *args, **kwargs) -> int:
        return len(self.matrix)

    def columnCount(self, parent=None, *args, **kwargs) -> int:
        return len(self.matrix)

    def data(self, index: QModelIndex, role=None):
        if not len(self.graph.vertexes_coordinates):
            return
        if role == Qt.DisplayRole:
            if not self.graph.oriented:
                # вернуть количество ребер
                return self.matrix[index.row()][index.column()] // 2
            else:
                # вернуть сумму весов ребер
                return self.matrix[index.row()][index.column()]

    def setData(self, index: QModelIndex, data: str, role=None):
        if data == '' or not data.isdigit():
            return False
        data = int(data)
        if data == 0:
            # новй вес 0 значит нужно удалить все ребра между данными вершинами
            v_from = str(index.row() + 1)
            v_to = str(index.column() + 1)
            self.graph.del_all_edges(v_from, v_to)
            if not self.graph.oriented and v_from != v_to:
                self.graph.del_all_edges(v_to, v_from, False)
            self.graphToMatrix()
            return True
        elif data > 0:
            # новый вес значит нужно обновить все старые на одно новое
            v_from = str(index.row() + 1)
            v_to = str(index.column() + 1)
            if self.graph.weighted:
                self.graph.set_all_edges(v_from, v_to, data)
            else:
                self.graph.set_all_edges(v_from, v_to, 1)
            if not self.graph.oriented and v_to != v_from:
                self.graph.set_all_edges(v_to, v_from, data, False)
            self.graphToMatrix()
            return True
        return False

    def flags(self, index: QModelIndex):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled
