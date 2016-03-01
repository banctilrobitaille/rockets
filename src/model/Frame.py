import struct
'''
Created on 2016-01-04

@author: rockets
'''

class Frame(object):

    
    RECEIVED_FRAME_LENGTH = 39
    TRANSMIT_FRAME_LENGTH = 10
    FLAG = 'a'
    
    def __init__(self,rocketID, command,data,crc): 
        
        self.__rocketID     = rocketID
        self.__command      = command
        self.__data         = data
        self.__crc          = crc
    
    @staticmethod
    def parseByteArray(byteArray):
        
        rocketData = {}
        
        rocketData['ROCKETID']      = struct.unpack_from("c",byteArray[0])[0]
        rocketData['COMMAND']       = struct.unpack_from("c",byteArray[0])[0]
        rocketData['TIMESTAMP']     = struct.unpack_from("f",byteArray[3:7])[0]
        rocketData['STATE']         = struct.unpack_from("c",byteArray[7])[0]
        rocketData['GPSFIX']        = struct.unpack_from("c",byteArray[11:15])
        rocketData['SPEED']         = struct.unpack_from("f",byteArray[11:15])[0]
        rocketData['ALTITUDE']      = struct.unpack_from("f",byteArray[15:19])[0]
        rocketData['ACCELERATION']  = struct.unpack_from("f",byteArray[19:23])[0]
        rocketData['LATITUDE']      = struct.unpack_from("f",byteArray[23:27])[0]
        rocketData['LONGITUDE']     = struct.unpack_from("f",byteArray[27:31])[0]
        rocketData['TEMPERATURE']   = struct.unpack_from("f",byteArray[31:35])[0]
        rocketData['CRC']           = struct.unpack_from("c",byteArray[35])[0]
        
        return rocketData
    
    @classmethod
    def fromByteArray(cls, byteArray):
        
        rocketData = Frame.parseByteArray(byteArray)
        frame = cls(rocketData['ROCKETID'],rocketData['COMMAND'], rocketData, rocketData['CRC'])
        
        return frame
    
    
    @property
    def rocketID(self):
        return self.__rocketID
    
    @rocketID.setter
    def rocketID(self,rocketID):
        
        self.__rocketID = rocketID
    
    @property
    def command(self):
        return self.__command
    
    @command.setter
    def command(self,command):
        self.__command = command
    
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