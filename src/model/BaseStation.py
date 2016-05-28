import PyQt4
from model.Rocket import Rocket
'''
Created on 2016-01-04

@author: rockets
'''


class BaseStation(PyQt4.QtCore.QObject):

    
    """
    Comments TODO
    """
    coordsChanged = PyQt4.QtCore.pyqtSignal(float, float)
    temperatureChanged = PyQt4.QtCore.pyqtSignal(float)
    availableRocketChanged = PyQt4.QtCore.pyqtSignal(object)
    connectedRocketChanged = PyQt4.QtCore.pyqtSignal(object)


    def __init__(self):
    
        super(PyQt4.QtCore.QObject, self).__init__()
        self.__temperature = 0
        self.__coords = {}
        self.__connectedRocket = None
        self.__availableRocket = {Rocket.DISCOVERY_ID: Rocket(ID=Rocket.DISCOVERY_ID, name="Broadcast"), }
    

    @property
    def connectedRocket(self):
        return self.__connectedRocket

    @connectedRocket.setter
    def connectedRocket(self, rocket):
        self.__connectedRocket = rocket
        self.connectedRocketChanged.emit(self.__connectedRocket)

    @property
    def availableRocket(self):
        return self.__availableRocket

    @availableRocket.setter
    def availableRocket(self, availableRocket):

        self.__availableRocket = availableRocket
        self.availableRocketChanged.emit(self.__availableRocket)

    def addAvailableRocket(self, rocket):

        if rocket.ID not in self.__availableRocket:
            self.__availableRocket[rocket.ID] = rocket
            self.availableRocketChanged.emit(self.__availableRocket)

    @property
    def temperature(self):
        
        return self.__temperature
    
    @temperature.setter
    def temperature(self, temperature):
        
        self.__temperature = temperature
        self.temperatureChanged.emit(self.__temperature)
        
    @property
    def coords(self):
        
        return self.__coords
    
    @coords.setter
    def coords(self, coordsDict):
        
        self.__coords['longitude'] = coordsDict['longitude']
        self.__coords['latitude'] = coordsDict['latitude']
        self.coordsChanged.emit(self.__coords['latitude'], self.__coords['longitude'])