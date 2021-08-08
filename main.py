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
from keyHelper import keyHelper

def tohex(dec):
    """ Переводит десятичное число в 16-ричный вид с отбрасыванием `0x` """
    s = hex(dec).split('x')[-1]
    s = s.upper()
    if len(s) == 1:
        s = "0" + s
    return s


class RfidApp(QtWidgets.QMainWindow, mainform.Ui_MainWindow):
    """ Класс главного окна приложения """

    # Списки ключей для каждого сектора
    keysa = []
    keysb = []
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.buttonReadUID)
        self.pushButton_2.clicked.connect(self.buttonReadDump)
        self.textEdit.setReadOnly(True)
        self.textEdit.setFont(QFont("Consolas", 10))
        self.progressBar.setVisible(False)

        self.card = rfidCard(vid = 0x1EAF, pid = 0x0030)

    def __del__(self):
        del(self.card)

    def buttonReadUID(self):
        """res = self.card.readUID()
        if res == None:
            self.label.setText("Ошибка чтения")
            return

        res = list(map(tohex, res))
        self.label.setText(" ".join(res))
        self.textEdit.setHtml("")"""

        res = self.card.readUID()
        if res == None:
            self.label.setText("Ошибка чтения")
            return

        res = self.card.authBlock(18, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], KEYB)
        if res:
            if self.card.writeBlock(18, [0x01, 0x02, 0x03, 0x04, 0x05, 0xEE, 0xEE, 0xEE, 0xEE, 0xEE, 0xEE, 0xEE, 0xEE, 0xEE, 0xEE, 0xEE]):
                self.label.setText("Запись успешна")
            else:
                self.label.setText("Ошибка записи")
        else:
            self.label.setText("Ошибка аутентификации")



    def buttonReadDump(self):
        res = self.card.readUID()
        if res == None:
            s = "<b>Ошибка чтения UID карты</b>"
            self.textEdit.setHtml(s)
            return
        res = list(map(tohex, res))
        self.label.setText(" ".join(res))
        s = "UID: " + " ".join(res) + "<br>"
        #s = s + "---------------------------------------------------<br>"

        self.keysa = []
        self.keysb = []
        self.card.dump = []

        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(15)
        keys = keyHelper()
        # Цикл по секторам RFID карты. В каждой итерации пробуем подобрать пару ключей (A/B) из словаря.
        for i in range(0, 16):
            self.progressBar.setValue(i)
            keys.reset()
            while not keys.end():
                currentKey = keys.get()
                res = self.card.authBlock(self.card.blockOfSector(i), keys.keyToList(currentKey), KEYA)
                print("A:", currentKey, self.card.blockOfSector(i), res)
                if res:
                    # Успешно найден ключ
                    self.keysa.append(currentKey)
                    break
                else:
                    # При попытке авторизации сектора неправильным ключом требуется повторная инициализация карты,
                    # для этого снова читаем её UID.
                    r = self.card.readUID()
                    if r == None:
                        print("ОШИБКА: Потеря карты")
            else:
                self.keysa.append(None)

            keys.reset()
            while not keys.end():
                currentKey = keys.get()
                res = self.card.authBlock(self.card.blockOfSector(i), keys.keyToList(currentKey), KEYB)
                print("B:", currentKey, self.card.blockOfSector(i), res)
                if res:
                    # Успешно найден ключ
                    self.keysb.append(currentKey)
                    break
                else:
                    # При попытке авторизации сектора неправильным ключом требуется повторная инициализация карты,
                    # для этого снова читаем её UID.
                    r = self.card.readUID()
                    if r == None:
                        print("ОШИБКА: Потеря карты")
            else:
                self.keysb.append(None)

        print("KEY A: ", self.keysa)
        print("KEY B: ", self.keysb)

        # Вывод ключей в таблицу на форме
        self.keyTable.clear()
        self.keyTable.setRowCount(16)
        self.keyTable.setHorizontalHeaderLabels(["KEY A", "KEY B"])
        self.keyTable.setVerticalHeaderLabels(list(map(str, [i for i in range(0, 16)])))
        for i in range(0, 16):
            self.keyTable.setItem(i, 0, QTableWidgetItem(self.keysa[i]))
            self.keyTable.setItem(i, 1, QTableWidgetItem(self.keysb[i]))


        # Проверяем, есть ли смысл пытаться прочитать карту. Для этого нужно, чтобы
        # хотя бы для одного сектора был подобран один из ключей. 
        flag = False
        for item in self.keysa:
            if item != None:
                flag = True
        for item in self.keysb:
            if item != None:
                flag = True

        self.progressBar.setMaximum(63)

        if flag:
            for block in range(0, 64):
                self.progressBar.setValue(block)
                nokey = False
                sector = self.card.sectorOfBlock(block)
                if self.card.isFirstBlock(block):
                    if self.keysa[sector] != None:
                        res = self.card.authBlock(block, keys.keyToList(self.keysa[sector]), KEYA)
                    elif self.keysb[sector] != None:
                        res = self.card.authBlock(block, keys.keyToList(self.keysb[sector]), KEYB)
                    else:
                        # Нет ключей для сектора
                        nokey = True
                if not nokey:
                    res = self.card.readBlock(block)
                    if res == None:
                        self.card.dump.append(None)
                        return
                    self.card.dump.append(res)

            for sector in range(0, 16):
                block = self.card.blockOfSector(sector) + 3
                temp = []
                temp = self.card.dump[block][:]
                self.card.dump[block] = []
                for i in range(0, 6):
                    self.card.dump[block].append(keys.keyToList(self.keysa[sector])[i])
                for i in range(6, 10):
                    self.card.dump[block].append(temp[i])
                for i in range(0, 6):
                    self.card.dump[block].append(keys.keyToList(self.keysb[sector])[i])

            print(self.card.dump)

            for block in range(0, 64):
                sector = self.card.sectorOfBlock(block)
                if self.card.isFirstBlock(block):
                    sectorstr = str(sector)
                    if sector < 10:
                        sectorstr = "0" + sectorstr
                    s = s + "---- Sector " + sectorstr + " ------------------------------------<br>"

                blockstr = str(block)
                if block < 10:
                    blockstr = "0" + blockstr

                if self.card.dump[block] != None:
                    ds = list(map(tohex, self.card.dump[block]))
                    if block == 0:
                        ss = blockstr + ': <font color="#FF1493">' + " ".join(ds)
                        ss = ss + "</font>"
                    elif self.card.isLastBlock(block):
                        ss = blockstr + ': <font color="#3CB043">' + " ".join(ds[0:6]) + '</font>'
                        ss = ss + ' <font color="#FF0000">' + " ".join(ds[6:9]) + '</font> '
                        ss = ss + ds[9]
                        ss = ss + ' <font color="#3CB043">' + " ".join(ds[10:16]) + '</font>'
                    else:
                        ss = blockstr + ": " + " ".join(ds)

                    dd = []
                    for item in self.card.dump[block]:
                        if (item >= 32 and item <= 126) or item >= 184:
                            dd.append(item)
                        else:
                            dd.append(183)

                    ch = list(map(chr, dd))
                    sch = "".join(ch)
                    sch = sch.replace(" ", "&nbsp;")
                    ss = ss + "&nbsp;&nbsp;&nbsp;&nbsp;" + sch

                else:
                    ss = blockstr + ": Ошибка чтения блока"
                s = s + ss + "<br>"

            self.textEdit.setHtml(s)
        
        self.progressBar.setVisible(False)
        del(keys)

        ac = self.card.getAccessBits(1)
        print(ac)
        #self.card.__fillAccessMatrix(ac)

    

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RfidApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
