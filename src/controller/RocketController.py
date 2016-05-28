from model.Rocket import Rocket
from datetime import datetime
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
    

    __INSTANCE = None

    def __init__(self):
        
        self.__rocketModel = Rocket()
  

    @property
    def rocket(self):
        return self.__rocketModel

    @rocket.setter
    def rocket(self, rocket):
        self.__rocketModel = rocket


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
   

    def updateRocketCameraState(self):

        if self.__rocketModel.cameraON:

            self.__rocketModel.cameraON = False
        else:
            self.__rocketModel.cameraON = True

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


    def updateRocketSpeedFromAltitude(self, altitude):

        if not self.__rocketModel.altitudeHistory.isEmpty():
            try:
                lastAltitude = self.__rocketModel.altitudeHistory.getLastValue()

                da = abs(altitude - lastAltitude["VALUE"])
                dt = float((datetime.now() - lastAltitude["TIMESTAMP"]).seconds)

                self.__rocketModel.speed = da/dt
                self.__rocketModel.speedHistory.addData(datetime.now(), self.__rocketModel.speed)
            except Exception as ex:

                print(ex.message)

    """
    #    Methode updateRocketAltitude
    #    Description: Methode du controlleur permettant de mettre a
    #                 jour laltitude de la fusee
    #
    #    param:       altitude, laltitude en pieds
    #    return: None
    """ 
    def updateRocketAltitude(self, altitude):
        
        self.__rocketModel.altitude = altitude
        self.__rocketModel.altitudeHistory.addData(datetime.now(), altitude)
    
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
    

    def updateRocketAccelerationFromSpeed(self):

        if not self.__rocketModel.speedHistory.isEmpty():
            try:
                dv = (self.__rocketModel.speedHistory.getDataAtIndex(-1)["VALUE"] -
                      self.__rocketModel.speedHistory.getDataAtIndex(-2)["VALUE"])

                dt = float((self.__rocketModel.speedHistory.getDataAtIndex(-1)["TIMESTAMP"] -
                            self.__rocketModel.speedHistory.getDataAtIndex(-2)["TIMESTAMP"]).seconds)

                self.__rocketModel.acceleration = dv/dt

            except Exception as ex:

                print(ex.message)

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


    @staticmethod
    def getInstance():

        if RocketController.__INSTANCE is None:
            RocketController.__INSTANCE = RocketController()

        return RocketController.__INSTANCE