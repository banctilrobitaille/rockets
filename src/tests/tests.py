'''
Created on 2016-02-02

@author: rockets
'''
import unittest
from model.Rocket import Rocket
from controller.RocketController import RocketController


class Test(unittest.TestCase):


    def setUp(self):
        
        self.__rocketModel = Rocket.getInstance()
        self.__rocketController = RocketController(self.__rocketModel)

    def tearDown(self):
        pass


    def testSpeedUpdate(self):
        
        for speed in range(0,300, 50):
            
            self.__rocketController.updateRocketSpeed(speed)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testViewUpdate']
    unittest.main()