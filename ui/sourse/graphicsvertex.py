from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsItem, QGraphicsEllipseItem, QGraphicsSimpleTextItem
from PyQt5.QtGui import QFont, QBrush, QPen, QColor

from graph.vertex import Vertex


class GraphicsVertex(QGraphicsItemGroup):
    def __init__(self, v: Vertex):
        super().__init__()
        dark = 20

        self.vertex_radius = 30
        self.pen = QPen(QBrush(QColor(68, 191, 46)), 3) if v.color is None \
            else QPen(QBrush(QColor(v.color.red() - dark, v.color.green() - dark, v.color.blue() - dark)), 3)
        self.brush = QBrush(QColor(91, 255, 62)) if v.color is None else QBrush(v.color)

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

        self.startPos = None
        self.rightButtonPressed = False
        self.edge_from = None

    # def mouseDoubleClickEvent(self, event: QMouseEvent):
    #     pass
    #
    # def mousePressEvent(self, event: QMouseEvent):
    #     if event.button() == 1:
    #         self.offset_coords = self.pos() - self.mapToScene(event.pos())
    #         self.setCursor(Qt.ClosedHandCursor)
    #     elif event.button() == Qt.RightButton:
    #         self.rightButtonPressed = True
    #         self.startPos = self.mapToScene(event.pos())
    #         item = self.scene().itemAt(self.mapToScene(event.pos()), QTransform()).group()
    #         if item:
    #             self.edge_from = item.v.name
    #
    # def mouseMoveEvent(self, event: QMouseEvent):
    #     if event.buttons() == Qt.LeftButton:
    #         pos = QPointF(self.mapToScene(event.pos()))
    #
    #         self.setPos(pos + self.offset_coords)
    #         self.v.x = pos.x()
    #         self.v.y = pos.y()
    #
    # def mouseReleaseEvent(self, event: QMouseEvent):
    #     self.setCursor(Qt.ArrowCursor)

