from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QMouseEvent, QTransform
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from graph.graph import Graph
from ui.sourse.graphicsvertex import GraphicsVertex


class QGraphView(QGraphicsView):
    def __init__(self, centralwidget):
        super().__init__(centralwidget)
        self.graph = None

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.rightButtonPressed = False
        self.startPos = None
        self.endPos = None
        self.edge_from = None

    def set_graph(self, graph: Graph):
        self.graph = graph
        print(graph)

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
        if event.button() == 2:
            print(self.scene.itemAt(self.mapToScene(event.pos()), QTransform()).group().group())

    # def mousePressEvent(self, event: QMouseEvent):
    #     if event.button() == 2:
    #         self.rightButtonPressed = True
    #         self.startPos = self.mapToScene(event.pos())
    #         item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform()).group()
    #         if item:
    #             self.edge_from = item.v.name
    #     else:
    #         item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
    #         if item:
    #             self.scene.itemAt(self.mapToScene(event.pos()), QTransform()).group().mousePressEvent(event)
    #
    # def mouseMoveEvent(self, event: QMouseEvent):
    #     self.drawGraph()
    #     if self.rightButtonPressed:
    #         # if self.scene.items():
    #         #     self.scene.removeItem(self.scene.items()[0])
    #         self.endPos = self.mapToScene(event.pos())
    #         self.scene.addLine(self.startPos.x(), self.startPos.y(), self.endPos.x(), self.endPos.y())
    #     else:
    #         item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
    #         if item:
    #             self.scene.itemAt(self.mapToScene(event.pos()), QTransform()).group().mousePressEvent(event)
    #
    # def mouseReleaseEvent(self, event: QMouseEvent):
    #     if event.button() == 2:
    #         self.rightButtonPressed = False
    #         self.scene.removeItem(self.scene.items()[0])
    #         print(self.scene.itemAt(self.mapToScene(event.pos()), QTransform()))
    #         item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform()).group()
    #         if item:
    #             edge_to = item.v.name
    #             self.graph.add_edge(self.edge_from, edge_to)
    #             self.drawGraph()
    #     else:
    #         item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
    #         if item:
    #             self.scene.itemAt(self.mapToScene(event.pos()), QTransform()).group().mousePressEvent(event)

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
