import math

from PyQt5.QtGui import QMouseEvent, QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from random import randint
from graphs.graph.graph import Graph


class QGraphView(QGraphicsView):
    def __init__(self, centralwidget):
        super().__init__(centralwidget)
        self.graph = None
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.pen = QPen(QBrush(QColor(68, 191, 46, 75)), 3)
        self.brush = QBrush(QColor(91, 255, 62, 100))

    def set_graph(self, graph: Graph):
        self.graph = graph
        # рисуем вершины
        for i in range(len(self.graph.adjacency_matrix)):
            # addEllipse(qreal x, qreal y, qreal w, qreal h, const QPen &pen = QPen(), const QBrush &brush = QBrush())
            self.scene.addEllipse(randint(0, 100), randint(0, 100), 10, 10, self.pen, self.brush)
        print(graph)

    # def update(self, *__args):
    #     pass

    def mouseMoveEvent(self, event: QMouseEvent):
        pass

    def mousePressEvent(self, event: QMouseEvent):
        print('mouse press', event.button())

    def mouseReleaseEvent(self, event: QMouseEvent):
        print('mouse release', event.button())

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        print('double click')
