"""#############################################################################
# 
# Nom du module:          Rocket
# Auteur:                 Benoit Anctil-Robitaille
# Date:                   5 janvier 2016
# Description:            Le module Rocket.py inclus les classes et méthodes
#                         permettant d'affecter ou lire les différents états
#                         de la fusée en vol.
#
##############################################################################"""


"""#
# La classe Rocket
# Description:    Classe representant la fusée en vol. Cette classe fournie
#                 l'interface nécessaire à l'affectation et lecture des 
#                 données de la fusée.
#"""
class Rocket(object):
    
    
    """The state provided by the rocket during the flight"""
    STATE = {'INITIALIZING'     : 0,
             'ON_THE_PAD'       : 1,
             'IN_FLIGHT'        : 2,
             'DROGUE_DESCENT'   : 3,
             'MAIN_DESCENT'     : 4,
             'ON_THE_GROUND'    : 5}
    
    
    """The model constructor, default value are provided if not given"""
    def __init__(self, acceleration=0, speed=0, altitude=0, temperature=0,direction=None,coords=None,id=None,state=None):
        
        self.__acceleration = acceleration
        self.__speed = speed
        self.__altitude = altitude
        self.__temperature = temperature
        self.__direction = direction
        self.__coords = coords
        self.__ID = id
        self.__currentState = state
        
    
    @property
    def acceleration(self):
        return self.__acceleration
    
    @acceleration.setter
    def acceleration(self, acceleration):
        self.__acceleration = acceleration
        
    @property
    def speed(self):
        return self.__speed
    
    @speed.setter
    def speed(self,speed):
        self.__speed = speed
        
    @property 
    def altitude(self):
        return self.__altitude
    
    @altitude.setter
    def altitude(self,altitude):
        self.__altitude = altitude
        
    @property
    def temperature(self):
        return self.__temperature
    
    @temperature.setter
    def temperature(self,temperature):
        self.__temperature = temperature
        
    @property
    def direction(self):
        return self.__direction
    
    @direction.setter
    def direction(self,direction):
        self.__direction = direction
        
    @property
    def coords(self):
        return self.__coords
    
    @coords.setter
    def coords(self,*coords):
        self.__coords = coords
    
    @property
    def currentState(self):
        return self.__currentState
    
    @currentState.setter
    def currentState(self, currentState):
        self.__currentState = currentState
        
    @property
    def ID(self):
        return self.__ID
    
    @ID.setter
    def ID(self, ID):
        self.__ID = ID