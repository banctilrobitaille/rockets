from model.Rocket import Rocket
'''
Created on 2016-01-26

@author: rockets
'''

class RocketController(object):
    

    def __init__(self, rocketModel):
        
        self.__rocketModel = Rocket()
  
  
    def updateRocketData(self,speed, altitude, acceleration, temperature, direction, coords, ID, state ):
        
        self.updateRocketSpeed(speed)
        self.updateRocketAltitude(altitude)
        self.updateRocketAcceleration(acceleration)
        self.updateRocketTemperature(temperature)
        self.updateRocketDirection(direction)
        self.updateRocketCoords(coords)
        self.updateRocketID(ID)
        self.updateRocketState(state)
        
    
    def updateRocketSpeed(self,speed):
        
        self.__rocketModel.speed(speed)
    
    
    def updateRocketAltitude(self,altitude):
        
        self.__rocketModel.altitude(altitude)
    
    
    def updateRocketAcceleration(self,acceleration):
        
        self.__rocketModel.acceleration(acceleration)
    
    
    def updateRocketTemperature(self,temperature):
        
        self.__rocketModel.temperature(temperature)
    
    def updateRocketDirection(self,direction):
        
        self.__rocketModel.direction(direction)
    
    def updateRocketCoords(self,coords):
        
        self.__rocketModel.coords(coords)
    
    def updateRocketID(self, ID):
        
        self.__rocketModel.ID(ID)
    
    def updateRocketState(self,state):
        
        self.__rocketModel.currentState(state)
    