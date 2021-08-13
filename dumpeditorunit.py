# Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QInputDialog, QComboBox
from PyQt5.QtWidgets import QMessageBox, QWidget, QMenu
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect
# design
import dumpeditorform

def tohex(dec):
    """ Переводит десятичное число в 16-ричный вид с отбрасыванием `0x` """
    s = hex(dec).split('x')[-1]
    s = s.upper()
    if len(s) == 1:
        s = "0" + s
    return s

class dumpEditorForm(QtWidgets.QDialog, dumpeditorform.Ui_Dialog):
    def __init__(self, dump):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.tableWidget.clear()
        self.setWindowTitle("Редактор дампа")
        self.tableWidget.setFont(QFont("Consolas", 10))
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(64)
        self.tableWidget.setHorizontalHeaderLabels(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"])
        self.tableWidget.setVerticalHeaderLabels(list(map(str, [i for i in range(0, 64)])))
        self.tableWidget.cellChanged.connect(self.cellChangeEvent)
        self.blockCheck = True

        for i in range(0, 64):
            for j in range(0, 16):
                self.tableWidget.setItem(i, j, QTableWidgetItem(tohex(dump[i][j])))

        self.paintBackground()

        self.blockCheck = False
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def paintBackground(self):
        for i in range(0, 64):
            for j in range(0, 16):
                self.tableWidget.item(i, j).setBackground(QColor(255, 255, 255))
        for j in range(0, 16):
            self.tableWidget.item(0, j).setBackground(QColor(255, 0, 0))
        for i in range(0, 64):
            if i % 4 == 3:
                for j in range(0, 6):
                    self.tableWidget.item(i, j).setBackground(QColor(139, 233, 167))
                for j in range(10, 16):
                    self.tableWidget.item(i, j).setBackground(QColor(139, 233, 167))
                for j in range(6, 9):
                    self.tableWidget.item(i, j).setBackground(QColor(249, 170, 174))

    def cellChangeEvent(self, row, column):
        """Событие вызывается при редактировании ячейки.

        :param row: строка
        :param column: столбец
        """
        if self.blockCheck:
            return

        sender = self.sender()
        s = sender.item(row, column).text().strip().upper()
        if len(s) == 0:
            s = "00"
        elif len(s) == 1:
            s = "0" + s
        elif len(s) == 2:
            pass
        else:
            s = "00"
        # Проверяем на валидность
        try:
            tt = int(s, 16)
        except ValueError:
            s = "00"

        self.blockCheck = True
        self.tableWidget.setItem(row, column, QTableWidgetItem(s))
        self.paintBackground()
        self.blockCheck = False
