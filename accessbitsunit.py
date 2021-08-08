# Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QInputDialog, QComboBox
from PyQt5.QtWidgets import QMessageBox, QWidget, QMenu
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect
# design
import accessbitsform

from rfidCard import rfidCard
from rfidCard import KEYA, KEYB, TB_SECTOR_TRAILER, TB_DATABLOCK_0, TB_DATABLOCK_1, TB_DATABLOCK_2, TB_UID

class accessBitsForm(QtWidgets.QDialog, accessbitsform.Ui_Dialog):
    def __init__(self, card):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.textEdit.setReadOnly(True)
        self.textEdit.setFont(QFont("Consolas", 10))

        s = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;KEYA&nbsp;&nbsp;KEYB<br>"
        for i in range(0, 64):
            if i % 4 == 0:
                s = s + "Sector " + str(i) + " ===========<br>"
            

            if card.getTypeOfBlock(i) != TB_SECTOR_TRAILER:
                s = s + "Block "
                if i < 10:
                    s = s + "0"
                s = s + str(i) + ":&nbsp;&nbsp;"
                if card.canReadBlock(i, KEYA):
                    s = s + '<font color="#3CB043">R</font>'
                else:
                    s = s + "&nbsp;"
                if card.canWriteBlock(i, KEYA):
                    s = s + '<font color="#FF0000">W</font>'
                else:
                    s = s + "&nbsp;"
                s = s + "&nbsp;&nbsp;&nbsp;&nbsp;"
                if card.canReadBlock(i, KEYB):
                    s = s + '<font color="#3CB043">R</font>'
                else:
                    s = s + "&nbsp;"
                if card.canWriteBlock(i, KEYB):
                    s = s + '<font color="#FF0000">W</font>'
                else:
                    s = s + "&nbsp;"
                s = s + "<br>"
            else:
                s = s + "KEYA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                if card.canWriteKEYA(card.sectorOfBlock(i), KEYA):
                    s = s + '<font color="#FF0000">W</font>'
                else:
                    s = s + "&nbsp;"
                s = s + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                if card.canWriteKEYA(card.sectorOfBlock(i), KEYB):
                    s = s + '<font color="#FF0000">W</font>'
                else:
                    s = s + "&nbsp;"
                s = s + "<br>"

                s = s + "KEYB&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                if card.canReadKEYB(card.sectorOfBlock(i), KEYA):
                    s = s + '<font color="#3CB043">R</font>'
                else:
                    s = s + "&nbsp;"
                if card.canWriteKEYB(card.sectorOfBlock(i), KEYA):
                    s = s + '<font color="#FF0000">W</font>'
                else:
                    s = s + "&nbsp;"
                s = s + "&nbsp;&nbsp;&nbsp;&nbsp;"
                if card.canReadKEYB(card.sectorOfBlock(i), KEYB):
                    s = s + '<font color="#3CB043">R</font>'
                else:
                    s = s + "&nbsp;"
                if card.canWriteKEYB(card.sectorOfBlock(i), KEYB):
                    s = s + '<font color="#FF0000">W</font>'
                else:
                    s = s + "&nbsp;"
                s = s + "<br>"

                s = s + "accBits&nbsp;&nbsp;&nbsp;&nbsp;"
                if card.canReadAccessBits(card.sectorOfBlock(i), KEYA):
                    s = s + '<font color="#3CB043">R</font>'
                else:
                    s = s + "&nbsp;"
                if card.canWriteAccessBits(card.sectorOfBlock(i), KEYA):
                    s = s + '<font color="#FF0000">W</font>'
                else:
                    s = s + "&nbsp;"
                s = s + "&nbsp;&nbsp;&nbsp;&nbsp;"
                if card.canReadAccessBits(card.sectorOfBlock(i), KEYB):
                    s = s + '<font color="#3CB043">R</font>'
                else:
                    s = s + "&nbsp;"
                if card.canWriteAccessBits(card.sectorOfBlock(i), KEYB):
                    s = s + '<font color="#FF0000">W</font>'
                else:
                    s = s + "&nbsp;"
                s = s + "<br>"

        self.textEdit.setHtml(s)
