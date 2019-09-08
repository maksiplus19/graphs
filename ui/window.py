import sys

from PyQt5.QtWidgets import QWidget, QApplication


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Графоид')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
