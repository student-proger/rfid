import os
import sys
import time
from pywinusb import hid
from threading import Thread, Lock

# Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QInputDialog, QComboBox, QSystemTrayIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QMenu
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QRect
# design
import mainform

TX_BUF_SIZE = 18

class hidDevice():
    def __init__(self, vid, pid):
        self.openHID(vid, pid)

    def __del__(self):
        self.closeHID()

    def writeHID(self, buf):
        """ Отправка данных на USB HID устройство """
        buff = [0x00]

        for item in buf:
            buff.append(item)

        while len(buff) < TX_BUF_SIZE + 1:
            buff.append(0x00)

        try:
            print(">> ", end="")
            print(buff)
            self.out_report.set_raw_data(buff)
            self.out_report.send()
        except AttributeError:
            return
        except:
            return

    def openHID(self, vid, pid):
        """ Открытие USB HID устройства для работы.

        vid -- Vendor ID
        pid -- Product ID
        """
        filter = hid.HidDeviceFilter(vendor_id = vid, product_id = pid)
        devices = filter.get_devices()
        if devices:
            self.device = devices[0]
            print("USB device founded.")
            
            self.device.set_raw_data_handler(self.readHID)
            self.device.open()
            
            self.out_report = self.device.find_output_reports()[0]

    def closeHID(self):
        """ Закрытие USB HID устройства """
        try:
            self.device.close()
            del(self.out_report)
        except AttributeError:
            return
        except:
            pass

    def readHID(self, msg):
        print("<< ", end="")
        print(msg)


class RfidApp(QtWidgets.QMainWindow, mainform.Ui_MainWindow):
    """ Класс главного окна приложения """
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.buttonclick)

        self.hid = hidDevice(vid = 0x1EAF, pid = 0x0030)

    def __del__(self):
        del(self.hid)

    def buttonclick(self):
        self.hid.writeHID([0x01])

    

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RfidApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
