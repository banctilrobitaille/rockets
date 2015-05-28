# -*- coding: utf-8 -*-
import PyQt4
import UiMainWindow
from serialIO import  SerialConnection



class baseStationApplication(PyQt4.QtGui.QApplication):
        
    def __init__(self, args):
        
        PyQt4.QtGui.QApplication.__init__(self, args)
        self.serialConnection = SerialConnection()
        self.mainWindow = UiMainWindow.MainWindow(self.serialConnection)
        self.mainWindow.show()
        self.exec_()
        

