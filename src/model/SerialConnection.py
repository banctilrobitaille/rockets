import serial 


'''
Created on 2016-01-04

@author: rockets
'''

class SerialConnection(serial.Serial):
    
    __INSTANCE = None
    
    def __init__(self, port="/dev/ttyS1", baudrate=57600, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS):
        
        super(serial.Serial,self).__init__()
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.__isConnected = False
    
    #===========================================================================
    # @property
    # def port(self):
    #     return self._port
    #   
    # @port.setter
    # def port(self, port):
    #     self._port = port
    #===========================================================================
    #===========================================================================
    #      
    # @property
    # def baudrate(self):
    #     return self._baudrate
    #  
    # @baudrate.setter
    # def baudrate(self, baudrate):
    #     self._baudrate = baudrate
    #      
    # @property
    # def stopbits(self):
    #     return self._stopbits
    #  
    # @stopbits.setter
    # def stopbits(self, stopbits):
    #     self._stopbits = stopbits
    #      
    # @property
    # def parity(self):
    #     return self._parity
    #  
    # @parity.setter
    # def parity(self, parity):
    #     self._parity = parity
    #      
    # @property
    # def bytesize(self):
    #     return self._bytesize
    #  
    # @bytesize.setter
    # def bytesize(self, bytesize):
    #     self._bytesize = bytesize
    #===========================================================================
          
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