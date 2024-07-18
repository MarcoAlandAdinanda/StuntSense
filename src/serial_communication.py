import serial

class SerialCommunication():
    def __init__(self, port_):
        self.port_ = port_

    def read_serial(self):
        mcu_serial = serial.Serial(port=self.port_, baudrate=115200, timeout=0.1)
        raw_msg = mcu_serial.readline().decode('utf-8')

        msg = raw_msg.split('|')
        return msg