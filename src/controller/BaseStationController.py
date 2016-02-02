'''
Created on 2016-01-28

@author: rockets
'''

class BaseStationController(object):
    
    __INSTANCE = None
    
    
    def __init__(self, params):
        
        pass
    
    
    @staticmethod
    def getInstance():
        
        if BaseStationController.__INSTANCE is None:
            BaseStationController.__INSTANCE = BaseStationController()
            
        return BaseStationController.__INSTANCE