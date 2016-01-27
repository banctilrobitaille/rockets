import serial
import bitarray
import PyQt4
from model.Frame import Frame
'''
Created on 2016-01-11

@author: rockets
'''

class SerialController():
    
    command = {'GETTELEMETRY' : bitarray('0'),
               'ACK'          : bitarray('10'),
               'NACK'         : bitarray('110'),
               'DISCOVER'     : bitarray('1110'),
               'GETLOG'       : bitarray('1111')}
    
    def __init__(self,SerialConnection):
        
        serial.Serial.__init__(self)
        self.__serialConnection = SerialConnection
        self.__serialReader = SerialReader(self.__serialConnection)
        
    
    def startReadingData(self):
        
        self.__serialReader.running = True
        self.__serialReader.start()
    
    def stopReadingData(self):
        
        self.__serialReader.running = False


class SerialReader(PyQt4.QtCore.QThread):
    
    __running = False
    
    def __init__(self,SerialConnection):
        
        super.__init__(self)
        self.__serialConnection = SerialConnection
    
    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self,value):
        self.__running = value
    
    def dataReceived(self):
        
        self.__frame = Frame(self.__serialConnection.read(size=Frame.LENGTH))
    
    def handleData(self):
        
        pass
    
    def run(self):
        
        try:
            self.__serialConnection.open()
            self.__serialConnection.isConnected(True)
        
        except serial.serialutil.SerialException:
        
            raise serial.serialutil.SerialException
        
        while self.__running:
            
            if self.__serialConnection.inWaiting() >= Frame.LENGTH:
               
                self.dataReceived()
                self.handleData()
       
        self.__serialConnection.isConnected(False)
        
    
    
    
        