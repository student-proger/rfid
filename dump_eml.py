"""
Класс для работы с дампами в формате eml.
Представляет собой текстовый файл с hex-дампом. Каждый блок с отдельной строки.
Дамп нельзя сохранить, если он неполный.

Пример:
DB5AA4B0950804006263646566676869
140103E103E103E103E103E103E103E1
03E103E103E103E103E103E103E103E1
A0A1A2A3A4A5787788C1FFFFFFFFFFFF
033E91010E5402656E746578746D6573
................................
"""

def tohex(dec):
    """ Переводит десятичное число в 16-ричный вид с отбрасыванием `0x` """
    s = hex(dec).split('x')[-1]
    s = s.upper()
    if len(s) == 1:
        s = "0" + s
    return s

class dumpEml():
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
            f = open(fn, "rt")
            for line in f:
                q = [line[i:i+2] for i in range(0, len(line), 2)]
                if q[-1] == "\n":
                    q = q[:-1]
                w = []
                for item in q:
                    w.append(int(item, 16))
                self._dump.append(w)
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
                s = list(map(ord, list("".join(list(map(tohex, self._dump[i]))))))
                f.write(bytes(s))
                if i < 63:
                    f.write(bytes([10])) # символ переноса строки
            f.close()
        except:
            return False
        else:
            return True
