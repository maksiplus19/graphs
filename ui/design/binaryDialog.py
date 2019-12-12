# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'binaryDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_BinaryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.aAndB.clicked.connect(self.aAndBF)
        self.aOrB.clicked.connect(self.aOrBF)
        self.aMinusB.clicked.connect(self.aMinusBF)
        self.bMinusA.clicked.connect(self.bMinusAF)
        self.aImpB.clicked.connect(self.aImpBF)
        self.bImpA.clicked.connect(self.bImpAF)
        self.aCoimpB.clicked.connect(self.aCoimpBF)
        self.bCoimpA.clicked.connect(self.bCoimpAF)
        self.aXorB.clicked.connect(self.aXorBF)
        self.aEqB.clicked.connect(self.aEqBF)
        self.sheph.clicked.connect(self.shephF)
        self.pirs.clicked.connect(self.pirsF)
        self.allOperations.clicked.connect(self.allOper)
        self.op: str = ''

    def setupUi(self):
        self.setObjectName("BinaryDialog")
        self.resize(398, 350)
        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.aOrB = QtWidgets.QPushButton(self)
        self.aOrB.setObjectName("aOrB")
        self.gridLayout_2.addWidget(self.aOrB, 1, 0, 1, 1)
        self.bMinusA = QtWidgets.QPushButton(self)
        self.bMinusA.setObjectName("bMinusA")
        self.gridLayout_2.addWidget(self.bMinusA, 2, 1, 1, 1)
        self.aImpB = QtWidgets.QPushButton(self)
        self.aImpB.setObjectName("aImpB")
        self.gridLayout_2.addWidget(self.aImpB, 3, 0, 1, 1)
        self.pirs = QtWidgets.QPushButton(self)
        self.pirs.setObjectName("pirs")
        self.gridLayout_2.addWidget(self.pirs, 8, 0, 1, 1)
        self.sheph = QtWidgets.QPushButton(self)
        self.sheph.setObjectName("sheph")
        self.gridLayout_2.addWidget(self.sheph, 7, 0, 1, 1)
        self.aAndB = QtWidgets.QPushButton(self)
        self.aAndB.setObjectName("aAndB")
        self.gridLayout_2.addWidget(self.aAndB, 0, 0, 1, 1)
        self.aXorB = QtWidgets.QPushButton(self)
        self.aXorB.setObjectName("aXorB")
        self.gridLayout_2.addWidget(self.aXorB, 5, 0, 1, 1)
        self.bImpA = QtWidgets.QPushButton(self)
        self.bImpA.setObjectName("bImpA")
        self.gridLayout_2.addWidget(self.bImpA, 3, 1, 1, 1)
        self.aEqB = QtWidgets.QPushButton(self)
        self.aEqB.setObjectName("aEqB")
        self.gridLayout_2.addWidget(self.aEqB, 6, 0, 1, 1)
        self.aMinusB = QtWidgets.QPushButton(self)
        self.aMinusB.setObjectName("aMinusB")
        self.gridLayout_2.addWidget(self.aMinusB, 2, 0, 1, 1)
        self.aCoimpB = QtWidgets.QPushButton(self)
        self.aCoimpB.setObjectName("aCoimpB")
        self.gridLayout_2.addWidget(self.aCoimpB, 4, 0, 1, 1)
        self.bCoimpA = QtWidgets.QPushButton(self)
        self.bCoimpA.setObjectName("bCoimpA")
        self.gridLayout_2.addWidget(self.bCoimpA, 4, 1, 1, 1)
        self.allOperations = QtWidgets.QPushButton(self)
        self.allOperations.setObjectName("allOperations")
        self.gridLayout_2.addWidget(self.allOperations, 8, 1, 1, 1)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, BinaryDialog):
        _translate = QtCore.QCoreApplication.translate
        BinaryDialog.setWindowTitle(_translate("BinaryDialog", "Бинарные операции"))
        self.aOrB.setText(_translate("BinaryDialog", "A или B"))
        self.bMinusA.setText(_translate("BinaryDialog", "B - A"))
        self.aImpB.setText(_translate("BinaryDialog", "A => B"))
        self.pirs.setText(_translate("BinaryDialog", "A пирс B"))
        self.sheph.setText(_translate("BinaryDialog", "A шефер B"))
        self.aAndB.setText(_translate("BinaryDialog", "A и B"))
        self.aXorB.setText(_translate("BinaryDialog", "A ^ B"))
        self.bImpA.setText(_translate("BinaryDialog", "B => A"))
        self.aEqB.setText(_translate("BinaryDialog", "A = B"))
        self.aMinusB.setText(_translate("BinaryDialog", "A - B"))
        self.aCoimpB.setText(_translate("BinaryDialog", "A <= B"))
        self.bCoimpA.setText(_translate("BinaryDialog", "B <= A"))
        self.allOperations.setText(_translate("BinaryDialog", "Все опреации"))

    def aAndBF(self):
        self.op = 'aandb'
        self.accept()

    def aOrBF(self):
        self.op = 'aorb'
        self.accept()

    def aMinusBF(self):
        self.op = 'aminusb'
        self.accept()

    def bMinusAF(self):
        self.op = 'bminusa'
        self.accept()

    def aImpBF(self):
        self.op = 'aimplb'
        self.accept()

    def bImpAF(self):
        self.op = 'bimpla'
        self.accept()

    def aCoimpBF(self):
        self.op = 'acoimplb'
        self.accept()

    def bCoimpAF(self):
        self.op = 'bcoimpla'
        self.accept()

    def aXorBF(self):
        self.op = 'axorb'
        self.accept()

    def aEqBF(self):
        self.op = 'aeqb'
        self.accept()

    def shephF(self):
        self.op = 'ashephb'
        self.accept()

    def pirsF(self):
        self.op = 'apirsb'
        self.accept()

    def getOperation(self):
        return self.op

    def allOper(self):
        self.op = 'aallb'
        self.accept()
