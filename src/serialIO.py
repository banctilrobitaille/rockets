import serial
import PyQt4
import time
import binascii
import re

class SerialConnection(serial.Serial):
    
    trigger = PyQt4.QtCore.pyqtSignal(int,int,int)
    
    def __init__(self):
        
        serial.Serial.__init__(self)
        self.port = "/dev/ttyS0"
        self.baudrate = 57600
        self.stopbits = serial.STOPBITS_ONE
        self.parity = serial.PARITY_NONE
        self.bytesize = serial.EIGHTBITS
        self.isConnected = False
        self.i = 0
        self.j = 0
        self.k = 0
    
    
    def handleData(self, data):
        
        self.i = self.i + 10
        self.j = self.j + 10
        self.k = self.k + 1
        return [self.i, self.j, self.k]
        self.trigger.emit(self.i, self.j, self.k)
        data.encode()
      
    def readFromSerialPort(self):
        
        data = self.read(self.inWaiting())
        self.handleData(data)
        
#        pattern = re.compile('\\\\x[0-9]*[a-f]*', re.IGNORECASE)
#        resultSet = pattern.findall(data)
        
#        for match in resultSet:
#            print match.span()
        
#        print(data)
        #if data.__len__() < 90 :
        hexString = binascii.b2a_qp(data, quotetabs=0, istext=1, header=0)
#        print(hexString)
        
        pattern = re.compile('\=[0-9]*[a-f]*', re.IGNORECASE)
        resultSet = pattern.findall(hexString)
        
        for match in resultSet:
            print binascii.b2a_hex(match[1:]).decode("hex")
        
        
            

        
class Thread(PyQt4.QtCore.QThread):
    
    isconnected = PyQt4.QtCore.pyqtSignal(bool)
    receivedata = PyQt4.QtCore.pyqtSignal(int, int, int)
    
    def __init__(self, serialConnection):
        self.serialConnection = serialConnection
        PyQt4.QtCore.QThread.__init__(self)
        self.isRunning = False
    
    def startCommunication(self):
        
        try:
            self.serialConnection.open()
            self.serialConnection.isConnected = True
            self.isRunning = True
            self.start()
            self.isconnected.emit(self.serialConnection.isConnected)
        except serial.serialutil.SerialException:
        
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to open the com port: " + str(self.serialConnection.port))
            
    def stopCommunication(self):
        
        if self.serialConnection.isConnected:
            
            try: 
                
                self.isRunning = False
                self.serialConnection.close()
                self.serialConnection.isConnected = False
                self.isconnected.emit(self.serialConnection.isConnected)
            except serial.serialutil.SerialException:
                
                PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to close the com port: " + str(self.serialConnection.port))
        
        else:
                   
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Oups", "No connection currently opened !")
    
    def run(self):
        
        while self.isRunning == True: 
            
            if self.serialConnection.inWaiting() > 0:
                self.analysedData = self.serialConnection.readFromSerialPort()
                #self.receivedata.emit(self.analysedData[0], self.analysedData[1], self.analysedData[2])
                
            