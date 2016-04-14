import PyQt4
from PyQt4.Qt import pyqtSlot
from src.controller.RocketController import RocketController
from src.controller.Communication import SerialController
from src.controller.Communication import RFD900Strategy, XbeeStrategy, FrameFactory
from src.model.BaseStation import BaseStation
from src.model.Rocket import Rocket
from src.controller.GPS import GlobalSat

class BaseStationController(PyQt4.QtCore.QObject):
    
    __INSTANCE = None

    def __init__(self):
        
        self.__rocketController = RocketController.getInstance()
        self.__baseStationModel = BaseStation()

        self.__RFD900SerialController = SerialController()
        self.__XBeeSerialController = SerialController()
        self.__globalSatSerialController = SerialController()
        self.__globalSatSerialController.updateSerialConnectionBaudrate(4800)
        self.__globalSatSerialController.updateSerialConnectionPort("/dev/ttyS0")

        self.__RFD900 = RFD900Strategy(self.__rocketController, self.__RFD900SerialController.serialConnection)
        self.__XBee = XbeeStrategy(self.__rocketController, self.__XBeeSerialController.serialConnection)
        self.__gpsDevice = GlobalSat(self.__globalSatSerialController)
        self.__gpsDevice.connect()

        self.__RFD900.rocketDiscovered.connect(self.__on_rocketDiscovery)
        self.__gpsDevice.coordsReceived.connect(self.__on_coordsReceived)


    @property
    def baseStation(self):
        return self.__baseStationModel

    @baseStation.setter
    def baseStation(self, baseStationModel):
        self.__baseStationModel = baseStationModel

    @property
    def rocketController(self):
        return self.__rocketController

    @rocketController.setter
    def rocketController(self, rocketController):
        self.__rocketController = rocketController

    @property
    def RFD900SerialController(self):
        return self.__RFD900SerialController

    @property
    def XBeeSerialController(self):
        return self.__XBeeSerialController

    @property
    def GlobalSatSerialController(self):
        return self.__globalSatSerialController

    @GlobalSatSerialController.setter
    def GlobalSatSerialController(self, serialController):
        self.__globalSatSerialController = serialController

    @property
    def RFD900(self):
        return self.__RFD900

    @RFD900.setter
    def RFD900(self, rfdCommStrategy):
        self.__RFD900 = rfdCommStrategy

    @property
    def XBee(self):
        return self.__XBee

    @XBee.setter
    def XBee(self, xbeeCommStrategy):
        self.__XBee = xbeeCommStrategy

    def updateAvailableRocket(self):

        self.__baseStationModel.availableRocket = {}
        self.__RFD900.sendData(FrameFactory.COMMAND['ROCKET_DISCOVERY'])

    def updateConnectedRocket(self, rocketID):

        self.__baseStationModel.connectedRocket = self.__baseStationModel.availableRocket[rocketID]

    def disconnectFromRocket(self, rocketID):

        if self.__baseStationModel.connectedRocket.ID == rocketID:

            self.__baseStationModel.connectedRocket = None

    @pyqtSlot(int)
    def __on_rocketDiscovery(self, rocketID):

        if rocketID not in self.__baseStationModel.availableRocket:

            self.__baseStationModel.availableRocket[rocketID] = Rocket()

    @pyqtSlot(float, float)
    def __on_coordsReceived(self, latitude, longitude):

        self.baseStation.coords = {"latitude": latitude, "longitude": longitude}


    @staticmethod
    def getInstance():
        
        if BaseStationController.__INSTANCE is None:
            BaseStationController.__INSTANCE = BaseStationController()
            
        return BaseStationController.__INSTANCE