from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsItem
from PyQt5.QtGui import QMouseEvent

from graph.vertex import Vertex


class GraphicsVertex(QGraphicsItemGroup):
    def __init__(self, v: Vertex):
        super().__init__()
        self.v = v
        self.offset_coords = QPointF()
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        pass

    def mousePressEvent(self, event: QMouseEvent):
        self.offset_coords = self.pos() - self.mapToScene(event.pos())
        self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = QPointF(self.mapToScene(event.pos()))

        self.setPos(pos + self.offset_coords)
        self.v.x = pos.x()
        self.v.y = pos.y()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.setCursor(Qt.ArrowCursor)

