import serial
import bitarray
import PyQt4
from model.Frame import Frame
from model.SerialConnection import SerialConnection
'''
Created on 2016-01-11

@author: rockets
'''

class SerialController():
    
    #command = {'GETTELEMETRY' : bitarray('0'),
     #          'ACK'          : bitarray('10'),
      #         'NACK'         : bitarray('110'),
       #        'DISCOVER'     : bitarray('1110'),
        #       'GETLOG'       : bitarray('1111')}
    
    def __init__(self,serialConnection, rocketController):
        
        serial.Serial.__init__(self)
        self.__serialConnection = serialConnection
        self.__rocketController = rocketController
        self.__serialReader = SerialReader(self.__serialConnection, self.__rocketController)
        
        
    def updateSerialConnectionSettings(self, port, baudrate, stopbits, parity, bytesize):
        
        self.updateSerialConnectionPort(port)
        self.updateSerialConnectionBaudrate(baudrate)
        self.updateSerialConnectionStopbits(stopbits)
        self.updateSerialConnectionParity(parity)
        self.updateSerialConnectionByteSize(bytesize)
    
    def updateSerialConnectionPort(self,port):
        
        self.__serialConnection.port(port)
        
    def updateSerialConnectionBaudrate(self, baudrate):
        
        self.__serialConnection.baurate(baudrate)
        
    def updateSerialConnectionStopbits(self, stopbits):
        
        self.__serialConnection.stopbits(stopbits)
        
    def updateSerialConnectionParity(self, parity):
        
        self.__serialConnection.parity(parity)
        
    def updateSerialConnectionByteSize(self, bytesize):
        
        self.__serialConnection.bytesize(bytesize)
    
    def startReadingData(self):
        
        self.__serialReader.running = True
        self.__serialReader.start()
    
    def stopReadingData(self):
        
        self.__serialReader.running = False


class SerialReader(PyQt4.QtCore.QThread):
    
    __running = False
    
    def __init__(self,serialConnection, rocketController):
        
        super.__init__(self)
        self.__serialConnection = serialConnection
        self.__rocketController = rocketController
    
    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self,value):
        self.__running = value
    
    
    def dataReceived(self):
        
        self.__frame = Frame.fromByteArray(self.__serialConnection.read(size=Frame.LENGTH))
    
    def handleData(self):
        
        rocketData = self.__frame.data
        self.__rocketController.updateRocketData(rocketData['speed'],
                                                 rocketData['altitude'],
                                                 rocketData['acceleration'],
                                                 rocketData['temperature'],
                                                 rocketData['direction'],
                                                 rocketData['coords'],
                                                 rocketData['ID'],
                                                 rocketData['state'])
    
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
        
    
    
    
        