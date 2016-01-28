import serial

'''
Created on 2016-01-04

@author: rockets
'''

class SerialConnection(serial.Serial):

    
    def __init__(self, port="/dev/ttyS0", baudrate=57600, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS):
        
        super.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.__isConnected = False
    
    @property
    def port(self):
        return self.port
    
    @port.setter
    def port(self, port):
        self.port = port
    
    @property
    def baudrate(self):
        return self.baudrate
    
    @baudrate.setter
    def baudrate(self, baudrate):
        self.baudrate = baudrate
        
    @property
    def stopbits(self):
        return self.stopbits
    
    @stopbits.setter
    def stopbits(self, stopbits):
        self.stopbits = stopbits
        
    @property
    def parity(self):
        return self.parity
    
    @parity.setter
    def parity(self, parity):
        self.parity = parity
        
    @property
    def bytesize(self):
        return self.bytesize
    
    @bytesize.setter
    def bytesize(self, bytesize):
        self.bytesize = bytesize
         
    @property
    def isConnected(self):
        return self.__isConnected
    
    @isConnected.setter
    def isConnected(self,isConnected):
        self.__isConnected = isConnected