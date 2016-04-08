import struct
from src.controller.CommunicationUtility import CRC16
from ctypes import c_ushort
'''
Created on 2016-01-04

@author: rockets
'''


class Frame(object):

    FLAG = "a"
    CRC_CALCULATOR = CRC16()

    def __init__(self, rocketID, command, timestamp, crc):

        self.__rocketID = rocketID
        self.__command = command
        self.__timestamp = timestamp
        self.__crc = crc

    def toByteArray(self, withCRC=False):

        raise NotImplementedError

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

    def isValid(self):

        raise NotImplementedError


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
        frame['CRC']           = struct.unpack_from("H",byteArray[35:37])[0]

        return frame
    
    @classmethod
    def fromByteArray(cls, byteArray):
        
        frameDict = ReceivedFrame.parseByteArray(byteArray)
        frame = cls(frameDict['ROCKETID'], frameDict['COMMAND'], frameDict['TIMESTAMP'],
                    frameDict['STATE'], frameDict['GPSFIX'], frameDict['SPEED'],
                    frameDict['ALTITUDE'], frameDict['ACCELERATION'], frameDict['LATITUDE'],
                    frameDict['LONGITUDE'], frameDict['TEMPERATURE'], frameDict['CRC'])
        
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

    def isValid(self):

        return Frame.CRC_CALCULATOR.calculate(self.toByteArray()) == self.crc

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
        self.crc = Frame.CRC_CALCULATOR.calculate(self.toByteArray())

    def toByteArray(self, withCRC=False):

        byteData = ""
        byteData += struct.pack('B', self.rocketID | self.command)
        byteData += struct.pack('i', self.timestamp)
        byteData += struct.pack('f', self.__payload)

        if withCRC and self.crc is not None:
            byteData += struct.pack('H', self.crc)

        return byteData

    def isValid(self):

        return True

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, payload):
        self.__payload = payload
