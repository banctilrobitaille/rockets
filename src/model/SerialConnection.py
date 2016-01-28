import serial 


'''
Created on 2016-01-04

@author: rockets
'''

class SerialConnection(serial.Serial):
    
    __INSTANCE = None
    
    def __init__(self, port="/dev/ttyS0", baudrate=57600, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS):
        
        self.__port = port
        self.__baudrate = baudrate
        self.__stopbits = stopbits
        self.__parity = parity
        self.__bytesize = bytesize
        self.__isConnected = False
    
    @property
    def port(self):
        return self.__port
    
    @port.setter
    def port(self, port):
        self.__port = port
        
    @property
    def baudrate(self):
        return self.__baudrate
    
    @baudrate.setter
    def baudrate(self, baudrate):
        self.__baudrate = baudrate
        
    @property
    def stopbits(self):
        return self.__stopbits
    
    @stopbits.setter
    def stopbits(self, stopbits):
        self.__stopbits = stopbits
        
    @property
    def parity(self):
        return self.__parity
    
    @parity.setter
    def parity(self, parity):
        self.__parity = parity
        
    @property
    def bytesize(self):
        return self.__bytesize
    
    @bytesize.setter
    def bytesize(self, bytesize):
        self.__bytesize = bytesize
         
    @property
    def isConnected(self):
        return self.__isConnected
    
    @isConnected.setter
    def isConnected(self,isConnected):
        self.__isConnected = isConnected
        
    @staticmethod
    def getInstance():
        
        if SerialConnection.__INSTANCE is None:
            SerialConnection.__INSTANCE = SerialConnection()
            
        return SerialConnection.__INSTANCE