# Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QInputDialog, QComboBox
from PyQt5.QtWidgets import QMessageBox, QWidget, QMenu
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect
# design
import logform

class logForm(QtWidgets.QDialog, logform.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.log.setFont(QFont("Consolas", 10))
        self.log.setReadOnly(True)
        self.buf = ""
        self.log.setHtml("")

    def clear(self):
        self.buf = ""
        self.log.setHtml("")

    def add(self, msg, error = False):
        """ Добавление строки в лог """
        if error:
            self.buf = self.buf + '<font color="#FF0000">' + msg + "</font><br>"
        else:
            self.buf = self.buf + msg + "<br>"
        self.log.setHtml(self.buf)
