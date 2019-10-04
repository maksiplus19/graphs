from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsEllipseItem

from graph.vertex import Vertex


class GraphicsEdge(QGraphicsItemGroup):
    def __init__(self, v_from: Vertex, v_to: Vertex, node: Vertex, oriented: bool, weight: int = 1):
        super().__init__()

        self.v_from = v_from
        self.v_to = v_to
        self.node = node
        # self.node = Vertex("node", self.v_from.x - (self.v_from.x - self.v_to.x) / 2,
        #                                          self.v_from.y - (self.v_from.y - self.v_to.y) / 2)
        # self.node.x = self.v_from.x - (self.v_from.x - self.v_to.x) / 2
        # self.node.y = self.v_from.y - (self.v_from.y - self.v_to.y) / 2
        self.weight = weight

        # self.pen = QPen(QBrush(QColor(0, 0, 0)), 3)

        self.line1 = QGraphicsLineItem(self.v_from.x, self.v_from.y, self.node.x, self.node.y)
        self.line1.setPen(QPen(QBrush(QColor(0, 0, 0)), 3))

        self.line2 = QGraphicsLineItem(self.node.x, self.node.y, self.v_to.x, self.v_to.y)
        if oriented:
            self.line2.setPen(QPen(QBrush(QColor(68, 191, 46)), 3))
        else:
            self.line2.setPen(QPen(QBrush(QColor(0, 0, 0)), 3))

        self.ellipse = QGraphicsEllipseItem(self.node.x - 4, self.node.y - 4, 8, 8)
        self.ellipse.setBrush(QBrush(QColor(0, 0, 0)))


        self.addToGroup(self.line1)
        self.addToGroup(self.line2)
        self.addToGroup(self.ellipse)




