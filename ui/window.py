import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from graphs.graph.graph import Graph
from graphs.ui.design.design import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graph = Graph()
        self.load_graph()
        self.graphView.set_graph(self.graph)

        # коннектим обработку нажатия кнопок меню
        self.actionOpen.triggered.connect(self.load_graph)
        self.actionSave.triggered.connect(self.save_graph)

    def load_graph(self):
        # получаем имя файла
        file_name = QFileDialog.getOpenFileName(self, 'Выбирите файл', 'C:\\Users\\admin\\PycharmProjects\\graphs',
                                             'Graph Files (*.gal *.gam *.gim *gar)')[0]
        # вытаскиваем формат
        file_type = file_name.split('.')[-1]
        # в зависимости от типа выбираем метод загрузки
        if file_type == 'gal':
            self.graph.load_from_adjacency_list(file_name)
        elif file_type == 'gam':
            self.graph.load_from_adjacency_matrix(file_name)
        elif file_name == 'gim':
            self.graph.load_from_incidence_matrix(file_name)
        elif file_name == 'gar':
            self.graph.load_from_arc_list(file_name)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неизвестный формат файла')

    def save_graph(self):
        print('save')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
