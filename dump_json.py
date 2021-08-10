"""
Класс для работы с дампами в формате json.

Пример:
{
  "Created": "App name",
  "FileType": "mfcard",
  "blocks": {
    "0": "DB5AA4B0950804006263646566676869",
    "1": "140103E103E103E103E103E103E103E1",
    "2": "03E103E103E103E103E103E103E103E1",
    "3": "A0A1A2A3A4A5787788C1FFFFFFFFFFFF",
    "4": "033E91010E5402656E746578746D6573",
    ........................................
  }
}
"""

import json

def tohex(dec):
    """ Переводит десятичное число в 16-ричный вид с отбрасыванием `0x` """
    s = hex(dec).split('x')[-1]
    s = s.upper()
    if len(s) == 1:
        s = "0" + s
    return s

class dumpJson():
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
            with open(fn, 'r') as f:
                js = json.load(f)
            for i in range(0, 64):
                line = js["blocks"][str(i)]
                q = [line[i:i+2] for i in range(0, len(line), 2)]
                w = []
                for item in q:
                    w.append(int(item, 16))
                self._dump.append(w)
        except:
            return False
        else:
            return True

    def saveToFile(self, fn):
        """ Сохранение дампа в файл """
        
        js = {"Created": "NFRFID",
              "FileType": "mfcard",
              "blocks": {}
             }
        for i in range(0, 64):
            js["blocks"][str(i)] = "".join(list(map(tohex, self._dump[i])))
        try:
            with open(fn, 'w') as f:
                json.dump(js, f)

        except:
            return False
        else:
            return True
