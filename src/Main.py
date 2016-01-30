# -*- coding: utf-8 -*-
import PyQt4
import sys
from view import UiMainWindow
from model.Rocket import Rocket
from model.BaseStation import BaseStation
from controller.Communication import SerialController
from controller.BaseStationController import BaseStationController

"""#############################################################################
# 
# Nom du module:          MainApplication
# Auteur:                 Benoit Anctil-Robitaille, Amine Waddah
# Date:                   8 Septembre 2015
# Description:            Le module MainApplication.py initialise l'interface graphique 
#                         de lapplication et cree une instance unique de serialConnection
#                         
##############################################################################"""
class baseStationApplication(PyQt4.QtGui.QApplication):
        
    def __init__(self, args):
        
        PyQt4.QtGui.QApplication.__init__(self, args)
        
        self.__rocketModel = Rocket.getInstance()
        self.mainWindow = UiMainWindow.MainWindow(self.__rocketModel)
        self.mainWindow.show()
        self.mainWindow.iren.Initialize()
        self.exec_()
        

if __name__ == "__main__":
    
    app = baseStationApplication(sys.argv)