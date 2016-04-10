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

        splashImage = PyQt4.QtGui.QPixmap('./Image_Files/LogoRocket.png')
        splash = PyQt4.QtGui.QSplashScreen(splashImage, PyQt4.QtCore.Qt.WindowStaysOnTopHint)
        splash.show()
        splash.showMessage("Loading modules", color=PyQt4.QtGui.QColor(255, 255, 255))

        self.mainWindow = UiMainWindow.MainWindow(BaseStationController())
        self.mainWindow.show()

        splash.showMessage("Loading VTK modules", color=PyQt4.QtGui.QColor(255, 255, 255))
        self.mainWindow.iren.Initialize()

        splash.finish(self.mainWindow)
        self.exec_()
        

if __name__ == "__main__":
    
    app = BaseStationApplication(sys.argv)