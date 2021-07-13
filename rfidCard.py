"""
Модуль для работы с RFID картами
"""

from hidDevice import hidDevice

# Константы для указания типа ключа
KEYA = 0x00
KEYB = 0x01

class rfidCard():
    def __init__(self, vid, pid):
        """ Конструктор класса. Принимает VID и PID картридера """
        self.hid = hidDevice(vid, pid, callback = self.callback)
        self.waitdata = False

    def __del__(self):
        del(self.hid)

    def callback(self, rawdata):
        """ Callback функция, которая принимает данные, поступившие от картридера """
        self.rawdata = rawdata
        del(self.rawdata[0])
        self.waitdata = False
        print(">> ", rawdata)

    def readUID(self):
        """ Чтение UID карты """
        self.waitdata = True
        self.hid.writeHID([0x01])
        while self.waitdata:
            pass

        if self.rawdata[0] != 0xAA:
            return None
        else:
            del(self.rawdata[0])
            count = self.rawdata[0]
            return self.rawdata[1:count + 1]

    def authBlock(self, n, key, key_type):
        """ Аутентификация блока номер n с помощью ключа key.
        key_type = KEYA / KEYB
        """
        buf = [0x02, key_type]
        for item in key:
            buf.append(item)
        buf.append(n)

        self.waitdata = True
        self.hid.writeHID(buf)
        while self.waitdata:
            pass

        if self.rawdata[0] != 0xAB:
            return None
        else:
            return self.rawdata

    def readBlock(self, n):
        """ Чтение блока с номером n """
        buf = [0x03, n]

        self.waitdata = True
        self.hid.writeHID(buf)
        while self.waitdata:
            pass

        if self.rawdata[0] != 0xAC:
            return None
        else:
            return self.rawdata

    def isFirstBlock(self, n):
        """ Проверка, что это первый блок сектора """
        if n % 4 == 0:
            return True
        else:
            return False

    def isLastBlock(self, n):
        """ Проверка, что это последний блок сектора """
        if (n + 1) % 4 == 0:
            return True
        else:
            return False
