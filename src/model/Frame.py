from bitarray import bitarray

'''
Created on 2016-01-04

@author: rockets
'''

class Frame(object):
    
    '''Command that can be send to the rockets. Compresssed with Huffman algorithm'''
    COMMAND = {'GETTELEMETRY'   : bitarray('0'),
               'ACK'            : bitarray('10'),
               'NACK'           : bitarray('110'),
               'DISCOVER'       : bitarray('1110'),
               'GETLOG'         : bitarray('1111')}
    
    '''Constant length of a frame'''
    LENGTH = 100
    
    def __init__(self, byteArray): 

        pass
    
    @property
    def rocketID(self):
        return self.__rocketID
    
    @rocketID.setter
    def rocketID(self,rocketID):
        pass