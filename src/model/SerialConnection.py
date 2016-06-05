import serial

'''
Created on 2016-01-04

@author: rockets
'''


class SerialConnection(serial.Serial):
    def __init__(self, port=None, baudrate=57600, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE,
                 bytesize=serial.EIGHTBITS, deviceName=None):
        super(SerialConnection, self).__init__()
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.__deviceName = deviceName
        self.__isConnected = False

    @property
    def deviceName(self):
        return self.__deviceName

    @deviceName.setter
    def deviceName(self, deviceName):
        self.__deviceName = deviceName

    @property
    def isConnected(self):
        return self.__isConnected

    @isConnected.setter
    def isConnected(self, isConnected):
        self.__isConnected = isConnected
