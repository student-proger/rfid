# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dumpeditorform.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(568, 529)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 490, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 411, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.fillButton = QtWidgets.QPushButton(Dialog)
        self.fillButton.setGeometry(QtCore.QRect(430, 10, 121, 23))
        self.fillButton.setObjectName("fillButton")
        self.replaceButton = QtWidgets.QPushButton(Dialog)
        self.replaceButton.setGeometry(QtCore.QRect(430, 40, 121, 23))
        self.replaceButton.setObjectName("replaceButton")
        self.factoryButton = QtWidgets.QPushButton(Dialog)
        self.factoryButton.setGeometry(QtCore.QRect(430, 90, 121, 23))
        self.factoryButton.setObjectName("factoryButton")
        self.ndefButton = QtWidgets.QPushButton(Dialog)
        self.ndefButton.setGeometry(QtCore.QRect(430, 120, 121, 23))
        self.ndefButton.setObjectName("ndefButton")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.fillButton.setText(_translate("Dialog", "Заполнить..."))
        self.replaceButton.setText(_translate("Dialog", "Заменить..."))
        self.factoryButton.setText(_translate("Dialog", "Заводской шаблон"))
        self.ndefButton.setText(_translate("Dialog", "NDEF шаблон"))
