# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126, 702)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphView = QGraphView(self.centralwidget)
        self.graphView.setObjectName("graphView")
        self.horizontalLayout.addWidget(self.graphView)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1126, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_graph = QtWidgets.QMenu(self.menubar)
        self.menu_graph.setObjectName("menu_graph")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_tasks = QtWidgets.QAction(MainWindow)
        self.action_tasks.setObjectName("action_tasks")
        self.action_question = QtWidgets.QAction(MainWindow)
        self.action_question.setObjectName("action_question")
        self.action_open_graph = QtWidgets.QAction(MainWindow)
        self.action_open_graph.setObjectName("action_open_graph")
        self.action_save_graph = QtWidgets.QAction(MainWindow)
        self.action_save_graph.setObjectName("action_save_graph")
        self.menu_file.addAction(self.action_tasks)
        self.menu_file.addAction(self.action_question)
        self.menu_graph.addAction(self.action_open_graph)
        self.menu_graph.addAction(self.action_save_graph)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_graph.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Графоид"))
        self.menu_file.setTitle(_translate("MainWindow", "Файл"))
        self.menu_graph.setTitle(_translate("MainWindow", "Граф"))
        self.action_tasks.setText(_translate("MainWindow", "Задачи теории графов"))
        self.action_question.setText(_translate("MainWindow", "?"))
        self.action_open_graph.setText(_translate("MainWindow", "Открыть из файла"))
        self.action_save_graph.setText(_translate("MainWindow", "Сохранить из файла"))


from ui.sourse.qgraphview import QGraphView
