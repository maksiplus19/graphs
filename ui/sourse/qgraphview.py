from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QMouseEvent, QPen, QBrush, QColor, QResizeEvent, QFont
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItemGroup, QGraphicsEllipseItem, \
    QGraphicsSimpleTextItem
from graph.graph import Graph


class QGraphView(QGraphicsView):
    def __init__(self, centralwidget):
        super().__init__(centralwidget)
        self.vertex_radius = 30
        self.graph = None

        self.scene = QGraphicsScene()
        self.setAlignment(Qt.AlignCenter)
        self.setScene(self.scene)

        self.pen = QPen(QBrush(QColor(68, 191, 46)), 3)
        self.brush = QBrush(QColor(91, 255, 62))

    def set_graph(self, graph: Graph):
        self.graph = graph
        print(graph)

    def mouseMoveEvent(self, event: QMouseEvent):
        pass

    def mousePressEvent(self, event: QMouseEvent):
        print('mouse press', event.button())

    def mouseReleaseEvent(self, event: QMouseEvent):
        print('mouse release', event.button())

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        print('double click')
        # только левая кнопка мыши
        if event.button() == 1:
            # получаем имя вершины
            name = str(len(self.graph.vertexes_coordinates))
            # преобразум коодинаты в координаты сцены
            pos = QPointF(self.mapToScene(event.pos()))
            # добавляем вершину в граф
            self.graph.add_vertex(name, pos.x(), pos.y())
            self.drawGraph()

    def drawGraph(self):
        # очищаем сцену
        self.scene.clear()
        # рисуем вершины
        for v in self.graph.vertexes_coordinates.values():
            # создаем группу элементов
            vertex = QGraphicsItemGroup()

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

            # объединяем и добавляем на сцену
            vertex.addToGroup(ellipse)
            vertex.addToGroup(text)
            self.scene.addItem(vertex)

    # def resizeEvent(self, event: QResizeEvent):
    #     self.scene.setSceneRect(0, 0, event.size().width(), event.size().height())
