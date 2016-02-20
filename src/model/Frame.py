from bitarray import bitarray

'''
Created on 2016-01-04

@author: rockets
'''

class Frame(object):
    
    '''Command that can be send to the rockets. Compresssed with Huffman algorithm'''
    COMMAND = {'GETTELEMETRY'   : '00000',
               'ACK'            : '00001',
               'NACK'           : '00010',
               'DISCOVER'       : '00011',
               'GETLOG'         : '00100'}
    
    '''Constant length of a frame'''
    
    
    LENGTH = 3
    
    def __init__(self,rocketID, command, payload, crc): 
        
        self.__rocketID = rocketID
        self.__command = command
        self.__data = payload
        self.__crc = crc
    
    @staticmethod
    def parseByteArray(self, byteArray):
        
        pass
    
    
    @classmethod
    def fromByteArray(cls, byteArray):
        
        args = Frame.parseByteArray(byteArray)
        frame = cls(args['rocketID'], args['command'], args['data'],
                    args['crc'])
        return frame
    
    
    @property
    def command(self):
        return self.__command
    
    @command.setter
    def command(self,command):
        self.__command = command
    
    @property
    def rocketID(self):
        return self.__rocketID
    
    @rocketID.setter
    def rocketID(self,rocketID):
        
        self.__rocketID = rocketID
        
    @property
    def dataBlocNumber(self):
        return self.__dataBlocNumber
    
    @dataBlocNumber.setter
    def dataBlocNumber(self, dataBlocNumber):
        self.__dataBlocNumber = dataBlocNumber
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data):
        self.__data = data
        
    @property
    def crc(self):
        return self.__crc
    
    @crc.setter
    def crc(self, crc):
        self.__crc = crc