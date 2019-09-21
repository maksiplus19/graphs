from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsItem, QGraphicsEllipseItem, QGraphicsSimpleTextItem
from PyQt5.QtGui import QMouseEvent, QFont, QBrush, QPen, QColor

from graph.vertex import Vertex


class GraphicsVertex(QGraphicsItemGroup):
    def __init__(self, v: Vertex):
        super().__init__()

        self.vertex_radius = 30
        self.pen = QPen(QBrush(QColor(68, 191, 46)), 3)
        self.brush = QBrush(QColor(91, 255, 62))

        self.v = v
        self.offset_coords = QPointF()
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)

        # создаем элипс для вершины
        ellipse = QGraphicsEllipseItem(v.x - (self.vertex_radius / 2), v.y - (self.vertex_radius / 2),
                                       self.vertex_radius, self.vertex_radius)
        ellipse.setPen(self.pen)
        ellipse.setBrush(self.brush)

        # создаем текст для имени вершины
        text = QGraphicsSimpleTextItem(v.name)
        font = QFont()
        font.setPixelSize(self.vertex_radius / 2)
        text.setFont(font)
        # настраиваем расположение текста
        if int(v.name) < 10:
            text.setPos(v.x - self.vertex_radius / 6, v.y - self.vertex_radius / 3)
        else:
            text.setPos(v.x - self.vertex_radius / 4, v.y - self.vertex_radius / 3)

        # объединяем
        self.addToGroup(ellipse)
        self.addToGroup(text)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        pass

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.offset_coords = self.pos() - self.mapToScene(event.pos())
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            pos = QPointF(self.mapToScene(event.pos()))

            self.setPos(pos + self.offset_coords)
            self.v.x = pos.x()
            self.v.y = pos.y()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.setCursor(Qt.ArrowCursor)
