from model.Rocket import Rocket

"""#############################################################################
# 
# Nom du module:          RocketController.py
# Auteur:                 Benoit Anctil-Robitaille
# Date:                   5 janvier 2016
# Description:            Le module RocketController.py inclus les classes et methodes
#                         permettant de mettre a jour le model Rocket, les donnees de
#                         vol de la fusee
#
##############################################################################"""


"""#
# La classe RocketController
# Description:    Classe permettant de mettre a jour le model Rocket, les donnees de
#                 vol de la fusee
#
#"""

class RocketController(object):
    

    def __init__(self, rocketModel):
        
        self.__rocketModel = rocketModel
  
  
    """
    #    Methode updateRocketData
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour toutes les donnees de la fusee pendant
    #                 le vol. Cette methode appelle des methodes specifiques
    #                 pour mettre a jour les donnees de vol de la fusee
    #
    #    param:       speed, la vitesse de la fusee en mph
    #                 altitude, laltitude de la fusee en pieds
    #                 acceleration, lacceleration de la fusee en g
    #                 temperature, la temperature interne de la fusee en C
    #                 direction, la direction de la fusee 'N', 'S', 'E', 'W'
    #                 coords, les coordonnees de la fusee, coords['longitude'], coords['latitude']
    #                 ID, l'ID unique de la fusee
    #                 state, l'etat de la fusee
    #    return: None
    """ 
    def updateRocketData(self,speed, altitude, acceleration, temperature, direction, coords, ID, state ):
        
        self.updateRocketSpeed(speed)
        self.updateRocketAltitude(altitude)
        self.updateRocketAcceleration(acceleration)
        self.updateRocketTemperature(temperature)
        self.updateRocketDirection(direction)
        self.updateRocketCoords(coords)
        self.updateRocketID(ID)
        self.updateRocketState(state)
   
        
    """
    #    Methode updateRocketSpeed
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour la vitesse de la fusee
    #
    #    param:       speed, la vitesse de la fusee en mph
    #    return: None
    """ 
    def updateRocketSpeed(self,speed):
        
        self.__rocketModel.speed = speed
    
    """
    #    Methode updateRocketAltitude
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour laltitude de la fusee
    #
    #    param:       altitude, laltitude en pieds
    #    return: None
    """ 
    def updateRocketAltitude(self,altitude):
        
        self.__rocketModel.altitude = altitude
    
    """
    #    Methode updateRocketAcceleration
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour lacceleration de la fusee
    #
    #    param:       acceleration, lacceleration de la fusee en G
    #    return: None
    """ 
    def updateRocketAcceleration(self,acceleration):
        
        self.__rocketModel.acceleration = acceleration
    
    
    """
    #    Methode updateRocketTemperature
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour la temperature de la fusee
    #
    #    param:       temperature, la temperature interne en Celcius
    #    return: None
    """ 
    def updateRocketTemperature(self,temperature):
        
        self.__rocketModel.temperature = temperature
    
    """
    #    Methode updateRocketDirection
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour la direction de la fusee
    #
    #    param:       direction, la direction 'N', 'E', 'W'
    #    return: None
    """ 
    def updateRocketDirection(self,direction):
        
        self.__rocketModel.direction = direction
    
    """
    #    Methode updateRocketCoords
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour les coordonnees GPS de la fusee
    #
    #    param:       coords, dict ['longitude'], ['latitude']
    #    return: None
    """ 
    def updateRocketCoords(self,coords):
        
        self.__rocketModel.coords = coords
    
    """
    #    Methode updateRocketID
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour lidentifiant de la fusee
    #
    #    param:       ID, identifiant de la fusee
    #    return: None
    """ 
    def updateRocketID(self, ID):
        
        self.__rocketModel.ID = ID
    
    
    """
    #    Methode updateRocketState
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour letat de la fusee
    #
    #    param:       state, etat de la fusee
    #    return: None
    """ 
    def updateRocketState(self,state):
        
        self.__rocketModel.currentState = state
    