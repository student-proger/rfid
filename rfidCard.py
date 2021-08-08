"""
Модуль для работы с RFID картами
"""

from hidDevice import hidDevice

# Константы для указания типа ключа
KEYA = 0x01
KEYB = 0x02
KEYAB = KEYA + KEYB

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
        buf = [0x02, key_type - 1]
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

    def getAccessBits(self, dump, sector):
        """ Возвращает биты доступа для сектора.

        +-----------------------------+--------------+----+-----------------------------+
        |  0 |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 | 13 | 14 | 15 |
        +-----------------------------+--------------+----+-----------------------------+
        |            Key A            | Access Conditions |            Key B            |
        |          (6 bytes)          |     (4 bytes)     |          (6 bytes)          |
        +-----------------------------+--------------+----+-----------------------------+
        """
        block = self.blockOfSector(sector) + 3
        b23 = dump[block][8]
        b1 = dump[block][7]
        c1 = b1 >> 4
        c3 = b23 >> 4
        c2 = b23 & 0x0F
        return [c1, c2, c3]

    def __fillAccessMatrix(self, accessBits):
        """ Заполняет списки битов доступа для использования в других функциях.

        __acdata - матрица доступа к блокам данных 0-2.
        3 элемента списка по 4 значения в каждом. 

        +-----------+-----------+-----------+-----------+-----------+
        |           |   Read    |   Write   | Increment | Decrement |
        +-----------+-----------+-----------+-----------+-----------+
        | Block 0   |           |           |           |           |
        +-----------+-----------+-----------+-----------+-----------+
        | Block 1   |           |           |           |           |
        +-----------+-----------+-----------+-----------+-----------+
        | Block 2   |           |           |           |           |
        +-----------+-----------+-----------+-----------+-----------+

        __actrailer - список доступа к трейлеру сектора. 6 элементов в списке.

        +-----------+-----------+-----------+-----------+-----------+-----------+
        |         KEYA          |      Access bits      |         KEYB          |
        +-----------+-----------+-----------+-----------+-----------+-----------+
        |   Read    |   Write   |   Read    |   Write   |   Read    |   Write   |
        +-----------+-----------+-----------+-----------+-----------+-----------+

        Каждое значение может иметь одно из следующих значений:
        None - нет доступа
        KEYA - доступ по ключу A.
        KEYB - доступ по ключу B.
        KEYAB (или KEYA+KEYB) - доступ по любому из ключей
        """
        self.__acdata = []
        self.__actrailer = []
        
        c1 = accessBits[0] & 0x01
        c2 = accessBits[1] & 0x01
        c3 = accessBits[2] & 0x01

        if c1 and c2 and c3:
            q = [None, None, None, None]
        elif c1 and (not c2) and c3:
            q = [KEYB, None, None, None]
        elif (not c1) and (c2) and c3:
            q = [KEYB, KEYB, None, None]
        elif (not c1) and (not c2) and (c3):
            q = [KEYAB, None, None, KEYAB]
        elif (c1) and (c2) and (not c3):
            q = [KEYAB, KEYB, KEYB, KEYAB]
        elif (c1) and (not c2) and (not c3):
            q = [KEYAB, KEYB, None, None]
        elif (not c1) and (c2) and (not c3):
            q = [KEYAB, None, None, None]
        elif (not c1) and (not c2) and (not c3):
            q = [KEYAB, KEYAB, KEYAB, KEYAB] # transport configuration

        self.__acdata.append(q)

        c1 = (accessBits[0] & 0x02) >> 1
        c2 = (accessBits[1] & 0x02) >> 1
        c3 = (accessBits[2] & 0x02) >> 1

        if c1 and c2 and c3:
            q = [None, None, None, None]
        elif c1 and (not c2) and c3:
            q = [KEYB, None, None, None]
        elif (not c1) and (c2) and c3:
            q = [KEYB, KEYB, None, None]
        elif (not c1) and (not c2) and (c3):
            q = [KEYAB, None, None, KEYAB]
        elif (c1) and (c2) and (not c3):
            q = [KEYAB, KEYB, KEYB, KEYAB]
        elif (c1) and (not c2) and (not c3):
            q = [KEYAB, KEYB, None, None]
        elif (not c1) and (c2) and (not c3):
            q = [KEYAB, None, None, None]
        elif (not c1) and (not c2) and (not c3):
            q = [KEYAB, KEYAB, KEYAB, KEYAB] # transport configuration

        self.__acdata.append(q)

        c1 = (accessBits[0] & 0x04) >> 2
        c2 = (accessBits[1] & 0x04) >> 2
        c3 = (accessBits[2] & 0x04) >> 2

        if c1 and c2 and c3:
            q = [None, None, None, None]
        elif c1 and (not c2) and c3:
            q = [KEYB, None, None, None]
        elif (not c1) and (c2) and c3:
            q = [KEYB, KEYB, None, None]
        elif (not c1) and (not c2) and (c3):
            q = [KEYAB, None, None, KEYAB]
        elif (c1) and (c2) and (not c3):
            q = [KEYAB, KEYB, KEYB, KEYAB]
        elif (c1) and (not c2) and (not c3):
            q = [KEYAB, KEYB, None, None]
        elif (not c1) and (c2) and (not c3):
            q = [KEYAB, None, None, None]
        elif (not c1) and (not c2) and (not c3):
            q = [KEYAB, KEYAB, KEYAB, KEYAB] # transport configuration

        self.__acdata.append(q)

        c1 = (accessBits[0] & 0x08) >> 3
        c2 = (accessBits[1] & 0x08) >> 3
        c3 = (accessBits[2] & 0x08) >> 3

        if c1 and c2 and c3:
            self.__actrailer = [None, None, KEYAB, None, None, None]
        elif c1 and (not c2) and c3:
            self.__actrailer = [None, None, KEYAB, KEYB, None, None]
        elif (not c1) and (c2) and c3:
            self.__actrailer = [None, KEYB, KEYAB, KEYB, None, KEYB]
        elif (not c1) and (not c2) and (c3):
            self.__actrailer = [None, KEYA, KEYA, KEYA, KEYA, KEYA] # Key B may be read, transport configuration
        elif (c1) and (c2) and (not c3):
            self.__actrailer = [None, None, KEYAB, None, None, None]
        elif (c1) and (not c2) and (not c3):
            self.__actrailer = [None, KEYB, KEYAB, None, None, KEYB]
        elif (not c1) and (c2) and (not c3):
            self.__actrailer = [None, None, KEYA, None, KEYA, None] # Key B may be read
        elif (not c1) and (not c2) and (not c3):
            self.__actrailer = [None, KEYA, KEYA, None, KEYA, KEYA] # Key B may be read

        #print(self.__acdata)
        #print(self.__actrailer)

    def canReadBlock(self, block, key):
        """ Возвращает True, если с помощью ключа (KEYA/KEYB) можно прочитать блок. """
        pass
        #self.__fillAccessMatrix()
