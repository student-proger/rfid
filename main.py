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
from key import key

def tohex(dec):
    """ Переводит десятичное число в 16-ричный вид с отбрасыванием `0x` """
    s = hex(dec).split('x')[-1]
    s = s.upper()
    if len(s) == 1:
        s = "0" + s
    return s


class RfidApp(QtWidgets.QMainWindow, mainform.Ui_MainWindow):
    """ Класс главного окна приложения """
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.buttonReadUID)
        self.pushButton_2.clicked.connect(self.buttonReadDump)
        self.textEdit.setReadOnly(True)

        self.card = rfidCard(vid = 0x1EAF, pid = 0x0030)

    def __del__(self):
        del(self.card)

    def buttonReadUID(self):
        res = self.card.readUID()
        if res == None:
            self.label.setText("Ошибка чтения")
            return

        res = list(map(tohex, res))
        self.label.setText(" ".join(res))
        self.textEdit.setHtml("")

    def buttonReadDump(self):
        res = self.card.readUID()
        if res == None:
            s = "<b>Ошибка чтения UID карты</b>"
            self.textEdit.setHtml(s)
            return

        res = list(map(tohex, res))
        self.label.setText(" ".join(res))
        s = " ".join(res) + '<br>'
        res = self.card.authBlock(3, [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5], KEYA)
        if not res:
            s = "<b>Ошибка аутентификации блока</b>"
            self.textEdit.setHtml(s)
            return
        res = list(map(tohex, self.card.readBlock(3)))
        if res == None:
            s = "<b>Ошибка чтения блока</b>"
            self.textEdit.setHtml(s)
            return
        s = s + " ".join(res) + '<br>'

        self.textEdit.setHtml(s)

    

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RfidApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
