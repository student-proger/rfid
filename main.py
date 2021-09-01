import os
import sys
import time
from threading import Thread, Lock

# Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QInputDialog, QFileDialog, QComboBox, QSystemTrayIcon, QCheckBox
from PyQt5.QtWidgets import QMessageBox, QWidget, QMenu
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect
# design
import mainform

from rfidCard import rfidCard
from rfidCard import KEYA, KEYB, TB_SECTOR_TRAILER, TB_DATABLOCK_0, TB_DATABLOCK_1, TB_DATABLOCK_2, TB_UID
from keyHelper import keyHelper
from dump_bin import dumpBin
from dump_eml import dumpEml
from dump_json import dumpJson
from dump_mct import dumpMct

from accessbitsunit import accessBitsForm
from writedialogunit import writeDialogForm
from logunit import logForm
from dumpeditorunit import dumpEditorForm

def tohex(dec):
    """ Переводит десятичное число в 16-ричный вид с отбрасыванием `0x` """
    if dec != None:
        s = hex(dec).split('x')[-1]
        s = s.upper()
        if len(s) == 1:
            s = "0" + s
    else:
        s = "--"
    return s

def messageBox(title, s):
    """Отображение диалогового окна с сообщением

    :param title: заголовок окна
    :param s: сообщение
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(s)
    msg.setWindowTitle(title)
    msg.exec_()

class RfidApp(QtWidgets.QMainWindow, mainform.Ui_MainWindow):
    """ Класс главного окна приложения """

    # Списки ключей для каждого сектора
    keysa = []
    keysb = []
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.readUID)
        self.pushButton_2.clicked.connect(self.readMemory)
        self.pushButton_3.clicked.connect(self.buttonViewAccessBits)
        self.pushButton_4.clicked.connect(self.saveDump)
        self.action_readDump.triggered.connect(self.readDump)
        self.action_saveDump.triggered.connect(self.saveDump)
        self.action_readUID.triggered.connect(self.readUID)
        self.action_readMemory.triggered.connect(self.readMemory)
        self.action_writeMemory.triggered.connect(self.writeMemory)
        self.action_editDump.triggered.connect(self.editDump)
        self.textEdit.setReadOnly(True)
        self.textEdit.setFont(QFont("Consolas", 10))
        self.keyTable.setFont(QFont("Consolas", 10))
        self.progressBar.setVisible(False)

        self.log = logForm()

        self.card = rfidCard(vid = 0x1EAF, pid = 0x0030)

    def __del__(self):
        del(self.card)
        del(self.log)

    def readDump(self):
        """ Функция загрузки дампа из файла """
        f = "Все файлы дампа (*.bin *.mfd *.dump *.eml *.json *.mct);;Proxmark, libnfc (*.bin *.mfd *.dump);;Proxmark emulator (*.eml);;json (*.json);;MIFARE Classic Tool (*.mct);;Все файлы (*.*)"
        fn = QFileDialog.getOpenFileName(self, 'Открыть дамп', '', f)[0]
        if fn == "":
            return

        ext = fn.split(".")[-1].lower()
        if ext == "bin" or ext == "mfd" or ext == "dump":
            d = dumpBin()
        elif ext == "eml":
            d = dumpEml()
        elif ext == "json":
            d = dumpJson()
        elif ext == "mct":
            d = dumpMct()
        else:
            messageBox("Ошибка", "Неизвестный тип файла")
            return

        d.loadFromFile(fn)
        self.card.dump = d.dump
        print(self.card.dump)
        del(d)

        self.viewDump()

    def saveDump(self):
        """ Функция сохранения дампа в файл """
        if len(self.card.dump) == 0:
            messageBox("Ошибка", "Дампа ещё нет. Нечего сохранять.")
            return

        f = "Proxmark, libnfc (*.bin *.mfd *.dump);;Proxmark emulator (*.eml);;json (*.json);;MIFARE Classic Tool (*.mct)"
        fn = QFileDialog.getSaveFileName(self, 'Сохранить дамп', '', f)[0]
        if fn == "":
            return

        ext = fn.split(".")[-1].lower()
        if ext == "bin" or ext == "mfd" or ext == "dump":
            d = dumpBin()
        elif ext == "eml":
            d = dumpEml()
        elif ext == "json":
            d = dumpJson()
        elif ext == "mct":
            d = dumpMct()
        else:
            messageBox("Ошибка", "Неизвестный тип файла")
            return

        d.dump = self.card.dump
        if not d.saveToFile(fn):
            messageBox("Ошибка", "Ошибка экспорта дампа.")
        del(d)

    def buttonViewAccessBits(self):
        self.acbForm = accessBitsForm(self.card)
        self.acbForm.exec_()


    def readUID(self):
        """ Чтение UID карты """

        res = self.card.readUID()
        if res == None:
            self.label.setText("")
            messageBox("Ошибка", "Ошибка чтения карты.")
            return

        res = list(map(tohex, res))
        self.label.setText(" ".join(res))

        """res = self.card.authBlock(18, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], KEYB)
        if res:
            if self.card.writeBlock(18, [0x06, 0x02, 0x06, 0x04, 0x06, 0xEE, 0xE6, 0xEE, 0xE6, 0xEE, 0xE6, 0xEE, 0xE6, 0xEE, 0xE6, 0xEE]):
                self.label.setText("Запись успешна")
            else:
                self.label.setText("Ошибка записи")
        else:
            self.label.setText("Ошибка аутентификации")"""

    def editDump(self):
        """ Редактирование дампа памяти """
        if len(self.card.dump) == 0:
            messageBox("Ошибка", "Дампа ещё нет. Нечего редактировать.")
            return

        window = dumpEditorForm(self.card.dump[:])
        
        if window.exec_() != 0:
            self.card.dump = window.dump[:]
        del(window)
        self.viewDump()

    def readMemory(self):
        self.log.clear()
        self.log.show()

        res = self.card.readUID()
        if res == None:
            self.label.setText("")
            self.log.close()
            messageBox("Ошибка", "Ошибка чтения карты.")
            return

        self.card.lastReadID = res[:]
        self.log.add("UID карты прочитан.")
        res = list(map(tohex, res))
        self.label.setText(" ".join(res))

        self.keysa = []
        self.keysb = []
        self.card.dump = []

        self.log.add("Поиск ключей для секторов...")
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(15)
        keys = keyHelper()
        # Цикл по секторам RFID карты. В каждой итерации пробуем подобрать пару ключей (A/B) из словаря.
        for i in range(0, 16):
            self.progressBar.setValue(i)

            # Подбираем ключ A
            keys.reset()
            while not keys.end():
                currentKey = keys.get()
                res = self.card.authBlock(self.card.blockOfSector(i), keys.keyToList(currentKey), KEYA)
                print("A:", currentKey, self.card.blockOfSector(i), res)
                if res:
                    # Успешно найден ключ
                    self.keysa.append(currentKey)
                    self.log.add("Ключ A для сектора " + str(i) + " найден.")
                    break
                else:
                    # При попытке авторизации сектора неправильным ключом требуется повторная инициализация карты,
                    # для этого снова читаем её UID.
                    r = self.card.readUID()
                    if r == None:
                        messageBox("Ошибка", "Потеря карты")
            else:
                self.keysa.append(None)
                self.log.add("Не удалось найти ключ A для сектора " + str(i) + ".", True)

            # Подбираем ключ B
            keys.reset()
            while not keys.end():
                currentKey = keys.get()
                res = self.card.authBlock(self.card.blockOfSector(i), keys.keyToList(currentKey), KEYB)
                print("B:", currentKey, self.card.blockOfSector(i), res)
                if res:
                    # Успешно найден ключ
                    self.keysb.append(currentKey)
                    self.log.add("Ключ B для сектора " + str(i) + " найден.")
                    break
                else:
                    # При попытке авторизации сектора неправильным ключом требуется повторная инициализация карты,
                    # для этого снова читаем её UID.
                    r = self.card.readUID()
                    if r == None:
                        messageBox("Ошибка", "Потеря карты")
            else:
                self.keysb.append(None)
                self.log.add("Не удалось найти ключ B для сектора " + str(i) + ".", True)

        self.log.add("Поиск ключей для секторов завершён.")
        self.log.add("")
        #print("KEY A: ", self.keysa)
        #print("KEY B: ", self.keysb)

        # Вывод ключей в таблицу на форме
        self.keyTable.clear()
        self.keyTable.setRowCount(16)
        self.keyTable.setHorizontalHeaderLabels(["KEY A", "KEY B"])
        self.keyTable.setVerticalHeaderLabels(list(map(str, [i for i in range(0, 16)])))
        for i in range(0, 16):
            self.keyTable.setItem(i, 0, QTableWidgetItem(self.keysa[i]))
            self.keyTable.setItem(i, 1, QTableWidgetItem(self.keysb[i]))
        self.keyTable.resizeRowsToContents()


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
                        if res:
                            self.log.add("Авторизация сектора " + str(sector) + " по ключу A.")
                        else:
                            self.log.add("Ошибка авторизации сектора " + str(sector) + " по ключу A.", True)
                    elif self.keysb[sector] != None:
                        res = self.card.authBlock(block, keys.keyToList(self.keysb[sector]), KEYB)
                        if res:
                            self.log.add("Авторизация сектора " + str(sector) + " по ключу B.")
                        else:
                            self.log.add("Ошибка авторизации сектора " + str(sector) + " по ключу B.", True)
                    else:
                        # Нет ключей для сектора
                        nokey = True
                if not nokey:
                    res = self.card.readBlock(block)
                    if res == None:
                        self.card.dump.append([None] * 16)
                        self.log.add("Ошибка считывания данных блока " + str(block) + ".")
                        continue
                    self.card.dump.append(res)
                    self.log.add("Данные блока " + str(block) + " считаны.")

            # Добавление найденных ключей в дамп
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

            #self.card.copyDump()
            self.viewDump()
        
        self.progressBar.setVisible(False)
        del(keys)

    def writeMemory(self):
        if len(self.card.dump) == 0:
            messageBox("Ошибка", "Дампа ещё нет. Откройте дамп из файла или считайте с другой карты.")
            return

        dialog = writeDialogForm()
        dialog.setWindowTitle("Запись")

        for i in range(0, 16):
            widget = dialog.findChild(QCheckBox, "checkBox_" + str(i + 1))
            widget.setChecked(True)
        dialog.checkBox_17.setChecked(False)

        ba = []
        if dialog.exec_() != 0:
            for i in range(0, 16):
                widget = dialog.findChild(QCheckBox, "checkBox_" + str(i + 1))
                ba.append(widget.isChecked())
            ignoreTrailer = dialog.checkBox_17.isChecked()
        del(dialog)

        # Сохраняем резервную копию записываемого дампа и подбираем ключи к текущей карте

        # Считываем ключи доступа с карты

        # Пишем ранее сохранённый дамп на карту

        # Делаем сравнение записанных данных

        # Восстанавливаем дамп из резервной копии

    def viewDump(self):
        """ Вывод дампа на форму """
        s = ""
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
                    if item != None:
                        if (item >= 32 and item <= 126) or item >= 184:
                            dd.append(item)
                        else:
                            dd.append(183)
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


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RfidApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
