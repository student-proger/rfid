# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(872, 567)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 131, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 40, 331, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 70, 551, 431))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 10, 131, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 500, 551, 23))
        self.progressBar.setMaximum(64)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.keyTable = QtWidgets.QTableWidget(self.centralwidget)
        self.keyTable.setGeometry(QtCore.QRect(570, 70, 291, 431))
        self.keyTable.setObjectName("keyTable")
        self.keyTable.setColumnCount(2)
        self.keyTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.keyTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.keyTable.setHorizontalHeaderItem(1, item)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(310, 10, 101, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 10, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 872, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_saveDump = QtWidgets.QAction(MainWindow)
        self.action_saveDump.setObjectName("action_saveDump")
        self.action_readDump = QtWidgets.QAction(MainWindow)
        self.action_readDump.setObjectName("action_readDump")
        self.action_readUID = QtWidgets.QAction(MainWindow)
        self.action_readUID.setObjectName("action_readUID")
        self.action_readMemory = QtWidgets.QAction(MainWindow)
        self.action_readMemory.setObjectName("action_readMemory")
        self.menu.addAction(self.action_readUID)
        self.menu.addAction(self.action_readMemory)
        self.menu_2.addAction(self.action_saveDump)
        self.menu_2.addAction(self.action_readDump)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Чтение UID"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Чтение дампа"))
        item = self.keyTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "KEY A"))
        item = self.keyTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "KEY B"))
        self.pushButton_3.setText(_translate("MainWindow", "Права доступа"))
        self.pushButton_4.setText(_translate("MainWindow", "Сохранить"))
        self.menu.setTitle(_translate("MainWindow", "Карта"))
        self.menu_2.setTitle(_translate("MainWindow", "Дамп"))
        self.action_saveDump.setText(_translate("MainWindow", "Сохранить в файл..."))
        self.action_readDump.setText(_translate("MainWindow", "Загрузить из файла..."))
        self.action_readUID.setText(_translate("MainWindow", "Прочитать UID"))
        self.action_readMemory.setText(_translate("MainWindow", "Считать содержимое памяти"))
