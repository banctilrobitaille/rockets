import serial
import PyQt4
import threading
import time

class SerialConnection(serial.Serial):

    def __init__(self):
        
        serial.Serial.__init__(self)
        self.port = "/dev/ttyS0"
        self.baudrate = 57600
        self.stopbits = serial.STOPBITS_ONE
        self.parity = serial.PARITY_NONE
        self.bytesize = serial.EIGHTBITS
        self.isConnected = False
        self.threadRunningFlag = False
    
    def startCommunication(self):
        
        try:
            #self.open()
            self.isConnected = True
            self.readingThread = Thread(self)
            self.readingThread.runningFlag = True
            self.readingThread.start()
            
        except serial.serialutil.SerialException:
        
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to open the com port: " + str(self.port))
    
    def stopCommunication(self):
        
        if self.isConnected:
            
            try: 
                
                self.readingThread.runningFlag = False
                #self.close()
                self.isConnected = False
            except serial.serialutil.SerialException:
                
                PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to close the com port: " + str(self.port))
        
        else:
                   
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Oups", "No connection currently opened !")
    
    
    def handleData(self, data):
        print(data)
      
    def readFromSerialPort(self):
        
            #data = self.readall()
            self.handleData("data")
        
class Thread(threading.Thread):
    
    def __init__(self, serialConnection):
        self.serialConnection = serialConnection
        threading.Thread.__init__(self)
        self.runningFlag = False
        
    def run(self):
        
        while self.runningFlag == True:
            
            self.serialConnection.readFromSerialPort()
            time.sleep(2)
            