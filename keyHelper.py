"""
Модуль для работы с ключами доступа
"""

class keyHelper():
    def __init__(self):
        self.keybuf = []
        self.fkey = open("keys\\std.keys", "rt")
        for item in self.fkey:
            item = item.strip()
            if (item != "") and (item[0] != "#"):
                self.keybuf.append(item)
        self.nextitem = 0

    def __del__(self):
        self.fkey.close()

    def end(self):
        """ Возвращает True, если список ключей закончился.
        Используется в циклах при переборе всего списка паролей. """
        if self.nextitem >= len(self.keybuf):
            return True
        else:
            return False

    def reset(self):
        """ Сбросить текущую позицию списка ключей и начать сначала """
        self.nextitem = 0

    def get(self):
        """ Возвращает следующий ключ """
        if self.end():
            return None
        r = self.keybuf[self.nextitem]
        self.nextitem += 1
        return r

    def keyToList(self, s):
        """ Преобразовывает строковый вид ключа к списку """
        if s == None:
            return [None] * 6
        w = []
        for i in range(0, 6):
            k = "0x" + s[i * 2:i * 2 + 2]
            w.append(int(k, 16))
        return w
