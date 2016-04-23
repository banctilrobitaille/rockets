import serial
import PyQt4
import time
from src.model.Frame import ReceivedFrame, SentFrame
from src.model.SerialConnection import SerialConnection
from PyQt4.Qt import pyqtSlot
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
    
    def __init__(self):
        
        super(PyQt4.QtCore.QObject,self).__init__()
        self.__serialConnection = SerialConnection()

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


"""#
# La classe SerialReader
# Description:    Classe representant un thread de lecture de donnees
#                 sur le _port serie. Celle-ci cree des frames et met a 
#                 jour les attributs du model Rocket selon les donnees
#                 recues.
#"""


class SerialReader(PyQt4.QtCore.QThread):
    
    __running = False

    frameReceived = PyQt4.QtCore.pyqtSignal(object)
    
    def __init__(self, serialConnection):
        super(PyQt4.QtCore.QThread, self).__init__()
        self.__serialConnection = serialConnection

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
        
        self.__serialConnection.flush()
            
        """Tant quon ne tue pas le thread"""
        while self.__running:    
            
            """Waiting for the beginning of a frame and reading the flag"""
            while self.__serialConnection.read(1) is not ReceivedFrame.FLAG:
       
                pass
            
            """Waiting for a complete frame to read"""
            if self.__serialConnection.inWaiting() >= ReceivedFrame.LENGTH:

                try:
                    
                    self.frameReceived.emit(self.__serialConnection.read(ReceivedFrame.LENGTH))
                    
                except Exception as e:
                    
                    print e.message


class CommunicationStrategy(PyQt4.QtCore.QObject):

    rocketDiscovered = PyQt4.QtCore.pyqtSignal(int)
    rocketDidNotRespond = PyQt4.QtCore.pyqtSignal(str)
    newCommandStreamer = PyQt4.QtCore.pyqtSignal(object)

    def __init__(self, rocketController):
        super(CommunicationStrategy, self).__init__()
        self.__rocketController = rocketController
        self.__history = CommunicationHistory()
        self.__commandStreamer = {'RocketDiscovery': None,}

    @property
    def commandStreamer(self):
        return self.__commandStreamer

    @commandStreamer.setter
    def commandStreamer(self, commandStreamer):
        self.__commandStreamer = commandStreamer

    def addCommandStreamer(self, blockID, commandStreamer):

        self.__commandStreamer[blockID] = commandStreamer
        self.newCommandStreamer.emit(commandStreamer)

    @property
    def rocketController(self):
        return self.__rocketController

    @rocketController.setter
    def rocketController(self, rocketController):
        self.__rocketController = rocketController

    @property
    def history(self):
        return self.__history

    @history.setter
    def history(self, communicationHistory):
        self.__history = communicationHistory

    def connect(self):

        raise NotImplementedError

    def disconnect(self):

        raise NotImplementedError

    def sendData(self, data):

        raise NotImplementedError

    def startRocketDiscovery(self):

        raise NotImplementedError

    def stopRocketDiscovery(self):

        raise NotImplementedError

    @pyqtSlot(object)
    def __on_received_data(self, receivedData):

        raise NotImplementedError

    @pyqtSlot(str)
    def on_Rocket_Did_Not_Respond(self, errorMessage):

        self.rocketDidNotRespond.emit(errorMessage)

class SerialDeviceStrategy(CommunicationStrategy):

    def __init__(self, rocketController, serialConnection):

        super(SerialDeviceStrategy, self).__init__(rocketController)
        self.__serialConnection = serialConnection
        self.__serialReader = SerialReader(self.__serialConnection)

    @property
    def serialConnection(self):
        return self.__serialConnection

    @serialConnection.setter
    def serialConnection(self, serialConnection):
        self.__serialConnection = serialConnection

    @property
    def serialReader(self):
        return self.__serialReader

    @serialReader.setter
    def serialReader(self, serialReader):
        self.__serialReader = serialReader

    def connect(self):

        try:
            self.__serialConnection.open()
            self.__serialConnection.isConnected = True
            self.__serialReader.running = True
            self.__serialReader.start()

        except Exception as e:

                print(e.message)

    def disconnect(self):

        try:
            self.__serialReader.running = False
            self.__serialConnection.close()
            self.__serialConnection.isConnected = False

        except Exception as e:

            print(e.message)


class RFD900Strategy(SerialDeviceStrategy):

    def __init__(self, rocketController, serialConnection):
        super(RFD900Strategy, self).__init__(rocketController, serialConnection)
        self.__streaming = False
        self.serialReader.frameReceived.connect(self.__on_received_data)
        self.__rocketDiscoveryThread = None

    @property
    def streaming(self):
        return self.__streaming

    @streaming.setter
    def streaming(self, streaming):
        self.__streaming = streaming

    def startRocketDiscovery(self):

        self.addCommandStreamer('RocketDiscovery', CommandStream(self.serialConnection,
                                                                 command=FrameFactory.COMMAND['ROCKET_DISCOVERY']
                                                                 , timeout=5, interval=5))
        self.commandStreamer['RocketDiscovery'].isRunning = True
        self.commandStreamer['RocketDiscovery'].rocketDidNotRespond.connect(self.on_Rocket_Did_Not_Respond)
        self.commandStreamer['RocketDiscovery'].start()

    def stopRocketDiscovery(self):

        if self.commandStreamer['RocketDiscovery'] is not None:

            self.commandStreamer['RocketDiscovery'].isRunning = False
            self.commandStreamer['RocketDiscovery'] = None


    def sendData(self, data, blockID=None):

        command = data

        if not self.serialConnection.isConnected:
            self.connect()

        if command == FrameFactory.COMMAND['START_STREAM']:
            self.__streaming = True
        elif command == FrameFactory.COMMAND['STOP_STREAM']:
            self.__streaming = False

        self.serialConnection.write(FrameFactory.create(FrameFactory.FRAMETYPES['SENT'],\
                                                        command=command).toByteArray(withCRC=True))

    def resendLastCommand(self):

        self.sendData(self.history.getLastSentFrame().command)

    @pyqtSlot(object)
    def __on_received_data(self, receivedData):

        receivedFrame = FrameFactory.create(FrameFactory.FRAMETYPES['RECEIVED'], receivedData)

        if receivedFrame.isValid():

            if receivedFrame.command == FrameFactory.COMMAND['START_STREAM'] or receivedFrame.command \
                    == FrameFactory.COMMAND['GET_TELEMETRY']:

                self.rocketController.updateRocketSpeed(receivedFrame.speed)
                self.rocketController.updateRocketAcceleration(receivedFrame.acceleration)
                self.rocketController.updateRocketAltitude(receivedFrame.altitude)
                self.rocketController.updateRocketAltitude(receivedFrame.temperature)
                self.rocketController.updateRocketCoords([receivedFrame.longitude, receivedFrame.latitude])

            elif receivedFrame.command == FrameFactory.COMMAND['ROCKET_DISCOVERY']:

                self.rocketDiscovered.emit(receivedFrame.rocketID)

            elif receivedFrame.command == FrameFactory.COMMAND['NACK']:

                self.resendLastCommand()

        elif self.history.getLastSentFrame().command != FrameFactory.COMMAND['START_STREAM']:

            self.resendLastCommand()



class XbeeStrategy(SerialDeviceStrategy):

    def __init__(self, rocketController, serialConnection):
        super(XbeeStrategy, self).__init__(rocketController, serialConnection)


class FrameFactory(object):

    FRAMETYPES = {'SENT' : 0, 'RECEIVED' : 1}

    COMMAND = {
        'GET_TELEMETRY'     : 0x01,
        'START_STREAM'      : 0x02,
        'STOP_STREAM'       : 0x03,
        'START_CAMERA'      : 0x04,
        'STOP_CAMERA'       : 0x05,
        'GET_LOG'           : 0x06,
        'NACK'              : 0x07,
        'ROCKET_DISCOVERY'  : 0x1F,
    }

    """The broadcast ID treated by every rocket"""
    DISCOVERY_ID = 0xF0

    def __init__(self):
        pass

    @staticmethod
    def create(frameType=None, rocketID=None, command=0x00,timestamp=None, payload=0x00, receivedData=None):

        frame = None

        if frameType is FrameFactory.FRAMETYPES['SENT']:

            if timestamp is None:
                frame = SentFrame(rocketID, command, time.time(), payload)
            else:
                frame = SentFrame(rocketID, command, timestamp, payload)

        elif frameType is FrameFactory.FRAMETYPES['RECEIVED']:

            frame = ReceivedFrame.fromByteArray(receivedData)

        return frame


class CommandStream(PyQt4.QtCore.QThread):

    commandStreamStarted    = PyQt4.QtCore.pyqtSignal(bool)
    commandStreamEnded      = PyQt4.QtCore.pyqtSignal(bool)
    rocketDidNotRespond     = PyQt4.QtCore.pyqtSignal(str)

    def __init__(self, serialConnection, command=None, timeout=None, interval=1):
        super(CommandStream, self).__init__()
        self.__serialConnection = serialConnection
        self.__command = command
        self.__timeout = timeout
        self.__interval = interval
        self.__isRunning = False
        self.__timer = None

        if timeout is not None:

            self.__timer = PyQt4.QtCore.QTimer()
            self.__timer.setSingleShot(True)
            self.__timer.timeout.connect(self.__on_Timer_Ended)

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, command):
        self.__command = command

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, second):
        self.__timeout = second

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, second):
        self.__interval = second

    @property
    def serialConnection(self):
        return self.__serialConnection

    @serialConnection.setter
    def serialConnection(self,serialConnection):
        self.__serialConnection = serialConnection

    @property
    def isRunning(self):
        return self.__isRunning

    @isRunning.setter
    def isRunning(self, bool):

        self.__isRunning = bool

    @property
    def timer(self):
        return self.__timer

    @timer.setter
    def timer(self, timer):
        self.__timer = timer

    @pyqtSlot()
    def __on_Timer_Ended(self):

        self.__isRunning = False
        commandString = None

        for command, value in FrameFactory.COMMAND.iteritems():

            if value == self.__command:

                commandString = command

        self.rocketDidNotRespond.emit("Rocket did not respond to command: \n" + commandString)

    def run(self):

        if self.__timer is not None:

            self.__timer.start(self.__timeout*1000)

        while self.__isRunning:

            frame = FrameFactory.create(FrameFactory.FRAMETYPES['SENT'], FrameFactory.COMMAND['ROCKET_DISCOVERY'])
            #self.__serialConnection.write(frame.toByteArray(withCRC=True))
            time.sleep(self.__interval)

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