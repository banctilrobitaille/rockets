import struct
from ctypes import c_ushort
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
     
     
class CRC16(object):
    crc16_tab = []

    # The CRC's are computed using polynomials. Here is the most used
    # coefficient for CRC16
    crc16_constant = 0xA001  # 40961

    def __init__(self, modbus_flag=False):
        # initialize the precalculated tables
        if not len(self.crc16_tab):
            self.init_crc16()
        self.mdflag = bool(modbus_flag)

    def calculate(self, input_data=None):
        try:
            is_string = isinstance(input_data, str)
            is_bytes = isinstance(input_data, (bytes, bytearray))

            if not is_string and not is_bytes:
                raise Exception("Please provide a string or a byte sequence "
                                "as argument for calculation.")

            crc_value = 0x0000 if not self.mdflag else 0xffff

            for c in input_data:
                d = ord(c) if is_string else c
                tmp = crc_value ^ d
                rotated = crc_value >> 8
                crc_value = rotated ^ self.crc16_tab[(tmp & 0x00ff)]

            return crc_value
        except Exception as e:
            print("EXCEPTION(calculate): {}".format(e))

    def init_crc16(self):
        """The algorithm uses tables with precalculated values"""
        for i in range(0, 256):
            crc = c_ushort(i).value
            for j in range(0, 8):
                if crc & 0x0001:
                    crc = c_ushort(crc >> 1).value ^ self.crc16_constant
                else:
                    crc = c_ushort(crc >> 1).value
            self.crc16_tab.append(crc)
   
        
