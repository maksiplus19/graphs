# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BeginEndDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog


class Ui_BeginEndDialog(QDialog):
    def __init__(self, parent):
        try:
            super().__init__()
        except Exception as e:
            print(e)
            exit(-3)
        self.setParent(parent)
        self.setupUi()
        self.textEnd = None
        self.textBegin = None

    def setupUi(self):
        self.setObjectName("BeginEndDialog")
        self.resize(363, 113)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.begin = QtWidgets.QSpinBox(self)
        self.begin.setMinimum(1)
        self.begin.setMaximum(100000)
        self.begin.setObjectName("begin")
        self.gridLayout.addWidget(self.begin, 1, 0, 1, 1)
        self.end = QtWidgets.QSpinBox(self)
        self.end.setMinimum(1)
        self.end.setMaximum(100000)
        self.end.setObjectName("end")
        self.gridLayout.addWidget(self.end, 1, 1, 1, 1)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.run)
        self.buttonBox.rejected.connect(self.stop)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("BeginEndDialog", "Выбор начала и конца"))
        self.label.setText(_translate("BeginEndDialog", "Начало"))
        self.label_2.setText(_translate("BeginEndDialog", "Конец"))

    def run(self):
        if self.begin.text().isdigit():
            self.textBegin = self.begin.text()
        if self.end.text().isdigit():
            self.textEnd = self.end.text()
        self.accept()

    def stop(self):
        self.textBegin = None
        self.textEnd = None
        self.reject()

