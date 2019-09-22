import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from graph.graph import Graph
from graph.vertex import Vertex
from graph.loadgraph import LoadGraph
from graph.savegraph import SaveGraph
from ui.design.design import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graph = Graph()
        self.graphView.set_graph(self.graph)

        # коннектим обработку нажатия кнопок меню
        self.actionOpen.triggered.connect(self.load_graph)
        self.actionSave.triggered.connect(self.save_graph)
        self.actionExit.triggered.connect(self.close)
        self.btnNext.clicked.connect(self.next)
        self.btnCancel.clicked.connect(self.undo)

    def load_graph(self):
        # получаем имя файла
        file_name = QFileDialog.getOpenFileName(self, 'Выбирите файл', 'C:\\Users\\admin\\PycharmProjects\\graphs',
                                                'JSON файлы (*.json)\n'
                                                'Матрица смежности  (*.gam)\n'
                                                'Матрица инцидентности (*.gim)\n'
                                                'Список дуг (*.gar)\n'
                                                'Список вершин (*.gal)\n'
                                                'Все файлы (*)')[0]
        if not file_name:
            return
        # вытаскиваем формат
        file_type = file_name.split('.')[-1]
        # LoadGraph.load(self.graph, file_name)
        # в зависимости от типа выбираем метод загрузки
        if file_type == 'gal':
            LoadGraph.load_from_arc_list(self.graph, file_name)
        elif file_type == 'gam':
            LoadGraph.load_from_adjacency_matrix(self.graph, file_name)
        elif file_type == 'gim':
            LoadGraph.load_from_incidence_matrix(self.graph, file_name)
        elif file_type == 'gar':
            LoadGraph.load_from_ribs_list(self.graph, file_name)
        elif file_type == 'json':
            print('here')
            LoadGraph.load(self.graph, file_name)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неизвестный формат файла')

        self.graphView.drawGraph()

    def save_graph(self):
        # получаем имя файла
        file_name = QFileDialog.getSaveFileName(self, 'Выбирите файл', 'C:\\Users\\admin\\PycharmProjects\\graphs',
                                                'Матрица смежности  (*.gam)\n'
                                                'Матрица инцидентности (*.gim)\n'
                                                'Список дуг (*.gar)\n'
                                                'Список вершин (*.gal)\n'
                                                'JSON файлы (*.json)')[0]
        if not file_name:
            return
        # вытаскиваем формат
        file_type = file_name.split('.')[-1]
        # LoadGraph.load(self.graph, file_name)
        # в зависимости от типа выбираем метод сохранения
        if file_type == 'gal':
            SaveGraph.save_as_vertexes_list(self.graph, file_name)
        if file_type == 'gam':
            SaveGraph.save_as_adjacency_matrix(self.graph, file_name)
        elif file_type == 'gim':
            SaveGraph.save_as_incidence_matrix(self.graph, file_name)
        elif file_type == 'gar':
            SaveGraph.save_as_ribs_list(self.graph, file_name)
        elif file_type == 'json':
            SaveGraph.save(self.graph, file_name)
        else:
            QMessageBox.warning(self, 'Ошибка', f'Неизвестный формат файла "{file_type}"')

    def undo(self):
        self.graph.undo()

    def next(self):
        self.graph.next()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
