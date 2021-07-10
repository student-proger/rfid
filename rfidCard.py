from hidDevice import hidDevice

class rfidCard():
    def __init__(self):
        self.hid = hidDevice(vid = 0x1EAF, pid = 0x0030)

    def __del__(self):
        del(self.hid)

    def readUID(self):
        self.hid.writeHID([0x01])
