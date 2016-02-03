import PyQt4

'''
Created on 2016-01-04

@author: rockets
'''


class BaseStation(PyQt4.QtCore.QObject):

    
    """
    Comments TODO
    """
    coordsChanged = PyQt4.QtCore.pyqtSignal(float, float)
    temperatureChanged = PyQt4.QtCore.pyqtSignal(float)
    
    
    def __init__(self, temperature=0, coords=None):
    
        super(PyQt4.QtCore.QObject, self).__init__()
        self.__temperature = temperature
        self.__coords = coords
    
    
    @property
    def temperature(self):
        
        return self.__temperature
    
    @temperature.setter
    def temperature(self,temperature):
        
        self.__temperature = temperature
        
    @property
    def coords(self):
        
        return self.__coords
    
    @coords.setter
    def coords(self,**coords):
        
        self.__coords['longitude'] = coords['longitude']
        self.__coords['latitude'] = coords['latitude']