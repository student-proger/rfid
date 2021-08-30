"""
Класс для работы с дампами в формате mct (Mifare Classic Tool).
Представляет собой текстовый файл с hex-дампом. Каждый блок с отдельной строки. Дополнительно указаны номера секторов.

Пример:
+Sector: 0
DB5AA4B0950804006263646566676869
140103E103E103E103E103E103E103E1
03E103E103E103E103E103E103E103E1
A0A1A2A3A4A5787788C1FFFFFFFFFFFF
+Sector: 1
033E91010E5402656E746578746D6573
................................
"""

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

class dumpMct():
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
            sector = -1
            f = open(fn, "rt")
            for line in f:
                if line[0] == "+":
                    sector += 1
                    fsector = int(line.split()[-1])
                    if sector != fsector:
                        while sector < fsector:
                            for _ in range(0, 4):
                                t = [None] * 16
                                self._dump.append(t)
                            sector += 1
                    continue
                q = [line[i:i+2] for i in range(0, len(line), 2)]
                if q[-1] == "\n":
                    q = q[:-1]
                w = []
                for item in q:
                    if item != "--":
                        w.append(int(item, 16))
                    else:
                        w.append(None)
                self._dump.append(w)
            if sector < 63:
                for _ in range(sector, 64):
                    for _ in range(0, 4):
                        t = [None] * 16
                        self._dump.append(t)
            f.close()
        except:
            return False
        else:
            return True

    def saveToFile(self, fn):
        """ Сохранение дампа в файл """
        try:
            f = open(fn, "wb")
            ok = True
            for i in range(0, 64):
                if i % 4 == 0:
                    # Проверяем наличие данных в секторе перед его записью:
                    ok = False
                    for k in range(i, i+4):
                        for t in range(0, 16):
                            if self._dump[k][t] != None:
                                ok = True
                                break
                    if ok:
                        ss = "+Sector: " + str(i // 4)
                        ss = list(map(ord, list(ss)))
                        f.write(bytes(ss))
                        f.write(bytes([10])) # символ переноса строки
                if ok:
                    s = list(map(ord, list("".join(list(map(tohex, self._dump[i]))))))
                    f.write(bytes(s))
                    if i < 63:
                        f.write(bytes([10])) # символ переноса строки
            f.close()
        except:
            return False
        else:
            return True
