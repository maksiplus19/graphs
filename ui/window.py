# -*- coding: utf-8 -*-
import sys
from copy import deepcopy
from datetime import datetime
from typing import cast

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QAbstractItemView

import algorithm
from graph.graph import Graph
from graph.graphmodel import GraphModel
from graph.loadgraph import LoadGraph
from graph.savegraph import SaveGraph
from ui.design import BeginDialog
from ui.design import BeginEndDialog
from ui.design.GetTextDialog import Ui_GetTextDialog
from ui.design.binaryDialog import Ui_BinaryDialog
from ui.design.design import Ui_MainWindow
from ui.sourse.qgraphview import QGraphView


def get_begin_end(method):
    def warped(self):
        dialog = BeginEndDialog.Ui_BeginEndDialog(None)
        dialog.setModal(True)
        if not dialog.exec_():
            return
        if dialog.textBegin is None or dialog.textEnd is None:
            return

        distance = method(self, dialog.textBegin, dialog.textEnd)

        self.textEdit.setText(f'Расстояние от {dialog.textBegin} до {dialog.textEnd} = {distance}')
        self.tabWidget.currentWidget().graph.update()

    return warped


def two_graphs(method):
    def warped(self, *args, **kwargs):
        if self.tabWidget.count() < 2:
            QMessageBox.information(self, 'Информация', 'Этот алгоритм требует 2 графов')
            return
        method(self)

    return warped


def get_begin(method):
    def warped(self):
        self.textEdit.setText("")
        dialog = BeginDialog.Ui_BeginDialog(None)
        dialog.setModal(True)
        if not dialog.exec_():
            return
        if dialog.textBegin is None:
            return
        if dialog.textBegin == '0':
            for i in range(len(self.graph.vertexes)):
                distance = method(self, str(i + 1))
                for j in range(len(distance)):
                    self.textEdit.append(f'Расстояние от {i + 1} до {j + 1} = {distance[j]}')
            self.graph.update()
            return

        distance = method(self, dialog.textBegin)

        for i in range(len(distance)):
            self.textEdit.append(f'Расстояние от {dialog.textBegin} до {i + 1} = {distance[i]}')
        self.graph.update()

    return warped


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        icon = QIcon('C:\\Users\\viktor\\PycharmProjects\\graphs\\graph.ico')
        self.setWindowIcon(icon)
        self.tabCounter = 1

        self.graphModel = GraphModel()
        self.graphMatrix.setModel(self.graphModel)
        self.graphMatrix.setEditTriggers(QAbstractItemView.AllEditTriggers)

        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)
        self.addTab()
        self.tabWidget.setTabsClosable(True)

        # коннектим обработку нажатия кнопок меню
        self.actionOpen.triggered.connect(self.load_graph)
        self.actionSave.triggered.connect(self.save_graph)
        self.actionExit.triggered.connect(self.close)
        self.actionNewTab.triggered.connect(self.addTab)

        self.btnNext.clicked.connect(self.redo)
        self.btnCancel.clicked.connect(self.undo)

        self.actionProgram.triggered.connect(self.open_program)
        self.actionAuthor.triggered.connect(self.open_author)

        self.cmbDirect.currentIndexChanged.connect(self.changeOrient)
        self.cmbWeight.currentIndexChanged.connect(self.changeWeight)

        self.tabWidget.currentChanged.connect(self.tabChange)
        self.tabWidget.tabCloseRequested.connect(self.tabClose)

        self.BFSaction.triggered.connect(self.BFS)
        self.actionA.triggered.connect(self.A_star)
        self.IDAaction.triggered.connect(self.IDA)
        self.action5.triggered.connect(self.check_isomorphic)
        self.action.triggered.connect(self.dijkstra)
        self.action_2.triggered.connect(self.floyd_worshel)
        self.action_3.triggered.connect(self.bellman_ford)
        self.action4.triggered.connect(self.radius_diametr)
        self.action_4.triggered.connect(self.djonson)
        self.action7.triggered.connect(self.addition)
        self.action8.triggered.connect(self.binary_operations)
        self.action6.triggered.connect(self.is_connect)
        self.action11.triggered.connect(self.extreme)
        self.action14.triggered.connect(self.coloring)
        self.action_5.triggered.connect(self.prima)
        self.action_6.triggered.connect(self.kruscal)
        self.action_7.triggered.connect(self.boruvki)
        self.action13.triggered.connect(self.cycles)
        self.action17.triggered.connect(self.complex_from_vector)
        self.action21.triggered.connect(self.test_efficiency)
        self.action9.triggered.connect(self.is_planary)
        self.action19.triggered.connect(self.salesman)
        self.action16.triggered.connect(self.addition_complex2)

    def addTab(self, name: str = None, graph: Graph = None):
        self.textEdit.setText("")
        self.tabWidget.addTab(QGraphView(self.tabWidget, Graph() if graph is None else graph),
                              str(self.tabCounter) if name is None or name is False else name)
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
        self.tabCounter += 1
        graph = self.graph
        self.graphModel.setGraph(graph)
        graph.signals.update.connect(self.graphModel.graphToMatrix)
        graph.signals.update.connect(self.graphMatrix.resizeColumnsToContents)
        graph.update()
        graph.saved = True
        # for i in range(10**4):
        #     graph.add_vertex(graph.get_new_vertex_name())
        #     if i % 100 == 0:
        #         print(i)

    def tabChange(self, index: int):
        if self.tabWidget.widget(index) is None:
            return
        graph = self.tabWidget.widget(index).graph
        self.graphModel.setGraph(graph)
        graph.signals.update.connect(self.graphModel.graphToMatrix)
        graph.signals.update.connect(self.graphMatrix.resizeColumnsToContents)
        self.setComboBox()
        self.graphMatrix.reset()

    def tabClose(self, index: int):
        graph = self.tabWidget.widget(index).graph
        if not graph.saved:
            message_box = QMessageBox(self)
            message_box.setText('В закрываемой вкладке содержиться несохраненный граф')
            message_box.setInformativeText('Хотите его сохранить?')
            message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            message_box.setDefaultButton(QMessageBox.Save)

            res = message_box.exec()

            if QMessageBox.Save == res:
                if not self.save_graph():
                    return
            elif QMessageBox.Cancel == res:
                return
        self.tabWidget.removeTab(index)

    def load_graph(self):
        # получаем имя файла
        file_name = QFileDialog.getOpenFileName(self, 'Выбирите файл', 'C:\\Users\\admin\\PycharmProjects\\graphs',
                                                'JSON файлы (*.json)\n'
                                                'Матрица смежности  (*.gam)\n'
                                                'Матрица инцидентности (*.gim)\n'
                                                'Список дуг (*.gal)\n'
                                                'Список вершин (*.gvl)\n'
                                                'Все файлы (*.*)')[0]
        if not file_name:
            return
        # вытаскиваем формат
        file_type = file_name.split('.')[-1]
        self.addTab()
        # LoadGraph.load(self.graph, file_name)
        # в зависимости от типа выбираем метод загрузки
        if file_type == 'gvl':
            LoadGraph.load_from_arc_list(self.graph, file_name)
        elif file_type == 'gam':
            LoadGraph.load_from_adjacency_matrix(self.graph, file_name)
        elif file_type == 'gim':
            LoadGraph.load_from_incidence_matrix(self.graph, file_name)
        elif file_type == 'gal':
            LoadGraph.load_from_ribs_list(self.graph, file_name)
        elif file_type == 'json':
            if not LoadGraph.load(self.graph, file_name):
                QMessageBox.critical(self, 'Ошибка файла', 'Файл не корректен')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неизвестный формат файла')

        self.setComboBox()

    def save_graph(self):
        # получаем имя файла
        file_name = QFileDialog.getSaveFileName(self, 'Выбирите файл', 'C:\\Users\\admin\\PycharmProjects\\graphs',
                                                'Матрица смежности  (*.gam)\n'
                                                'Матрица инцидентности (*.gim)\n'
                                                'Список дуг (*.gal)\n'
                                                'Список вершин (*.gvl)\n'
                                                'JSON файлы (*.json)\n'
                                                'Изображение (*.png)')[0]
        if not file_name:
            return False
        # вытаскиваем формат
        file_type = file_name.split('.')[-1]
        # LoadGraph.load(self.graph, file_name)
        # в зависимости от типа выбираем метод сохранения
        if file_type == 'gvl':
            SaveGraph.save_as_vertexes_list(self.graph, file_name)
        elif file_type == 'gam':
            SaveGraph.save_as_adjacency_matrix(self.graph, file_name)
        elif file_type == 'gim':
            SaveGraph.save_as_incidence_matrix(self.graph, file_name)
        elif file_type == 'gal':
            SaveGraph.save_as_ribs_list(self.graph, file_name)
        elif file_type == 'json':
            SaveGraph.save(self.graph, file_name)
        elif file_type == 'png':
            SaveGraph.save_as_image(file_name, self.scene)
        else:
            QMessageBox.warning(self, 'Ошибка', f'Неизвестный формат файла "{file_type}"')
            return False
        self.graph.saved = True
        return True

    def undo(self):
        self.graph.undo()

    def redo(self):
        self.graph.redo()

    def changeOrient(self, data):
        self.graph.oriented = not bool(data)

        self.graph.update()

    def changeWeight(self, data):
        self.graph.weighted = not bool(data)
        self.graph.update()

    def open_program(self):
        QMessageBox.information(self, "Информация", "Программа предоставляет интерфейс для работы с графом."
                                                    " Есть возможнсть добавить граф с файла(матрица смежности и "
                                                    "инцидентности, список вершин и ребер), а также нарисовать граф. "
                                                    "Программа является базовым инструментом для дальнейших "
                                                    "лабораторных работ.")

    def open_author(self):
        QMessageBox.information(self, "Информация", "М8О-312Б-17 Комаров Виктор\nМ8О-313Б-17 Безенков Савелий"
                                                    "\nМ8О-312Б-17 Якупова Айгуль")

    def setComboBox(self):
        self.cmbDirect.setCurrentIndex(int(not self.graph.oriented))
        self.cmbWeight.setCurrentIndex(int(not self.graph.weighted))
        self.graph.update()

    @get_begin_end
    def BFS(self, begin: str, end: str):
        return algorithm.BFS(self.graph, begin, end)

    @get_begin_end
    def A_star(self, begin: str, end: str):
        return algorithm.A_star(self.graph, begin, end)

    @get_begin_end
    def IDA(self, begin: str, end: str):
        return algorithm.IDA_star(self.graph, begin, end)

    @two_graphs
    def check_isomorphic(self):
        index = self.tabWidget.count()
        res = algorithm.isomorphic(self.tabWidget.widget(index - 1).graph, self.tabWidget.widget(index - 2).graph)
        QMessageBox.information(self, 'Резкльтат', res)

    @two_graphs
    def binary_operations(self):
        bin_d = Ui_BinaryDialog()
        bin_d.exec_()
        if bin_d.getOperation() == '':
            return
        op = bin_d.getOperation()
        index = self.tabWidget.count()
        first, second = self.tabWidget.widget(index - 2).graph, self.tabWidget.widget(index - 1).graph
        if op != 'aallb':
            if op[0] == 'b':
                first, second = second, first
            res = algorithm.binary_operation(first, second, op[1:-1])
            self.addTab('Результат', res)
        else:
            all_op = ['aandb', 'aorb', 'aminusb', 'bminusa',
                      'aimplb', 'bimpla', 'acoimplb', 'bcoimpla',
                      'axorb', 'aeqb', 'ashephb', 'apirsb']
            for op in all_op:
                if op[0] == 'b':
                    res = algorithm.binary_operation(second, first, op[1:-1])
                else:
                    res = algorithm.binary_operation(first, second, op[1:-1])
                self.addTab(op, res)

    @get_begin
    def dijkstra(self, begin: str):
        return algorithm.dijkstra(begin, self.graph.to_matrix())

    def floyd_worshel(self):
        self.textEdit.setText("")
        result = algorithm.floydWorshel(self.graph.to_matrix(), self.graph.oriented)
        for i in range(len(result)):
            for j in range(len(result)):
                self.textEdit.append(f'Расстояние от {i + 1} до {j + 1} = {result[i][j]}')
                self.graph.update()

    @get_begin
    def bellman_ford(self, begin: str):
        return algorithm.bellmanFord(self.graph, begin)

    def djonson(self):
        self.textEdit.setText("")
        for i in range(len(self.graph.vertexes)):
            distance = algorithm.dijkstra(str(i + 1), self.graph.to_matrix())
            for j in range(len(distance)):
                self.textEdit.append(f'Расстояние от {i + 1} до {j + 1} = {distance[j]}')
        self.graph.update()

    def radius_diametr(self):
        self.textEdit.setText("")
        with open("res.txt", "w", encoding='utf8') as f:
            size = self.graph.size()
            ecscentr = []
            for i in range(size):
                dist = algorithm.dijkstra(str(i + 1), self.graph.to_matrix())
                maximum = np.inf * -1
                for j in range(len(dist)):
                    if dist[j] > maximum:
                        maximum = dist[j]
                ecscentr.append(maximum)
            self.textEdit.append(f'Эксцентриситеты: {ecscentr}')
            f.write(f'Эксцентриситеты: {str(ecscentr)}\n')
            diam = np.inf * -1
            rad = np.inf
            for i in range(len(ecscentr)):
                if ecscentr[i] > diam:
                    diam = ecscentr[i]
                if ecscentr[i] < rad:
                    rad = ecscentr[i]

            if diam == np.inf:
                self.textEdit.append(f'Граф не связный')
            else:
                self.textEdit.append(f'Диаметр = {diam}')
                self.textEdit.append(f'Радиус = {rad}')
            f.write(f'Диаметр = {str(diam)}\n')
            f.write(f'Радиус = {str(rad)}\n')

            matrix = self.graph.to_matrix()
            degrees = np.zeros(size)
            for i in range(len(matrix)):
                for j in range(len(matrix)):
                    if matrix[i][j] != 0:
                        degrees[i] += 1
                        degrees[j] += 1
            if not self.graph.oriented:
                for i in range(len(degrees)):
                    degrees[i] = degrees[i] // 2
            self.textEdit.append(f'Вектор степеней: {degrees}')
            f.write(f'Вектор степеней: {str(degrees)}\n')

    def addition(self):
        self.textEdit.setText("")
        matrix = algorithm.additional(self.graph.to_matrix(with_weight=False))
        matrix_copy = deepcopy(matrix)
        for i in range(len(matrix_copy)):
            matrix[i][i] = 0

        is_full = not any(sum(matrix_copy, []))
        if is_full:
            self.textEdit.setText("Граф полный")
            return

        g = Graph.from_matrix(matrix)
        g.oriented = self.graph.oriented
        g.vertexes_coordinates = deepcopy(self.graph.vertexes_coordinates)
        self.graph = g
        self.graphModel.setGraph(g)
        g.update()
        self.tabWidget.currentWidget().drawGraph()

    def is_connect(self):
        self.textEdit.setText(algorithm.isConnected(self.graph.to_matrix(),
                                                    self.graph.oriented))
        comps = algorithm.find_comps(self.graph)
        if self.graph.oriented:
            self.textEdit.append("Компоненты сильной связности:")
        else:
            self.textEdit.append("Компоненты связности:")
        for i in comps:
            self.textEdit.append(str(i))

        bridges, hinges = algorithm.find_bridges(self.tabWidget.currentWidget().graph)

        self.textEdit.append("Мосты:")
        self.textEdit.append(str(bridges))
        # for i in bridges:
        #     self.textEdit.append(i)
        self.textEdit.append("Шарниры:")
        self.textEdit.append(str(hinges))

    def extreme(self):
        dialog = Ui_GetTextDialog('База', 'Введите базу')
        if not dialog.exec_():
            return
        base1 = dialog.getText()
        dialog = Ui_GetTextDialog('База', 'Введите базу')
        if not dialog.exec_():
            return

        base2 = dialog.getText()

        res = algorithm.extreme(base1, base2)
        if res is None:
            QMessageBox.information(self, 'Ошибка', 'Ошибка')
            return

        for name, graph in res.items():
            self.addTab(name, graph)

    def coloring(self):
        g = self.graph
        chromatic_number = algorithm.coloring(g)
        self.textEdit.setText(f'Хроматическое число {chromatic_number}')
        g.update()

    def prima(self):
        g = self.graph
        res = algorithm.prima(g.to_matrix(), g.oriented)
        if res == "Граф ориентированный" or res == "Граф не связный":
            self.textEdit.setText(res)
        else:
            self.addTab("prima", res)

    def kruscal(self):
        res = algorithm.kruscal(self.graph)
        if res == "Граф ориентированный" or res == "Граф не связный":
            self.textEdit.setText(res)
        else:
            self.addTab("kruscal", res)

    def boruvki(self):
        res = algorithm.boruvki(self.graph)
        if res == "Граф ориентированный" or res == "Граф не связный":
            self.textEdit.setText(res)
        else:
            self.addTab("boruvki", res)

    def cycles(self):
        if not algorithm.isCycled(self.graph):
            self.textEdit.setText("Циклов нет")
            centres, depth = algorithm.find_center(self.graph)
            if depth is None:
                self.textEdit.setText(str(centres))
                return
            self.textEdit.append("Центры:")
            self.textEdit.append(str(centres))
            self.textEdit.append("Глубина = " + str(depth))
            prufer = algorithm.to_prufer(self.graph)
            if prufer:
                self.textEdit.append("Код Прюфера:")
                self.textEdit.append(str(prufer))
        else:
            mincycle = algorithm.find_mincycle(self.graph)
            for i in mincycle:
                self.graph.vertexes_coordinates[str(i)].color = QColor(100, 191, 46)
            self.tabWidget.currentWidget().graph.update()
            self.textEdit.setText("Минимальный цикл:")
            self.textEdit.append(str(mincycle))

    def is_planary(self):
        res = algorithm.isPlanary(self.graph)
        self.textEdit.setText(res[0])
        self.textEdit.append(res[1])

    def addition_complex2(self):
        dialog = Ui_GetTextDialog('2-комплекс', 'Введите вектор степеней 2-комплекса')
        if not dialog.exec_():
            return
        text: str = dialog.getText()
        text: list = cast(list, text.split(' '))
        text: list = list(map(int, text))
        res = algorithm.addition_complex2(text)
        if not res["addition_triples"]:
            text = f'Гипер граф полный\n{res["triples"]}\n'
        else:
            text = f'Гипер граф\n{res["triples"]}\n' \
                   f'Дополнение\n{res["addition_triples"]}\n'
        QMessageBox.information(self, 'Результат', text)


    @property
    def graph(self) -> Graph:
        return self.tabWidget.currentWidget().graph

    def complex_from_vector(self):
        dialog = Ui_GetTextDialog('Вектор гиперграфа', 'Введите вектор гиперграфа')
        if not dialog.exec_():
            return
        text: str = dialog.getText()
        text: list = cast(list, text.split(' '))
        d = None
        try:
            d = algorithm.get_complex_from_vector(list(map(int, text)))
        except ValueError:
            QMessageBox.critical(self, 'Ошибка', 'Не получилось преобразовать в вектор чисел')
            return
        if d is None:
            QMessageBox.information(self, 'Ошибка', 'Не возможно реализовать вектор')
            return
        text = f'{d["triples"]}\nГипер граф{" не" if not d["complete"] else ""} совершенный\n' \
               f'Граф{" не" if not d["extreme"] else ""} экстремальный\n'
        if d['extreme']:
            text += str(d['base'])
        QMessageBox.information(self, 'Результат', text)

    def test_efficiency(self):
        start = datetime.now()
        algorithm.compare_efficiency(self.tabWidget)
        QMessageBox.information(self, 'Сообщение', f'Сравнение алгоритмов завершено\n'
                                                   f'Всего затрачено времени {datetime.now() - start}')

    def salesman(self):
        algorithm.salesman(self.graph)
        self.graph.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
