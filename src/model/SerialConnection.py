import serial

'''
Created on 2016-01-04

@author: rockets
'''

class SerialConnection(serial.Serial):

    
    def __init__(self, port="/dev/ttyS0", baudrate=5600, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS):
        
        super.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.__isConnected = False
             
    @property
    def isConnected(self):
        return self.__isConnected
    
    @isConnected.setter
    def isConnected(self,isConnected):
        self.__isConnected = isConnected