"""
Класс для работы с дампами в формате bin.
Размер файла дампа равен объёму карты. Представляет собой побайтовую копию карты.
"""

class dumpBin():
    dump = property()

    def __init__(self):
        self._dump = None

    def __del__(self):
        del(self._dump)

    @dump.getter
    def dump(self):
        return self._dump[:]

    @dump.setter
    def dump(self, value):
        self._dump = value[:]

    def loadFromFile(self, fn):
        """ Загрузка дампа из файла """
        self._dump = []
        try:
            f = open(fn, "rb")
            for i in range(0, 64):
                q = f.read(16)
                self._dump.append(list(bytes(q)))
            f.close()
        except:
            return False
        else:
            return True

    def saveToFile(self, fn):
        """ Сохранение дампа в файл """
        try:
            f = open(fn, "wb")
            for i in range(0, 64):
                f.write(bytes(self._dump[i]))
            f.close()
        except:
            return False
        else:
            return True
