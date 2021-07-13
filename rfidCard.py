"""
Модуль для работы с RFID картами
"""

from hidDevice import hidDevice

KEYA = 0x00
KEYB = 0x01

class rfidCard():
    def __init__(self):
        self.hid = hidDevice(vid = 0x1EAF, pid = 0x0030, callback = self.callback)
        self.waitdata = False

    def __del__(self):
        del(self.hid)

    def callback(self, rawdata):
        self.rawdata = rawdata
        self.waitdata = False
        print(">> ", rawdata)

    def readUID(self):
        self.waitdata = True
        self.hid.writeHID([0x01])
        while self.waitdata:
            pass
        return self.rawdata

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
        return self.rawdata

    def readBlock(self, n):
        """ Чтение блока с номером n
        """
        buf = [0x03, n]

        self.waitdata = True
        self.hid.writeHID(buf)
        while self.waitdata:
            pass
        return self.rawdata

    def isFirstBlock(self, n):
        if n % 4 == 0:
            return True
        else:
            return False

    def isLastBlock(self, n):
        if (n + 1) % 4 == 0:
            return True
        else:
            return False
