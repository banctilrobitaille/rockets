import PyQt4
from src.model.ModelUtils import DataOverTimeHistory
"""#############################################################################
# 
# Nom du module:          Rocket
# Auteur:                 Benoit Anctil-Robitaille
# Date:                   5 janvier 2016
# Description:            Le module Rocket.py inclus les classes et methodes
#                         permettant d'affecter ou lire les differents etats
#                         de la fusee en vol.
#
##############################################################################"""


"""#
# La classe Rocket
# Description:    Classe representant la fusee en vol. Cette classe fournie
#                 l'interface necessaire a l'affectation et lecture des 
#                 donnees de la fusee.
#"""


class Rocket(PyQt4.QtCore.QObject):
    
    __INSTANCE = None
    
    """Signal to update the view"""
    accelerationChanged = PyQt4.QtCore.pyqtSignal(float)
    speedChanged = PyQt4.QtCore.pyqtSignal(int)
    altitudeChanged = PyQt4.QtCore.pyqtSignal(float)
    temperatureChanged = PyQt4.QtCore.pyqtSignal(float)
    directionChanged = PyQt4.QtCore.pyqtSignal(int)
    coordsChanged = PyQt4.QtCore.pyqtSignal(float,float)
    idChanged = PyQt4.QtCore.pyqtSignal(int)
    stateChanged = PyQt4.QtCore.pyqtSignal(int)
    cameraStateChanged = PyQt4.QtCore.pyqtSignal(bool)
    streamingStateChanged = PyQt4.QtCore.pyqtSignal(bool)

    DISCOVERY_ID = 0xE0
    
    """The state provided by the rocket during the flight"""
    STATE = {'INITIALIZING'     : 0,
             'ON_THE_PAD'       : 1,
             'IN_FLIGHT'        : 2,
             'DROGUE_DESCENT'   : 3,
             'MAIN_DESCENT'     : 4,
             'ON_THE_GROUND'    : 5}

    NAME = {32 : "Emerillon IV",}

    """The model constructor, default value are provided if not given"""
    def __init__(self, acceleration=0, speed=0, altitude=0, temperature=0,direction=None,coords=None,ID=None,state=None, name=""):
        
        super(PyQt4.QtCore.QObject, self).__init__()

        self.__accelerationHistory = DataOverTimeHistory()
        self.__speedHistory = DataOverTimeHistory()
        self.__altitudeHistory = DataOverTimeHistory()
        self.__temperatureHistory = DataOverTimeHistory()

        self.__acceleration = acceleration
        self.__speed = speed
        self.__altitude = altitude
        self.__temperature = temperature
        self.__direction = direction
        self.__coords = coords
        self.__ID = ID
        self.__currentState = state
        self.__cameraON = False
        self.__name = name
        self.__isStreaming = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def cameraON(self):
        return self.__cameraON 
    
    @cameraON.setter
    def cameraON(self, state):
        self.__cameraON = state
        self.cameraStateChanged.emit(state)
    
    @property
    def acceleration(self):
        return self.__acceleration
    
    @acceleration.setter
    def acceleration(self, acceleration):
        self.__acceleration = acceleration
        self.accelerationChanged.emit(acceleration)
        
    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self,speed):
        self.__speed = speed
        self.speedChanged.emit(speed)
        
    @property 
    def altitude(self):
        return self.__altitude
    
    @altitude.setter
    def altitude(self,altitude):
        self.__altitude = altitude
        self.altitudeChanged.emit(altitude)
        
    @property
    def temperature(self):
        return self.__temperature
    
    @temperature.setter
    def temperature(self,temperature):
        self.__temperature = temperature
        self.temperatureChanged.emit(temperature)
        
    @property
    def direction(self):
        return self.__direction
    
    @direction.setter
    def direction(self,direction):
        self.__direction = direction
        self.directionChanged.emit(direction)
        
    @property
    def coords(self):
        return self.__coords
    
    @coords.setter
    def coords(self,coords):
        self.__coords = coords
        self.coordsChanged.emit(self.__coords['latitude'], self.__coords['longitude'])
        
    @property
    def currentState(self):
        return self.__currentState
    
    @currentState.setter
    def currentState(self, currentState):
        self.__currentState = currentState
        self.stateChanged.emit(currentState)
        
    @property
    def ID(self):
        return self.__ID
    
    @ID.setter
    def ID(self, ID):
        self.__ID = ID
        self.__name = self.NAME[ID]
        self.idChanged.emit(ID)

    @property
    def isStreaming(self):
        return self.__isStreaming

    @isStreaming.setter
    def isStreaming(self, isStreaming):
        self.__isStreaming = isStreaming
        self.streamingStateChanged.emit(isStreaming)

    @property
    def accelerationHistory(self):
        return self.__accelerationHistory

    @property
    def speedHistory(self):
        return self.__speedHistory

    @property
    def altitudeHistory(self):
        return self.__altitudeHistory

    @staticmethod
    def getInstance():
        
        if Rocket.__INSTANCE is None:
            Rocket.__INSTANCE = Rocket()
            
        return Rocket.__INSTANCE