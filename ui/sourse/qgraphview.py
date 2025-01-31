from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QMouseEvent, QPainter, QTransform, QContextMenuEvent, QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsSimpleTextItem, \
    QGraphicsLineItem, QMenu
from graph.graph import Graph
from graph.vertex import Vertex
from ui.sourse.graphicsedge import GraphicsEdge
from ui.sourse.graphicsvertex import GraphicsVertex
from graph.savegraph import SaveGraph


class QGraphView(QGraphicsView):
    def __init__(self, centralwidget, graph: Graph):
        super().__init__(centralwidget)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.rightButtonPressed = False
        self.leftButtonPressed = True
        self.startPos = QPointF()
        self.endPos = None
        self.edge_from = None
        self.moveVertex = None
        self.isVertex = None
        self.i = 0
        self.setRenderHint(QPainter.Antialiasing)

        self.pen = QPen(QColor(0, 0, 0), 3)
        self.greenPen = QPen(QColor(68, 191, 46), 3)
        self.pathPen = QPen(QColor(68, 133, 255), 3)
        self.pathBrush = QBrush(QColor(68, 133, 255))

        self.graph = graph
        self.graph.signals.update.connect(self.drawGraph)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        # print('double click')
        # только левая кнопка мыши
        pos = QPointF(self.mapToScene(event.pos()))
        if event.button() == 1:
            # получаем имя вершины
            name = self.graph.get_new_vertex_name()
            # преобразум коодинаты в координаты сцены
            # добавляем вершину в граф
            self.graph.add_vertex(name, pos.x(), pos.y())
        elif event.button() == 2:
            item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
            if item is None:
                return
            if type(item) is QGraphicsLineItem or type(item) is GraphicsEdge or 'node' in item.group().__dict__:
                if self.graph.oriented:
                    context_menu = QMenu(self)
                    change_orient = context_menu.addAction("Изменить направление")
                    action = context_menu.exec_(self.mapToGlobal(event.pos()))
                    if action == change_orient:
                        if type(item) is GraphicsEdge:
                            d = item.__dict__
                        else:
                            d = item.group().__dict__
                        self.graph.change_orient(d['v_from'].name, d['v_to'].name, d['weight'], d['node'])
            elif type(item) is QGraphicsEllipseItem or type(item) is QGraphicsSimpleTextItem:
                context_menu = QMenu(self)
                add_loop = context_menu.addAction("Добавить петлю")
                delete_loop = context_menu.addAction("Удалить петлю")
                delete_vertex = context_menu.addAction("Удалить вершину")
                action = context_menu.exec_(self.mapToGlobal(event.pos()))
                if action == delete_vertex:
                    self.graph.del_vertex(item.group().v.name)
                    self.drawGraph()
                if action == add_loop:
                    print(item.group().v.name)
                    self.graph.add_edge(item.group().v.name, item.group().v.name)
                if action == delete_loop:
                    self.graph.del_edge(item.group().v.name, item.group().v.name)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == 2:
            self.rightButtonPressed = True
            item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
            if item:
                if type(item) is QGraphicsLineItem:
                    pass
                elif type(item) is GraphicsVertex:
                    self.startPos = self.mapToScene(event.pos())
                    self.edge_from = item.v.name
                elif type(item) is QGraphicsEllipseItem or QGraphicsSimpleTextItem and not type(item) is GraphicsEdge:
                    if 'v' in item.group().__dict__:
                        self.startPos = self.mapToScene(event.pos())
                        self.edge_from = item.group().v.name
        elif event.button() == 1:
            self.leftButtonPressed = True
            item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
            if item:
                if type(item) is QGraphicsLineItem:
                    pass
                elif type(item) is GraphicsEdge:
                    self.moveVertex = item.node
                    self.setCursor(Qt.ClosedHandCursor)
                elif type(item) is GraphicsVertex:
                    self.moveVertex = item.v
                    self.setCursor(Qt.ClosedHandCursor)
                elif type(item) is QGraphicsEllipseItem or QGraphicsSimpleTextItem and not type(item) is GraphicsEdge:
                    if type(item.group()) is GraphicsVertex:
                        self.moveVertex = item.group().v
                    else:
                        self.moveVertex = item.group().node
                    self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.drawGraph()
        if self.rightButtonPressed and self.edge_from is not None:
            self.endPos = self.mapToScene(event.pos())
            self.scene.addLine(self.startPos.x(), self.startPos.y(), self.endPos.x(), self.endPos.y())
            # self.isVertex = True
        elif self.leftButtonPressed and self.moveVertex is not None:
            pos = QPointF(self.mapToScene(event.pos()))
            self.moveVertex.x = pos.x()
            self.moveVertex.y = pos.y()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == 2 and self.edge_from is not None:
            self.rightButtonPressed = False
            if type(self.scene.items()[0]) == QGraphicsLineItem:
                self.scene.removeItem(self.scene.items()[0])
            item = self.scene.itemAt(self.mapToScene(event.pos()), QTransform())
            if item:
                if type(item) is QGraphicsLineItem:
                    pass
                elif type(item) is GraphicsVertex:
                    edge_to = item.v.name
                    if edge_to == 'node':
                        return
                    if edge_to != self.edge_from:
                        self.graph.add_edge(self.edge_from, edge_to)
                elif type(item) is QGraphicsEllipseItem or QGraphicsSimpleTextItem:
                    if type(item.group()) is GraphicsEdge:
                        return
                    edge_to = item.group().v.name
                    if edge_to == 'node':
                        return
                    if edge_to != self.edge_from:
                        self.graph.add_edge(self.edge_from, edge_to)
            self.edge_from = None

        elif event.button() == 1:
            self.leftButtonPressed = False
            self.moveVertex = None
            self.setCursor(Qt.ArrowCursor)

    def drawGraph(self, simple: bool = False):
        if simple:
            self.simpleDrawGraph()
            return

        # очищаем сцену
        self.scene.clear()

        # рисуем ребра
        for v_from, to_dict in self.graph.vertexes.items():
            v_from = self.graph.vertexes_coordinates[v_from]
            for v_to, to_list in to_dict.items():
                v_to = self.graph.vertexes_coordinates[v_to]
                try:
                    for weight, node in to_list:
                        # key = f'{v_from.name}_{v_to.name}'
                        # if key in self.graph.edge_path and self.graph.edge_path[key] == weight:
                        #     pen = self.pathPen
                        # elif self.graph.oriented:
                        #     pen = self.greenPen
                        # else:
                        #     pen = self.pen

                        # if v_from is v_to:
                        #     pen = QPen(QBrush(QColor(255, 0, 0)), 3)
                        #     ellipse = QGraphicsEllipseItem(v_from.x - 30, v_from.y - 30, 30, 30)
                        #     ellipse.setPen(pen)
                        #     self.scene.addItem(ellipse)
                        # else:
                        # print(self.graph.oriented)
                        if self.graph.oriented:
                            key = f'{v_from.name}_{v_to.name}'
                            if (key, node) in self.graph.edge_path.items():
                                pen = self.pathPen
                            else:
                                pen = self.greenPen
                            self.scene.addLine(v_from.x, v_from.y, node.x, node.y, self.pen)
                            self.scene.addLine(node.x, node.y, v_to.x, v_to.y, pen)

                            # self.scene.addItem(line1)
                            # self.scene.addItem(line2)
                            self.scene.addItem(GraphicsEdge(v_from, v_to, node, self.graph.oriented, weight))
                        elif int(v_from.name) > int(v_to.name):
                            key = f'{v_from.name}_{v_to.name}'
                            rev_key = f'{v_to.name}_{v_from.name}'
                            if (key in self.graph.edge_path and self.graph.edge_path[key] == weight)\
                                    or (rev_key in self.graph.edge_path and self.graph.edge_path[rev_key] == weight):
                                pen = self.pathPen
                            else:
                                pen = self.pen
                            self.scene.addLine(v_from.x, v_from.y, node.x, node.y, pen)
                            self.scene.addLine(node.x, node.y, v_to.x, v_to.y, pen)

                            # self.scene.addItem(line1)
                            # self.scene.addItem(line2)
                            self.scene.addItem(GraphicsEdge(v_from, v_to, node, self.graph.oriented, weight))

                except TypeError as e:
                    # print(e)
                    self.graph.restore()
                    self.drawGraph()
                except Exception as e:
                    print(e)
                    exit(-2)

        # рисуем вершины
        for v in self.graph.vertexes_coordinates.values():
            self.scene.addItem(GraphicsVertex(v))

    def simpleDrawGraph(self):
        self.scene.clear()
        for v_from, to_dict in self.graph.vertexes.items():
            v_from = self.graph.vertexes_coordinates[v_from]
            for v_to, to_list in to_dict.items():
                v_to = self.graph.vertexes_coordinates[v_to]
                for weight, node in to_list:
                    self.scene.addLine(v_from.x, v_from.y, v_to.x, v_to.y)

        # рисуем вершины
        for v in self.graph.vertexes_coordinates.values():
            self.scene.addItem(GraphicsVertex(v))
