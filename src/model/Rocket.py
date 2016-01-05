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
    
    state = {'INITIALIZING' : 0, 'ON_THE_PAD' : 1, 'IN_FLIGHT' : 2,
              'DROGUE_DESCENT' : 3, 'MAIN_DESCENT' : 4, 'ON_THE_GROUND' : 5}
    
    def __init__(self):
        
        self.acceleration = 0
        self.speed = 0
        self.altitude = 0
        self.temperature = 0
        self.direction = ""
        self.coords = [0.0,0.0]
        self.currentState = self.state['INITIALIZING']
        
    
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