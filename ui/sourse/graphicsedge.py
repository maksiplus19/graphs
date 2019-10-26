from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsSimpleTextItem

from graph.vertex import Vertex


class GraphicsEdge(QGraphicsItemGroup):
    def __init__(self, v_from: Vertex, v_to: Vertex, node: Vertex, oriented: bool, weight: int = 1,
                 weighted: bool = True):
        super().__init__()

        self.v_from = v_from
        self.v_to = v_to
        self.node = node
        self.weighted = weighted
        self.weight = weight

        # self.pen = QPen(QBrush(QColor(0, 0, 0)), 3)



        if weighted:
            self.ellipse = QGraphicsEllipseItem(self.node.x - 8, self.node.y - 8, 16, 16)
            self.ellipse.setBrush(QBrush(QColor(0, 0, 0)))
            self.addToGroup(self.ellipse)

            text = QGraphicsSimpleTextItem(str(self.weight))
            font = QFont()
            font.setPixelSize(8)
            text.setPen(QColor(255, 255, 255))
            text.setFont(font)
            # настраиваем расположение текста
            if self.weight < 10:
                text.setPos(self.node.x - 16 / 6, self.node.y - 16 / 3)
            else:
                text.setPos(self.node.x - 4, self.node.y - 16 / 3)

            self.addToGroup(text)
        else:
            self.ellipse = QGraphicsEllipseItem(self.node.x - 4, self.node.y - 4, 8, 8)
            self.ellipse.setBrush(QBrush(QColor(0, 0, 0)))
            self.addToGroup(self.ellipse)







