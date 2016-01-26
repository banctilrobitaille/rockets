from bitarray import bitarray

'''
Created on 2016-01-04

@author: rockets
'''

class Frame(object):
    
    COMMAND = {'GETTELEMETRY' : bitarray('0'), 'ACK' : bitarray('10'), 'NACK' : bitarray('110'),
               'DISCOVER' : bitarray('1110'), 'GETLOG' : bitarray('1111')}
    
    LENGTH = 100
    
    #def __init__(self, rocketID, length, cmd, data, crc):
    def __init__(self,*arg,**kwarg): 
      
      pass
    
    @property
    def rocketID(self):
        return self.__rocketID
    
    @rocketID.setter
    def rocketID(self,rocketID):
        pass