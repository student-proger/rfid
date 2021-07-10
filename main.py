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

def sample_handler(msg):
    print(":")
    print(msg)

class RfidApp(QtWidgets.QMainWindow, mainform.Ui_MainWindow):
    """ Класс главного окна приложения """
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.buttonclick)

        self.openHID(vid = 0x1EAF, pid = 0x0030)


    def __del__(self):
        self.closeHID()

    def writeHID(self):
        """ Отправка данных на USB HID устройство """
        buf = [0x00]

        for i in range(0, 18):
            buf.append(0x01)

        try:
            print(buf)
            self.out_report.set_raw_data(buf)
            self.out_report.send()
        except AttributeError:
            return
        except:
            return

    def buttonclick(self):
        self.writeHID()

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
            
            self.device.set_raw_data_handler(sample_handler)
            self.device.open()
            
            self.out_report = self.device.find_output_reports()[0]
         


    def closeHID(self):
        """ Закрытие USB HID устройства """
        buf = [0x00]

        try:
            self.out_report.set_raw_data(buf)
            self.out_report.send()
            self.device.close()
        except AttributeError:
            return
        except:
            pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RfidApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
