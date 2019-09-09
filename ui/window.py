import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from graph.graph import Graph
from ui.design.design import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__graph = Graph()
        self.__graph.load_from_adjacency_list('C:\\Users\\maksi\\PycharmProjects\\graphs\\test.txt')
        self.draw_graph()

    def draw_graph(self):
        self.graphView.drawGraph(self.__graph)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
