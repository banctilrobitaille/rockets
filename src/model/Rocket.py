import PyQt4
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
    stateChanged = PyQt4.QtCore.pyqtSignal(str)

    DISCOVERY_ID = 0xF0
    
    """The state provided by the rocket during the flight"""
    STATE = {'INITIALIZING'     : 0,
             'ON_THE_PAD'       : 1,
             'IN_FLIGHT'        : 2,
             'DROGUE_DESCENT'   : 3,
             'MAIN_DESCENT'     : 4,
             'ON_THE_GROUND'    : 5}


    """The model constructor, default value are provided if not given"""
    def __init__(self, acceleration=0, speed=0, altitude=0, temperature=0,direction=None,coords=None,ID=None,state=None, name=""):
        
        super(PyQt4.QtCore.QObject, self).__init__()
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
        self.coordsChanged(self.__coords['longitude'], self.__coords['latitude'])
        
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
        self.idChanged.emit(ID)
        
    @staticmethod
    def getInstance():
        
        if Rocket.__INSTANCE is None:
            Rocket.__INSTANCE = Rocket()
            
        return Rocket.__INSTANCE