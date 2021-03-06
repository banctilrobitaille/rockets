import PyQt4
import time
from model.Frame import ReceivedFrame, SentFrame, Frame
from model.SerialConnection import SerialConnection
from PyQt4.Qt import pyqtSlot
from Exception import SerialDeviceException
from controller.LogController import LogController
from controller.AnalyticsController import CommunicationAnalyticsController
from controller.FlightController import FlightController
from datetime import datetime

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
    deviceNameChanged = PyQt4.QtCore.pyqtSignal(str)

    def __init__(self):

        super(SerialController, self).__init__()
        self.__serialConnection = SerialConnection()
        self.__LOGGER = LogController.getInstance()

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

        try:
            self.updateSerialConnectionPort(port, verbose=False)
            self.updateSerialConnectionBaudrate(baudrate, verbose=False)
            self.updateSerialConnectionStopbits(stopbits, verbose=False)
            self.updateSerialConnectionParity(parity, verbose=False)
            self.updateSerialConnectionByteSize(bytesize, verbose=False)
            self.__LOGGER.success("Sucessfully updated {} settings".format(self.serialConnection.deviceName))
        except SerialDeviceException.UnableToConfigureException as e:
            raise

    """
    #    Methode updateSerialConnectionPort
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le _port de la connexion serie
    #
    #    param:       _port, le _port serie ex: /dev/ttyS0
    #    return: None
    """

    def updateSerialConnectionPort(self, port, verbose=True):
        try:
            self.__serialConnection.port = port
            self.portChanged.emit(port)
            if verbose:
                self.__LOGGER.success("Sucessfully updated serial port to: \n" + str(port))
        except Exception as e:
            self.__LOGGER.error("Unable to update device serial port to: \n" + port)
            raise SerialDeviceException.UnableToConfigureException("Unable to update device serial port to:" + port)

    """
    #    Methode updateSerialConnectionBaudrate
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le _baudrate de la connexion serie
    #
    #    param:       _baudrate, le _baudrate du _port serie
    #    return: None
    """

    def updateSerialConnectionBaudrate(self, baudrate, verbose=True):
        try:
            self.__serialConnection.baudrate = baudrate
            self.baudrateChanged.emit(baudrate)
            if verbose:
                self.__LOGGER.success("Sucessfully updated serial port baudrate to: \n" + str(baudrate))
        except Exception:
            self.__LOGGER.error("Unable to update serial device baudrate to:\n" + str(baudrate))
            raise SerialDeviceException.UnableToConfigureException(
                    "Unable to update serial device baudrate to: " + str(baudrate))

    """
    #    Methode updateSerialConnectionStopbits
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le _stopbits de la connexion serie
    #
    #    param:       _stopbits, le _stopbits ex: serial.STOPBITS_ONE
    #    return: None
    """

    def updateSerialConnectionStopbits(self, stopbits, verbose=True):
        try:
            self.__serialConnection.stopbits = stopbits
            self.stopbitsChanged.emit(stopbits)
            if verbose:
                self.__LOGGER.success("Sucessfully updated serial port stopbit to: \n" + str(stopbits))
        except Exception:
            self.__LOGGER.error("Unable to update serial device stopbits to:\n" + str(stopbits))
            raise SerialDeviceException.UnableToConfigureException(
                    "Unable to update serial device stopbits to: " + str(stopbits))

    """
    #    Methode updateSerialConnectionParity
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour la parite de la connexion serie
    #
    #    param:       _parity, la parite ex: serial.PARITY_NONE
    #    return: None
    """

    def updateSerialConnectionParity(self, parity, verbose=True):
        try:
            self.__serialConnection.parity = parity
            self.parityChanged.emit(parity)
            if verbose:
                self.__LOGGER.success("Sucessfully updated serial port parity to: \n" + str(parity))
        except Exception:
            self.__LOGGER.error("Unable to update serial device parity to:\n" + str(parity))
            raise SerialDeviceException.UnableToConfigureException(
                    "Unable to update serial device parity to: " + str(parity))

    """
    #    Methode updateSerialConnectionByteSize
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour le nombre de bits envoyes par la connexion serie
    #
    #    param:       _bytesize, le nombre de bits envoye ex: serial.EIGHTBITS
    #    return: None
    """

    def updateSerialConnectionByteSize(self, bytesize, verbose=True):
        try:
            self.__serialConnection.bytesize = bytesize
            self.bytesizeChanged.emit(bytesize)
            if verbose:
                self.__LOGGER.success("Sucessfully updated serial port bytesize to: \n" + str(bytesize))
        except Exception:
            self.__LOGGER.error("Unable to update serial device bytesize to:\n" + str(bytesize))
            raise SerialDeviceException.UnableToConfigureException(
                    "Unable to update serial device bytesize to: " + str(bytesize))

    def updateSerialConnectionDeviceName(self, deviceName, verbose=True):
        try:
            self.__serialConnection.deviceName = deviceName
            self.deviceNameChanged.emit(deviceName)
            if verbose:
                self.__LOGGER.success("Sucessfully updated serial device name to: \n" + deviceName)
        except Exception:
            self.__LOGGER.error("Unable to update serial device name to:\n" + deviceName)
            raise SerialDeviceException.UnableToConfigureException(
                    "Unable to update serial device name to: " + deviceName)

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
        self.__LOGGER = LogController.getInstance()

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, value):
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

        while self.__running:

            if self.__serialConnection.inWaiting() >= ReceivedFrame.LENGTH:
                while self.__serialConnection.read(1) is not Frame.FLAG:
                    pass

                try:
                    self.frameReceived.emit(self.__serialConnection.read(ReceivedFrame.LENGTH - 1))
                except Exception as e:
                    self.__LOGGER.error(e.message, verbose=False)


class CommunicationStrategy(PyQt4.QtCore.QObject):
    rocketDiscovered = PyQt4.QtCore.pyqtSignal(int)
    newCommandStreamer = PyQt4.QtCore.pyqtSignal(object)
    discoveringRocket = PyQt4.QtCore.pyqtSignal(bool)

    def __init__(self, rocketController):
        super(CommunicationStrategy, self).__init__()
        self.__LOGGER = LogController.getInstance()
        self.__rocketController = rocketController
        self.__history = CommunicationHistory()
        self.__commandStreamer = {}
        self.__ID = 0
        self.__isDiscoveringRocket = False
        self.__rocketDiscoveryStreamer = None

    @property
    def LOGGER(self):
        return self.__LOGGER

    @property
    def rocketDiscoveryStreamer(self):
        return self.__rocketDiscoveryStreamer

    @rocketDiscoveryStreamer.setter
    def rocketDiscoveryStreamer(self, rocketDiscoveryStreamer):
        self.__rocketDiscoveryStreamer = rocketDiscoveryStreamer

    @property
    def isDiscoveringRocket(self):
        return self.__isDiscoveringRocket

    @isDiscoveringRocket.setter
    def isDiscoveringRocket(self, state):
        self.__isDiscoveringRocket = state
        self.discoveringRocket.emit(state)

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, value):
        self.__ID = value

    @property
    def commandStreamer(self):
        return self.__commandStreamer

    @commandStreamer.setter
    def commandStreamer(self, commandStreamer):
        self.__commandStreamer = commandStreamer

    def addCommandStreamer(self, commandStreamer):
        CommunicationAnalyticsController.getInstance().incrementNbOfCommandSent(FrameFactory.COMMAND_STRING[commandStreamer.command])
        self.__commandStreamer[str(self.__ID)] = commandStreamer
        commandStreamer.isRunning = True
        self.newCommandStreamer.emit(commandStreamer)
        commandStreamer.start()
        self.__ID += 1

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

    def reconnect(self):
        raise NotImplementedError

    def startRocketDiscovery(self):
        raise NotImplementedError

    def stopRocketDiscovery(self):
        raise NotImplementedError

    def startCamera(self):
        raise NotImplementedError

    def stopCamera(self):
        raise NotImplementedError

    def startStream(self):
        raise NotImplementedError

    def stopStream(self):
        raise NotImplementedError

    def resendLastCommand(self):
        self.addCommandStreamer(CommandStream(self.serialConnection, self.rocketController.rocket.ID,
                                              command=self.history.getLastCommand(), ID=self.ID, timeout=5, interval=5))

    @pyqtSlot(object)
    def on_received_data(self, receivedData):
        raise NotImplementedError


class SerialDeviceStrategy(CommunicationStrategy):
    def __init__(self, rocketController, serialConnection):

        super(SerialDeviceStrategy, self).__init__(rocketController)
        self.__serialConnection = serialConnection
        self.__serialReader = SerialReader(self.__serialConnection)
        self.__serialReader.frameReceived.connect(self.on_received_data)

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
            raise SerialDeviceException.UnableToConnectException(
                    "Unable to connect {}: \n".format(self.serialConnection.deviceName))

    def disconnect(self):

        try:
            self.__serialReader.running = False
            self.__serialConnection.close()
            self.__serialConnection.isConnected = False

        except Exception as e:
            raise SerialDeviceException.UnableToDisconnectException(
                    "Unable to disconnect {}: \n".format(self.serialConnection.deviceName))


class RFD900Strategy(SerialDeviceStrategy):
    def __init__(self, rocketController, serialConnection):
        super(RFD900Strategy, self).__init__(rocketController, serialConnection)
        self.__streaming = False

    @property
    def streaming(self):
        return self.__streaming

    @streaming.setter
    def streaming(self, streaming):
        self.__streaming = streaming

    def startRocketDiscovery(self):
        try:
            self.rocketDiscoveryStreamer = CommandStream(self.serialConnection,
                                                         rocketID=self.rocketController.rocket.DISCOVERY_ID,
                                                         ID=self.ID, command=FrameFactory.COMMAND['ROCKET_DISCOVERY'],
                                                         interval=0.1)
            self.addCommandStreamer(self.rocketDiscoveryStreamer)
            self.isDiscoveringRocket = True
        except Exception as e:
            self.LOGGER.error("Unable to enter in rocket discovery mode")

        self.LOGGER.success("Sucessfully entered in rocket discovery mode !")

    def stopRocketDiscovery(self):
        try:
            if self.isDiscoveringRocket:
                self.rocketDiscoveryStreamer.kill()
                self.rocketDiscoveryStreamer.wait(3000)
                self.rocketDiscoveryStreamer = None
                self.isDiscoveringRocket = False
        except Exception as e:
            self.LOGGER.error("Unable to leave rocket discovery mode")

        self.LOGGER.success("Sucessfully leaved rocket discovery mode !")

    def startStream(self):

        self.addCommandStreamer(CommandStream(self.serialConnection, rocketID=self.rocketController.rocket.ID,
                                              command=FrameFactory.COMMAND['START_STREAM'], ID=self.ID,
                                              timeout=15, interval=0.1))
        self.__streaming = True

    def stopStream(self):

        self.addCommandStreamer(CommandStream(self.serialConnection, rocketID=self.rocketController.rocket.ID,
                                              command=FrameFactory.COMMAND['STOP_STREAM'], ID=self.ID,
                                              timeout=15, interval=0.1))
        self.__streaming = False

    @pyqtSlot(object)
    def on_received_data(self, receivedData):

        CommunicationAnalyticsController.getInstance().incrementNbOfFrameReceived()
        receivedFrame = FrameFactory.create(FrameFactory.FRAMETYPES['RECEIVED'], receivedData=receivedData)

        if receivedFrame.rocketID is self.rocketController.rocket.ID or receivedFrame.command \
                is FrameFactory.COMMAND['ROCKET_DISCOVERY']:

            if receivedFrame.command == FrameFactory.COMMAND['ACK']:

                if str(receivedFrame.ID) in self.commandStreamer:
                    self.commandStreamer[str(receivedFrame.ID)].kill()
                    self.commandStreamer[str(receivedFrame.ID)].wait(3000)
                    del self.commandStreamer[str(receivedFrame.ID)]

                if not self.__streaming and self.rocketController.rocket.isStreaming:
                    self.rocketController.rocket.isStreaming = False
                elif not self.__streaming and not self.rocketController.rocket.isStreaming:
                    self.rocketController.rocket.isStreaming = True

            elif receivedFrame.command == FrameFactory.COMMAND['GET_TELEMETRY']:

                if str(receivedFrame.ID) in self.commandStreamer:
                    self.commandStreamer[str(receivedFrame.ID)].kill()
                    self.commandStreamer[str(receivedFrame.ID)].wait(5000)
                    del self.commandStreamer[str(receivedFrame.ID)]

                if self.__streaming and not self.rocketController.rocket.isStreaming:
                    self.rocketController.rocket.isStreaming = True

                self.rocketController.updateRocketState(receivedFrame.state)
                self.rocketController.updateRocketSpeedFromAltitude(receivedFrame.altitude)
                self.rocketController.updateRocketAltitude(receivedFrame.altitude)
                self.rocketController.updateRocketAccelerationFromSpeed()
                self.rocketController.updateRocketTemperature(receivedFrame.temperature)
                self.rocketController.updateRocketCoords({'longitude': receivedFrame.longitude,
                                                          'latitude' : receivedFrame.latitude})

                FlightController.getInstance().updateStateTime(receivedFrame.state)
                FlightController.getInstance().updateApogee(receivedFrame.altitude)
                FlightController.getInstance().updateMaxSpeed(self.rocketController.rocket.speed)
                FlightController.getInstance().updateMaxAcceleration(self.rocketController.rocket.acceleration)
                FlightController.getInstance().updateMinTemperature(receivedFrame.temperature)
                FlightController.getInstance().updateMaxTemperature(receivedFrame.temperature)

                if self.rocketController.rocket.currentState is self.rocketController.rocket.STATE['ON_THE_PAD']:
                    FlightController.getInstance().updateLaunchCoordinate({'longitude': receivedFrame.longitude,
                                                                           'latitude' : receivedFrame.latitude})
                elif self.rocketController.rocket.currentState is self.rocketController.rocket.STATE['ON_THE_GROUND']:
                    FlightController.getInstance().updateLandCoordinate({'longitude': receivedFrame.longitude,
                                                                         'latitude' : receivedFrame.latitude})

            elif receivedFrame.command == FrameFactory.COMMAND['ROCKET_DISCOVERY']:

                self.rocketDiscovered.emit(receivedFrame.rocketID)

            elif receivedFrame.command == FrameFactory.COMMAND['NACK']:

                self.resendLastCommand()
                self.LOGGER.error("Bad frame sent, received NACK", verbose=False)
                CommunicationAnalyticsController.incrementNbOfBadFrameSent()
            else:
                CommunicationAnalyticsController.incrementNbOfBadFrameReceived()


class XbeeStrategy(SerialDeviceStrategy):
    def __init__(self, rocketController, serialConnection):
        super(XbeeStrategy, self).__init__(rocketController, serialConnection)

    def StartCamera(self):

        self.addCommandStreamer(CommandStream(self.serialConnection, rocketID=self.rocketController.rocket.ID,
                                              command=FrameFactory.COMMAND['START_CAMERA'], ID=self.ID, timeout=15,
                                              interval=0.1))

    def StopCamera(self):

        self.addCommandStreamer(CommandStream(self.serialConnection, rocketID=self.rocketController.rocket.ID,
                                              command=FrameFactory.COMMAND['STOP_CAMERA'], ID=self.ID, timeout=5,
                                              interval=0.1))

    def on_received_data(self, receivedData):

        receivedFrame = FrameFactory.create(FrameFactory.FRAMETYPES['RECEIVED'], receivedData=receivedData)
        CommunicationAnalyticsController.getInstance().incrementNbOfFrameReceived()

        if receivedFrame.command is FrameFactory.COMMAND['ACK']:

            try:
                self.commandStreamer[str(receivedFrame.ID)].kill()
                self.commandStreamer[str(receivedFrame.ID)].wait(5000)
                del self.commandStreamer[str(receivedFrame.ID)]

                self.rocketController.updateRocketCameraState()

            except Exception as e:
                pass
        else:
            CommunicationAnalyticsController.getInstance().incrementNbOfBadFrameReceived()


class FrameFactory(object):
    FRAMETYPES = {'SENT': 0, 'RECEIVED': 1}

    COMMAND = {
        'ACK'             : 0x01,
        'GET_TELEMETRY'   : 0x02,
        'START_STREAM'    : 0x03,
        'STOP_STREAM'     : 0x04,
        'START_CAMERA'    : 0x05,
        'STOP_CAMERA'     : 0x06,
        'GET_LOG'         : 0x07,
        'NACK'            : 0x08,
        'ROCKET_DISCOVERY': 0x1F,
    }

    COMMAND_STRING = {
        0x01 : 'ACK',
        0x02 : 'GET TELEMETRY',
        0x03 : 'START STREAM',
        0x04 : 'STOP STREAM',
        0x05 : 'START CAMERA',
        0x06 : 'STOP CAMERA',
        0x07 : 'GET LOG',
        0x08 : 'NACK',
        0x1F : 'ROCKET DISCOVERY',
    }

    """The broadcast ID treated by every rocket"""
    DISCOVERY_ID = 0xE0

    def __init__(self):
        pass

    @staticmethod
    def create(frameType=None, rocketID=None, command=0x00, ID=0, timestamp=None, payload=0x00, receivedData=None):

        frame = None

        if frameType is FrameFactory.FRAMETYPES['SENT']:

            if timestamp is None:
                frame = SentFrame(rocketID, command, ID, time.time(), payload)
            else:
                frame = SentFrame(rocketID, command, ID, timestamp, payload)

        elif frameType is FrameFactory.FRAMETYPES['RECEIVED']:

            frame = ReceivedFrame.fromByteArray(receivedData)

        return frame


class CommandStream(PyQt4.QtCore.QThread):
    commandStreamStarted = PyQt4.QtCore.pyqtSignal(bool)
    commandStreamEnded = PyQt4.QtCore.pyqtSignal(bool)

    def __init__(self, serialConnection, rocketID=None, command=None, ID=None, timeout=None, interval=1):
        super(CommandStream, self).__init__()
        self.__serialConnection = serialConnection
        self.__rocketID = rocketID
        self.__command = command
        self.__timeout = timeout
        self.__interval = interval
        self.__isRunning = False
        self.__timer = None
        self.__ID = ID
        self.__inError = False
        self.__LOGGER = LogController.getInstance()

        if timeout is not None:
            self.__timer = PyQt4.QtCore.QTimer()
            self.__timer.setSingleShot(True)
            self.__timer.timeout.connect(self.__on_Timer_Ended)

    @property
    def rocketID(self):
        return self.__rocketID

    @rocketID.setter
    def rocketID(self, ID):
        self.__rocketID = ID

    @property
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, ID):
        self.__ID = ID

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
    def serialConnection(self, serialConnection):
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

        self.commandStreamEnded.emit(self.__inError)
        self.__LOGGER.error("Rocket did not respond to command: \n" + commandString)

    def kill(self):

        self.__isRunning = False
        if self.__timeout is not None:
            self.__timer.stop()

        self.commandStreamEnded.emit(self.__inError)

    def run(self):

        if self.__timer is not None:
            self.__timer.start(self.__timeout * 1000)

        self.commandStreamStarted.emit(True)

        while self.__isRunning:
            try:
                frame = FrameFactory.create(FrameFactory.FRAMETYPES['SENT'], rocketID=self.__rocketID,
                                            ID=self.ID, command=self.command)
                self.__serialConnection.write(Frame.FLAG + frame.toByteArray(withCRC=True))
                CommunicationAnalyticsController.getInstance().incrementNbOfFrameSent()
                CommunicationAnalyticsController.getInstance().incrementNbOfRetries(datetime.now())
                time.sleep(self.__interval)
                CommunicationAnalyticsController.getInstance().incrementNbOfFrameLost()
            except Exception as e:
                self.__LOGGER.error("Error while sending command on port: \n" + self.serialConnection.port +
                                    "\n" + e.message)
                self.__inError = True
                self.kill()


'''
TO DO
'''


class CommunicationHistory(object):
    HISTORY_DEEPNESS = 10

    def __init__(self):

        self.__commandHistory = []

    def addSentCommand(self, command):

        if len(self.__commandHistory) < 10:

            self.__commandHistory.append(command)

        else:

            for i in range(1, self.HISTORY_DEEPNESS - 1):
                self.__commandHistory[i - 1] = self.__commandHistory[i]

            self.__commandHistory[self.HISTORY_DEEPNESS - 1] = command

    def getLastCommand(self):

        if len(self.__commandHistory) is not 0:
            return self.__commandHistory[-1]
