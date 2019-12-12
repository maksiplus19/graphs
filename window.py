import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QAbstractItemView

from graph.graph import Graph
from graph.graphmodel import GraphModel
from graph.loadgraph import LoadGraph
from graph.savegraph import SaveGraph
from ui.design import BeginEndDialog
from ui.design.design import Ui_MainWindow
from ui.sourse.qgraphview import QGraphView
import algorithm


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
        self.action7.triggered.connect(self.addition)
        self.action8.triggered.connect(self.binary_operations)

    def addTab(self, name: str = None, graph: Graph = None):
        self.tabWidget.addTab(QGraphView(self.tabWidget, Graph() if graph is None else graph),
                              str(self.tabCounter) if name is None or name is False else name)
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)
        self.tabCounter += 1
        graph = self.tabWidget.currentWidget().graph
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
            LoadGraph.load_from_arc_list(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'gam':
            LoadGraph.load_from_adjacency_matrix(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'gim':
            LoadGraph.load_from_incidence_matrix(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'gal':
            LoadGraph.load_from_ribs_list(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'json':
            if not LoadGraph.load(self.tabWidget.currentWidget().graph, file_name):
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
            SaveGraph.save_as_vertexes_list(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'gam':
            SaveGraph.save_as_adjacency_matrix(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'gim':
            SaveGraph.save_as_incidence_matrix(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'gal':
            SaveGraph.save_as_ribs_list(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'json':
            SaveGraph.save(self.tabWidget.currentWidget().graph, file_name)
        elif file_type == 'png':
            SaveGraph.save_as_image(file_name, self.tabWidget.currentWidget().scene)
        else:
            QMessageBox.warning(self, 'Ошибка', f'Неизвестный формат файла "{file_type}"')
            return False
        self.tabWidget.currentWidget().graph.saved = True
        return True

    def undo(self):
        self.tabWidget.currentWidget().graph.undo()

    def redo(self):
        self.tabWidget.currentWidget().graph.redo()

    def changeOrient(self, data):
        self.tabWidget.currentWidget().graph.oriented = not bool(data)

        self.tabWidget.currentWidget().graph.update()

    def changeWeight(self, data):
        self.tabWidget.currentWidget().graph.weighted = not bool(data)
        self.tabWidget.currentWidget().graph.update()

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
        self.cmbDirect.setCurrentIndex(int(not self.tabWidget.currentWidget().graph.oriented))
        self.cmbWeight.setCurrentIndex(int(not self.tabWidget.currentWidget().graph.weighted))

    @get_begin_end
    def BFS(self, begin: str, end: str):
        return algorithm.BFS(self.tabWidget.currentWidget().graph, begin, end)

    @get_begin_end
    def A_star(self, begin: str, end: str):
        return algorithm.A_star(self.tabWidget.currentWidget().graph, begin, end)

    @get_begin_end
    def IDA(self, begin: str, end: str):
        return algorithm.IDA_star(self.tabWidget.currentWidget().graph, begin, end)

    def radius_other(self):
        return algoritm.radius(self.tabWidget.currentWidget().graph)

    def addition(self):
        self.textEdit.setText("")
        matrix = algorithm.additional(self.graphModel.matrix)
        is_full = True
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    is_full = False

        if is_full:
            self.textEdit.setText("Граф полный")
            return

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    if not self.tabWidget.currentWidget().graph.oriented and i < j:
                        break
                    self.tabWidget.currentWidget().graph.add_edge(str(i+1), str(j+1))
                if matrix[i][j] == 0:
                    self.tabWidget.currentWidget().graph.del_edge(str(i + 1), str(j + 1))


        self.tabWidget.currentWidget().graph.update()


    @two_graphs
    def check_isomorphic(self):
        index = self.tabWidget.count()
        res = algorithm.isomorphic(self.tabWidget.widget(index - 1).graph, self.tabWidget.widget(index - 2).graph)
        QMessageBox.information(self, 'Резкльтат', res)

    @two_graphs
    def binary_operations(self):
        bin_d = binaryDialog.Ui_BinaryDialog()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
