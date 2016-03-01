import serial
import PyQt4
import struct
from bitstring import BitArray
from model.Frame import Frame
from PyQt4.Qt import  pyqtSlot
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
    
    """Signal to connect the model to the view, has been implemented
    in the controller as the serial connection class uses serial.Serial
    metaclass and cannot inherite from QObject"""
    portChanged = PyQt4.QtCore.pyqtSignal(str)
    baudrateChanged = PyQt4.QtCore.pyqtSignal(int)
    stopbitsChanged = PyQt4.QtCore.pyqtSignal(float)
    parityChanged = PyQt4.QtCore.pyqtSignal(str)
    bytesizeChanged = PyQt4.QtCore.pyqtSignal(int)
    stateChanged = PyQt4.QtCore.pyqtSignal(bool)
    
    def __init__(self, rocketController, serialConnection):
        
        super(PyQt4.QtCore.QObject,self).__init__()
        self.__serialConnection = serialConnection
        self.__rocketController = rocketController
        self.__commandBuffer = None
        self.__history = CommunicationHistory()
        #self.__serialWriter = SerialWriter
        self.__serialReader = SerialReader(self.__serialConnection, self.__rocketController)
        #self.__serialReader.corruptedFrameReceived.connect(self.on_CorruptedFrameReceived)
        
    
    @property
    def serialConnection(self):
        return self.__serialConnection
    
    @serialConnection.setter
    def serialConnection(self, serialConnection):
        
        self.__serialConnection = serialConnection
    
    """
    #    Methode updateSerialConnectionSettings
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour tous les parametres de la connexion serie
    #                 Cette methode appelle des methodes specifiques
    #                 pour mettre a jour les attributs.
    #
    #    param:       _port, le _port serie ex: /dev/ttyS0
    #                 _baudrate, le _baudrate du _port serie
    #                 _stopbits, le _stopbits ex: serial.STOPBITS_ONE
    #                 _parity, la parite ex: serial.PARITY_NONE
    #                 _bytesize, le nombre de bits envoye ex: serial.EIGHTBITS
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
    #                 jour le _port de la connexion serie
    #
    #    param:       _port, le _port serie ex: /dev/ttyS0
    #    return: None
    """ 
    def updateSerialConnectionPort(self,port):
        
        self.__serialConnection._port = port
        self.portChanged.emit(port)
    
    """
    #    Methode updateSerialConnectionBaudrate
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le _baudrate de la connexion serie
    #
    #    param:       _baudrate, le _baudrate du _port serie
    #    return: None
    """ 
    def updateSerialConnectionBaudrate(self, baudrate):
        
        self.__serialConnection._baudrate = baudrate
        self.baudrateChanged.emit(baudrate)
    
    """
    #    Methode updateSerialConnectionStopbits
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le _stopbits de la connexion serie
    #
    #    param:       _stopbits, le _stopbits ex: serial.STOPBITS_ONE
    #    return: None
    """ 
    def updateSerialConnectionStopbits(self, stopbits):
        
        self.__serialConnection._stopbits = stopbits
        self.stopbitsChanged.emit(stopbits)
    
    """
    #    Methode updateSerialConnectionParity
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour la parite de la connexion serie
    #
    #    param:       _parity, la parite ex: serial.PARITY_NONE
    #    return: None
    """ 
    def updateSerialConnectionParity(self, parity):
        
        self.__serialConnection._parity = parity
        self.parityChanged.emit(parity)
    
    
    """
    #    Methode updateSerialConnectionByteSize
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le nombre de bits envoyes par la connexion serie
    #
    #    param:       _bytesize, le nombre de bits envoye ex: serial.EIGHTBITS
    #    return: None
    """ 
    def updateSerialConnectionByteSize(self, bytesize):
        
        self.__serialConnection._bytesize = bytesize
        self.bytesizeChanged.emit(bytesize)
    
    """
    #    Methode updateSerialConnectionState
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour l'etat de la connexion, True: est connecte, 
    #                 False: n'est pas connecte
    #
    #    param:       state, l'etat de la connexion
    #    return: None
    """ 
    def updateSerialConnectionState(self, state):
        
        self.__serialConnection.isConnected = state
        self.stateChanged.emit(state)

    
    
    """
    #    Methode startReadingData
    #    Description: Methode demarrant un thread de lecture de donnees
    #                 sur le _port serie
    #                 
    #
    #    param:    None
    #    return:   None
    """ 
    def startReadingData(self):
        
        try:
            self.__serialConnection.open()
            self.__serialReader.running = True
            self.__serialReader.start()
            self.updateSerialConnectionState(True)
            
        except serial.SerialException as error:
            
            print "Error while trying to open serial _port " + str(error)
            #raise serial.serialutil.SerialException
    
    
    """
    #    Methode stopReadingData
    #    Description: Methode qui arrete le thread de lecture de donnees
    #                 sur le _port serie
    #                 
    #
    #    param:    None
    #    return:   None
    """ 
    def stopReadingData(self):
        
        self.__serialReader.running = False
        self.__serialConnection.close()
        self.updateSerialConnectionState(False)
        #self.__serialWriter.running = False
        
        
    def sendCommand(self, command):
        
        if self.__serialConnection.isOpen:
            
            frame = None
            self.__serialConnection.write(frame)
            self.__history.addSentFrame(frame)
    
    @pyqtSlot(bool)     
    def on_CorruptedFrameReceived(self, corruptedFrameReceived):
        
        self.sendCommand(self.__history.getLastSentFrame())
        

"""#
# La classe SerialReader
# Description:    Classe representant un thread de lecture de donnees
#                 sur le _port serie. Celle-ci cree des frames et met a 
#                 jour les attributs du model Rocket selon les donnees
#                 recues.
#"""
class SerialReader(PyQt4.QtCore.QThread):
    
    __running = False
    
    '''Emit true is received a corupted frame(Invalid CRC)'''
    corruptedFrameReceived = PyQt4.QtCore.pyqtSignal(bool)
    
    def __init__(self,serialConnection, rocketController):
        super(PyQt4.QtCore.QThread, self).__init__()
        self.__serialConnection = serialConnection
        self.__rocketController = rocketController
    
    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self,value):
        self.__running = value
    
    """
    #    Methode dataReceived
    #    Description: Methode qui lit les donnees de la longeure dune trame et
    #                 cree une trame avec ces donnees
    #                 
    #
    #    param:    None
    #    return:   None
    """ 
    def dataReceived(self):
        
        try:
            
            self.__frame = Frame.fromByteArray(self.__serialConnection.read(Frame.RECEIVED_FRAME_LENGTH))
        
        except Exception as e:
            
            print e.message
            #self.corruptedFrameReceived.emit(True)
    
    
    """
    #    Methode handleData
    #    Description: Methode qui mets a jour les donnees de la fusees selon les donnees
    #                 de la derniere trame recue.
    #                 
    #
    #    param:    None
    #    return:   None
    """ 
    def handleData(self):
        
        self.__rocketController.updateRocketSpeed(self.__frame.data['SPEED'])
        self.__rocketController.updateRocketAcceleration(self.__frame.data['ALTITUDE'])
        self.__rocketController.updateRocketAltitude(self.__frame.data['ACCELERATION'])
        self.__rocketController.updateRocketAltitude(self.__frame.data['TEMPERATURE'])
        
        #rocketData = self.__frame.data
        #=======================================================================
        # self.__rocketController.updateRocketData(rocketData['speed'],
        #                                          rocketData['altitude'],
        #                                          rocketData['acceleration'],
        #                                          rocketData['temperature'],
        #                                          rocketData['direction'],
        #                                          rocketData['coords'],
        #                                          rocketData['ID'],
        #                                          rocketData['state'])
        #=======================================================================
    
    """
    #    Methode run
    #    Description: Ovveride de la methode run de la classe QThread, initilalise la
    #                 la connexion serie et appele les methodes necessaire lors de la
    #                 reception dune quatite suffisante de byte(longueur dune trame)
    #                 
    #
    #    param:    None
    #    return:   None
    """ 
    def run(self):
        
        
        print "Reading Data"
        
        self.__serialConnection.flush()
            
        """Tant quon ne tue pas le thread"""
        while self.__running:    
            
            """Waiting for the beginning of a frame and reading the flag"""
            while self.__serialConnection.read(1) is not Frame.FLAG:
       
                pass
            
            """Waiting for a complete frame to read"""
            if (self.__serialConnection.inWaiting() >= Frame.RECEIVED_FRAME_LENGTH):
                
            
                #data = self.__serialConnection.read(Frame.LENGTH)
                
                try:
                    
                    self.dataReceived()
                    self.handleData()
                    
                except Exception as e:
                    
                    print e.message
                
                #c = BitArray(bytes=data, length=(len(data)*8), offset=0)
                #print(c.bin)
                
                #for byte in data:
                    #print(struct.unpack_from("c",byte))
                    
                
                #print(data)
                #print(len(data))
                #print("Timestamp:")
                #print("GPS state")
                #print(struct.unpack_from("f",data[5:10]))
                
                
                                
        self.__serialConnection.isConnected = False
    
        
        
"""#
# La classe SerialWriter
# Description:    Classe representant un thread d'ecriture de donnees
#                 sur le _port serie. Celle-ci cree des trames et les 
#                 envoie sur la connexion serie recu en parametre
#                 
#"""
class SerialWriter(PyQt4.QtCore.QThread):
    
    __running = False
    
    def __init__(self,serialConnection, commandBuffer, serialReader):
        super(PyQt4.QtCore.QThread, self).__init__()
        self.__serialConnection = serialConnection
        self.__commandBuffer = commandBuffer
    
    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self,value):
        self.__running = value
    
    
    
    """
    #    Methode run
    #    Description: Ovveride de la methode run de la classe QThread, initilalise la
    #                 la connexion serie et appele les methodes necessaire lors de la
    #                 reception dune quatite suffisante de byte(longueur dune trame)
    #                 
    #
    #    param:    None
    #    return:   None
    """ 
    def run(self):
        
        
        """Tant quon ne tue pas le thread"""
        while self.__running:
            pass
                
        """Fermeture de la connextion serie lorsque le thread termine"""
        self.__serialConnection.close()
        self.__serialConnection.isConnected(False)





'''
TO DO
'''
class CommunicationHistory(object):
    
    HISTORY_DEEPNESS = 10
    
    def __init__(self):
        
        self.__sentFrameHistory = []
    
    def addSentFrame(self, sentFrame):
        
        if len(self.__sentFrameHistory) < 10:
            
            self.__sentFrameHistory.append(sentFrame)
            
        else:
            
            for i in range(1, self.HISTORY_DEEPNESS-1):
                
                self.__sentFrameHistory[i-1] = self.__sentFrameHistory[i]
            
            self.__sentFrameHistory[9]
    
    def getLastSentFrame(self):
        
        if len(self.__sentFrameHistory) is not 0:
            
            return self.__sentFrameHistory[-1]