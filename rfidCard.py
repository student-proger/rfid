from hidDevice import hidDevice

class rfidCard():
    def __init__(self):
        self.hid = hidDevice(vid = 0x1EAF, pid = 0x0030, callback = self.callback)

    def __del__(self):
        del(self.hid)

    def callback(self, rawdata):
        print(">> ", rawdata)

    def readUID(self):
        self.hid.writeHID([0x01])
