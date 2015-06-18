import serial
import PyQt4
import time

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
        #self.trigger.emit(self.i, self.j, self.k)
      
    def readFromSerialPort(self):
        
        data = self.read(self.inWaiting())
        print(data)
            

        
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
                
            