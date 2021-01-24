import serial

def bytes2int(byte):
    return int.from_bytes(byte, "big")

class MrzReader:
    def __init__(self, port='COM3'):
        self.ser = serial.Serial(port)

    def read_mrz(self):
        cmd = int("0x49",16)
        data = bytearray([ cmd, 0, 0 ])
        self.ser.write(data)     # write a string
        cmd_res, MSB, LSB = map(bytes2int, [self.ser.read(1) for _ in range(3)])
        assert cmd_res == cmd
        MRZ = self.ser.read(LSB).decode('ascii')
        return MRZ.replace('\r', '')