"""
Модуль для работы с RFID картами
"""

from hidDevice import hidDevice

# Константы для указания типа ключа
KEYA = 0x00
KEYB = 0x01

#Типы блоков
TB_SECTOR_TRAILER = 0x00
TB_DATABLOCK_0 = 0x01
TB_DATABLOCK_1 = 0x02
TB_DATABLOCK_2 = 0x03
TB_UID = 0x04

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
        #print(">> ", rawdata)

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
            return False
        else:
            return True

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
            del(self.rawdata[0])
            return self.rawdata

    def writeBlock(self, n, data):
        """ Запись блока с номером n """
        buf = [0x04, n]
        for item in data:
            buf.append(item)

        self.waitdata = True
        self.hid.writeHID(buf)
        while self.waitdata:
            pass

        if self.rawdata[0] != 0xAD:
            return False
        else:
            return True

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

    def getTypeOfBlock(self, n):
        """ Возвращает тип блока по его номеру """
        if n == 0:
            return TB_UID
        elif n % 4 == 0:
            return TB_DATABLOCK_0
        elif n % 4 == 1:
            return TB_DATABLOCK_1
        elif n % 4 == 2:
            return TB_DATABLOCK_2
        elif n % 4 == 3:
            return TB_SECTOR_TRAILER

    def sectorOfBlock(self, n):
        """ Возвращает номер сектора по номеру блока """
        return n // 4

    def blockOfSector(self, n):
        """ Возвращает номер первого блока в секторе n """
        return n * 4
