import struct
from ctypes import c_ushort
'''
Created on 2016-01-04

@author: rockets
'''


class Frame(object):

    FLAG = "a"

    def __init__(self, rocketID, command, timestamp, crc):

        self.__crcCalculator = CRC16()
        self.__rocketID = rocketID
        self.__command = command
        self.__timestamp = timestamp
        self.__crc = crc

    def toByteArray(self, withCRC=False):

        raise NotImplementedError

    @property
    def crcCalculator(self):
        return self.__crcCalculator

    @property
    def rocketID(self):
        return self.__rocketID

    @rocketID.setter
    def rocketID(self, rocketID):

        self.__rocketID = rocketID

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, command):
        self.__command = command

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self.__timestamp = timestamp

    @property
    def crc(self):
        return self.__crc

    @crc.setter
    def crc(self, crc):
        self.__crc = crc


class ReceivedFrame(Frame):

    LENGTH = 39

    def __init__(self,rocketID, command, timestamp, state, gpsFix, speed, altitude,
                 acceleration, latitude, longitude, temperature, crc):
        
        Frame.__init__(self, rocketID, command, timestamp, crc)
        self.__state = state
        self.__gpsFix = gpsFix
        self.__speed = speed
        self.__altitude = altitude
        self.__acceleration = acceleration
        self.__latitude = latitude
        self.__longitude = longitude
        self.__temperature = temperature
    
    @staticmethod
    def parseByteArray(byteArray):
        
        frame = {}

        frame['ROCKETID']      = struct.unpack_from("c",byteArray[0])[0]
        frame['COMMAND']       = struct.unpack_from("c",byteArray[0])[0]
        frame['TIMESTAMP']     = struct.unpack_from("f",byteArray[3:7])[0]
        frame['STATE']         = struct.unpack_from("c",byteArray[7])[0]
        frame['GPSFIX']        = struct.unpack_from("c",byteArray[11:15])
        frame['SPEED']         = struct.unpack_from("f",byteArray[11:15])[0]
        frame['ALTITUDE']      = struct.unpack_from("f",byteArray[15:19])[0]
        frame['ACCELERATION']  = struct.unpack_from("f",byteArray[19:23])[0]
        frame['LATITUDE']      = struct.unpack_from("f",byteArray[23:27])[0]
        frame['LONGITUDE']     = struct.unpack_from("f",byteArray[27:31])[0]
        frame['TEMPERATURE']   = struct.unpack_from("f",byteArray[31:35])[0]
        frame['CRC']           = struct.unpack_from("H",byteArray[35:36])[0]

        return frame
    
    @classmethod
    def fromByteArray(cls, byteArray):
        
        frameDict = ReceivedFrame.parseByteArray(byteArray)
        frame = cls(frameDict['ROCKETID'], frameDict['COMMAND'], frameDict['TIMESTAMP'],
                    frameDict['STATE'], frameDict['GPSFIX'], frameDict['SPEED'],
                    frameDict['ALTITUDE'], frameDict['ACCELERATION'], frameDict['LATITUDE'],
                    frameDict['LONGITUDE'], frameDict['TEMPERATURE'],frameDict['CRC'])
        
        return frame

    #Override
    def toByteArray(self, withCRC=False):

        dataByte = ""
        dataByte   += struct.pack("c", self.rocketID)
        dataByte   += struct.pack("c", self.command)
        dataByte   += struct.pack("f", self.timestamp)
        dataByte   += struct.pack("c", self.__state)
        dataByte   += struct.pack("c", self.__gpsFix)
        dataByte   += struct.pack("f", self.__speed)
        dataByte   += struct.pack("f", self.__altitude)
        dataByte   += struct.pack("f", self.__acceleration)
        dataByte   += struct.pack("f", self.__latitude)
        dataByte   += struct.pack("f", self.__longitude)
        dataByte   += struct.pack("f", self.__temperature)

        if withCRC:
            dataByte += struct.pack("H", self.crc)

        return dataByte

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def gpsFix(self):
        return self.__gpsFix

    @gpsFix.setter
    def gpsFix(self, gpsFix):
        self.__gpsFix = gpsFix

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self,speed):
        self.__speed = speed

    @property
    def altitude(self):
        return self.__altitude

    @altitude.setter
    def altitude(self,altitude):
        self.__altitude = altitude

    @property
    def acceleration(self):
        return self.__acceleration

    @acceleration.setter
    def acceleration(self, acceleration):
        self.__acceleration = acceleration

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude):
        self.__latitude = latitude

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, longitude):
        self.__longitude = longitude

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self,temperature):
        self.__temperature = temperature


class SentFrame(Frame):

    LENGTH = 10

    def __init__(self, rocketID, command, timestamp, payload):
        Frame.__init__(self, rocketID, command, timestamp, None)

        self.__payload = payload
        #self.crc = self.crcCalculator.calculate(self.toByteArray())

    def toByteArray(self, withCRC=False):

        byteData = ""
        byteData += struct.pack('B', self.rocketID | self.command)
        byteData += struct.pack('f', self.timestamp)
        byteData += struct.pack('f', self.__payload)

        if withCRC and self.crc is not None:
            byteData += struct.pack('H', self.crc)

        return byteData

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, payload):
        self.__payload = payload


class CRC16(object):
    crc16_tab = []

    # The CRC's are computed using polynomials. Here is the most used
    # coefficient for CRC16
    crc16_constant = 0x8005
    #crc16_constant = 0xA001

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
                tmp = (crc_value ^ (d & 0x00ff))
                rotated = crc_value >> 8
                crc_value = rotated ^ self.crc16_tab[(tmp & 0xff)]

            return crc_value
        except Exception as e:
            print("EXCEPTION(calculate): {}".format(e))

    def init_crc16(self):
        """The algorithm uses tables with precalculated values"""
        for i in range(0, 256):

            crc = 0
            c = c_ushort(i).value

            for j in range(0, 8):

                if (crc ^ c) & 0x0001:

                    crc = c_ushort(crc >> 1).value ^ self.crc16_constant

                else:

                    crc = c_ushort(crc >> 1).value

                c = c_ushort(c >> 1).value

            self.crc16_tab.append(crc)