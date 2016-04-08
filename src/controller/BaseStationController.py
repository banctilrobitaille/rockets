import PyQt4
from PyQt4.Qt import pyqtSlot
from src.controller.RocketController import RocketController
from src.controller.Communication import SerialController
from src.controller.Communication import RFD900Strategy, XbeeStrategy, FrameFactory
from src.model.BaseStation import BaseStation
from src.model.Rocket import Rocket

class BaseStationController(PyQt4.QtCore.QObject):
    
    __INSTANCE = None

    def __init__(self):
        
        self.__rocketController = RocketController.getInstance()
        self.__baseStationModel = BaseStation()
        self.__RFD900SerialController = SerialController()
        self.__XBeeSerialController = SerialController()
        self.__RFD900 = RFD900Strategy(self.__rocketController, self.__RFD900SerialController.serialConnection)
        self.__XBee = XbeeStrategy(self.__rocketController, self.__XBeeSerialController.serialConnection)

        self.__RFD900.rocketDiscovered.connect(self.__on_rocketDiscovery)
    

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
    def RFD900(self):
        return self.__RFD900

    @RFD900.setter
    def RFD900(self, rfdCommStrategy):
        self.__RFD900 = rfdCommStrategy

    @property
    def XBee(self):
        return self.__XBee

    @XBee.setter
    def Xbee(self, xbeeCommStrategy):
        self.__XBee = xbeeCommStrategy


    def updateAvailableRocket(self):

        self.__baseStationModel.availableRocket = {}
        self.__RFD900.sendData(FrameFactory.COMMAND['ROCKET_DISCOVERY'])


    @pyqtSlot(int)
    def __on_rocketDiscovery(self, rocketID):

        if not self.__baseStationModel.availableRocket.has_key(rocketID):

            self.__baseStationModel.availableRocket[rocketID] = Rocket()


    @staticmethod
    def getInstance():
        
        if BaseStationController.__INSTANCE is None:
            BaseStationController.__INSTANCE = BaseStationController()
            
        return BaseStationController.__INSTANCE