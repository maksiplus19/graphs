from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractTableModel, QModelIndex

from graph.graph import Graph


class GraphModel(QAbstractTableModel):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph
        self.matrix = []
        self.graphToMatrix()

    def graphToMatrix(self):
        n = len(self.graph.vertexes_coordinates)
        if n > 0:
            # преобразование графа в матрицу смежности
            self.matrix = [[0]*n for i in range(n)]
            for v_from, to_dict in self.graph.vertexes.items():
                v_from = int(v_from)
                for v_to, to_list in to_dict.items():
                    v_to = int(v_to)
                    for weight in to_list:
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

    def data(self, index: QModelIndex, role=None) -> any:
        if role == Qt.DisplayRole:
            if not self.graph.oriented:
                # вернуть 1 если есть ребро, 0 если нет
                return 1 if self.matrix[index.row()][index.column()] > 0 else 0
            else:
                # вернуть сумму весов ребер
                return self.matrix[index.row()][index.column()]