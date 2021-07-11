import os
import sys
import time
from threading import Thread, Lock

# Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QInputDialog, QComboBox, QSystemTrayIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QMenu
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect
# design
import mainform

from rfidCard import rfidCard, KEYA, KEYB

def tohex(dec):
    """ Переводит десятичное число в 16-ричный вид с отбрасыванием `0x` """
    s = hex(dec).split('x')[-1]
    s = s.upper()
    if len(s) == 1:
        s = "0" + s
    return s

def isFirstBlock(n):
    if n % 4 == 0:
        return True
    else:
        return False

def isLastBlock(n):
    if (n + 1) % 4 == 0:
        return True
    else:
        return False


class RfidApp(QtWidgets.QMainWindow, mainform.Ui_MainWindow):
    """ Класс главного окна приложения """
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.buttonclick)

        self.card = rfidCard()

    def __del__(self):
        del(self.card)

    def buttonclick(self):
        res = list(map(tohex, self.card.readUID()))
        res = list(map(tohex, self.card.authBlock(3, [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5], KEYA)))
        res = list(map(tohex, self.card.readBlock(3)))
        self.label.setText(" ".join(res))

    

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RfidApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
