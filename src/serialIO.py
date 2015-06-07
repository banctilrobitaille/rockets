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
        
    def isConnected(self):
        
        return self.isConnected
    
    def startCommunication(self):
        
        try:
            self.open()
            self.isConnected = True
            
        except serial.serialutil.SerialException, e:
        
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to open the com port: " + str(self.port))
                
           
        #while True:
           # data = self.readline().decode()
            #self.handleData(data)

    #def handleData(self,data):
        
        