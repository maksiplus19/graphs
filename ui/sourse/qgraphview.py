from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QGraphicsView

from graph.graph import Graph


class QGraphView(QGraphicsView):
    def __init__(self, centralwidget):
        super().__init__(centralwidget)

    def drawGraph(self, graph: Graph):
        pass

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
