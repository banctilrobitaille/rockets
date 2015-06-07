import serial
import PyQt4
import threading


class SerialConnection(serial.Serial):

    def __init__(self):
        
        serial.Serial.__init__(self)
        self.port = "/dev/ttyS0"
        self.baudrate = 57600
        self.stopbits = serial.STOPBITS_ONE
        self.parity = serial.PARITY_NONE
        self.bytesize = serial.EIGHTBITS
        self.isConnected = False
    
    def startCommunication(self):
        
        try:
            self.open()
            self.isConnected = True
            
        except serial.serialutil.SerialException:
        
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to open the com port: " + str(self.port))
    
    def stopCommunication(self):
        
        if self.isConnected:
            
            try: 
                self.close()
                self.isConnected = False
            except serial.serialutil.SerialException:
                
                PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to close the com port: " + str(self.port))
        
        else:
                   
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Oups", "No connection currently opened !")
        #while True:
           # data = self.readline().decode()
            #self.handleData(data)

    #def handleData(self,data):
        
        