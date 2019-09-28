from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QTransform
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsSimpleTextItem, \
    QGraphicsLineItem
from graph.graph import Graph
from ui.sourse.graphicsvertex import GraphicsVertex


class QGraphView(QGraphicsView):
    def __init__(self, centralwidget):
        super().__init__(centralwidget)
        self.graph = None

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.rightButtonPressed = False
        self.leftButtonPressed = True
        self.startPos = QPointF()
        self.endPos = None
        self.edge_from = None
        self.moveVertex = None

        self.setRenderHint(QPainter.Antialiasing)

    def set_graph(self, graph: Graph):
        self.graph = graph

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        print('double click')
        # только левая кнопка мыши
        if event.button() == 1:
            # получаем имя вершины
            name = self.graph.get_new_vertex_name()
            # преобразум коодинаты в координаты сцены
            pos = QPointF(self.mapToScene(event.pos()))
            # добавляем вершину в граф
            self.graph.add_vertex(name, pos.x(), pos.y())
            self.drawGraph()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == 2:
            self.rightButtonPressed = True
            item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
            if item:
                self.startPos = self.mapToScene(event.pos())
                self.edge_from = item.group().v.name
        elif event.button() == 1:
            self.leftButtonPressed = True
            item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
            if item:
                self.moveVertex = item.group().v.name
                self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.drawGraph()
        if self.rightButtonPressed and self.edge_from is not None:
            self.endPos = self.mapToScene(event.pos())
            self.scene.addLine(self.startPos.x(), self.startPos.y(), self.endPos.x(), self.endPos.y())
        elif self.leftButtonPressed and self.moveVertex is not None:
            pos = QPointF(self.mapToScene(event.pos()))
            self.graph.vertexes_coordinates[self.moveVertex].x = pos.x()
            self.graph.vertexes_coordinates[self.moveVertex].y = pos.y()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == 2 and self.edge_from is not None:
            self.rightButtonPressed = False
            self.scene.removeItem(self.scene.items()[0])
            item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
            if item:
                if type(item) is QGraphicsLineItem:
                    pass
                elif type(item) is GraphicsVertex:
                    edge_to = item.v.name
                    self.graph.add_edge(self.edge_from, edge_to)
                elif type(item) is QGraphicsEllipseItem or QGraphicsSimpleTextItem:
                    edge_to = item.group().v.name
                    self.graph.add_edge(self.edge_from, edge_to)
                self.drawGraph()
            self.edge_from = None
        elif event.button() == 1:
            self.leftButtonPressed = False
            self.moveVertex = None
            self.setCursor(Qt.ArrowCursor)

    def drawGraph(self):
        # очищаем сцену
        self.scene.clear()

        # рисуем ребра
        for v_from, to_dict in self.graph.vertexes.items():
            v_from = self.graph.vertexes_coordinates[v_from]
            for v_to, to_list in to_dict.items():
                v_to = self.graph.vertexes_coordinates[v_to]
                for edge in to_list:
                    if not self.graph.oriented:
                        self.scene.addLine(v_from.x, v_from.y, v_to.x, v_to.y)

        # рисуем вершины
        for v in self.graph.vertexes_coordinates.values():
            self.scene.addItem(GraphicsVertex(v))

    # def resizeEvent(self, event: QResizeEvent):
    #     self.scene.setSceneRect(0, 0, event.size().width(), event.size().height())
