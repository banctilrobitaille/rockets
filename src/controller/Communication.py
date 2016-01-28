import serial
import PyQt4
from model.Frame import Frame

"""#############################################################################
# 
# Nom du module:          Cummunication.py
# Auteur:                 Benoit Anctil-Robitaille
# Date:                   5 janvier 2016
# Description:            Le module Communication.py inclus les classes et methodes
#                         permettant de controller la communication serie
#
##############################################################################"""


"""#
# La classe SerialController
# Description:    Classe permettant de controller la communication serie,
#                 commencer la communication avec la fusee, fermer la
#                 communication avec la fusee, construire les trames de 
#                 donnees avec les donnees recues etc.
#"""

class SerialController(PyQt4.QtCore.QObject):
    
    #command = {'GETTELEMETRY' : bitarray('0'),
    #          'ACK'          : bitarray('10'),
    #         'NACK'         : bitarray('110'),
    #        'DISCOVER'     : bitarray('1110'),
    #       'GETLOG'       : bitarray('1111')}
    
    """Signal to connect the model to the view, has been implemented
    in the controller as the serial connection class uses serial.Serial
    metaclass and cannot inherite from QObject"""
    portChanged = PyQt4.QtCore.pyqtSignal(str)
    baudrateChanged = PyQt4.QtCore.pyqtSignal(int)
    stopbitsChanged = PyQt4.QtCore.pyqtSignal(float)
    parityChanged = PyQt4.QtCore.pyqtSignal(str)
    bytesizeChanged = PyQt4.QtCore.pyqtSignal(int)
    stateChanged = PyQt4.QtCore.pyqtSignal(bool)
    
    def __init__(self,serialConnection, rocketController):
        
        super(PyQt4.QtCore.QObject,self).__init__()
        self.__serialConnection = serialConnection
        self.__rocketController = rocketController
        self.__serialReader = SerialReader(self.__serialConnection, self.__rocketController)
        
    
    """
    #    Methode updateSerialConnectionSettings
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour tous les parametres de la connexion serie
    #                 Cette methode appelle des methodes specifiques
    #                 pour mettre a jour les attributs.
    #
    #    param:       port, le port serie ex: /dev/ttyS0
    #                 baudrate, le baudrate du port serie
    #                 stopbits, le stopbits ex: serial.STOPBITS_ONE
    #                 parity, la parite ex: serial.PARITY_NONE
    #                 bytesize, le nombre de bits envoye ex: serial.EIGHTBITS
    #    return: None
    """ 
    def updateSerialConnectionSettings(self, port, baudrate, stopbits, parity, bytesize):
        
        self.updateSerialConnectionPort(port)
        self.updateSerialConnectionBaudrate(baudrate)
        self.updateSerialConnectionStopbits(stopbits)
        self.updateSerialConnectionParity(parity)
        self.updateSerialConnectionByteSize(bytesize)
    
    """
    #    Methode updateSerialConnectionPort
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le port de la connexion serie
    #
    #    param:       port, le port serie ex: /dev/ttyS0
    #    return: None
    """ 
    def updateSerialConnectionPort(self,port):
        
        self.__serialConnection.port = port
        self.portChanged.emit(port)
    
    """
    #    Methode updateSerialConnectionBaudrate
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le baudrate de la connexion serie
    #
    #    param:       baudrate, le baudrate du port serie
    #    return: None
    """ 
    def updateSerialConnectionBaudrate(self, baudrate):
        
        self.__serialConnection.baudrate = baudrate
        self.baudrateChanged.emit(baudrate)
    
    """
    #    Methode updateSerialConnectionStopbits
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le stopbits de la connexion serie
    #
    #    param:       stopbits, le stopbits ex: serial.STOPBITS_ONE
    #    return: None
    """ 
    def updateSerialConnectionStopbits(self, stopbits):
        
        self.__serialConnection.stopbits = stopbits
        self.stopbitsChanged.emit(stopbits)
    
    """
    #    Methode updateSerialConnectionParity
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour la parite de la connexion serie
    #
    #    param:       parity, la parite ex: serial.PARITY_NONE
    #    return: None
    """ 
    def updateSerialConnectionParity(self, parity):
        
        self.__serialConnection.parity = parity
        self.parityChanged.emit(parity)
    
    
    """
    #    Methode updateSerialConnectionByteSize
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le nombre de bits envoyes par la connexion serie
    #
    #    param:       bytesize, le nombre de bits envoye ex: serial.EIGHTBITS
    #    return: None
    """ 
    def updateSerialConnectionByteSize(self, bytesize):
        
        self.__serialConnection.bytesize = bytesize
        self.bytesizeChanged(bytesize)
        
    
    """
    #    Methode startReadingData
    #    Description: Methode demarrant un thread de lecture de donnees
    #                 sur le port serie
    #                 
    #
    #    param:    None
    #    return:   None
    """ 
    def startReadingData(self):
        
        self.__serialReader.running = True
        self.__serialReader.start()
    
    """
    #    Methode stopReadingData
    #    Description: Methode qui arrete le thread de lecture de donnees
    #                 sur le port serie
    #                 
    #
    #    param:    None
    #    return:   None
    """ 
    def stopReadingData(self):
        
        self.__serialReader.running = False

"""#
# La classe SerialReader
# Description:    Classe representant un thread de lecture de donnees
#                 sur le port serie. Celle-ci cree des frames et met a 
#                 jour les attributs du model Rocket selon les donnees
#                 recues.
#"""
class SerialReader(PyQt4.QtCore.QThread):
    
    __running = False
    
    def __init__(self,serialConnection, rocketController):
        
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
        
    
    
    
        