# -*- coding: utf-8 -*-
import PyQt4
import sys
from view import UiMainWindow
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
class BaseStationApplication(PyQt4.QtGui.QApplication):
        
    def __init__(self, args):
        
        PyQt4.QtGui.QApplication.__init__(self, args)

        self.mainWindow = UiMainWindow.MainWindow(BaseStationController())
        self.mainWindow.show()
        self.mainWindow.iren.Initialize()
        self.exec_()
        

if __name__ == "__main__":
    
    app = BaseStationApplication(sys.argv)