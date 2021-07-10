from hidDevice import hidDevice

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
