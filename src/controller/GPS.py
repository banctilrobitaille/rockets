import PyQt4
import time
import re
from PyQt4.Qt import pyqtSlot


class GPSDevice(PyQt4.QtCore.QThread):

    coordsReceived = PyQt4.QtCore.pyqtSignal(float, float)
    fixChanged = PyQt4.QtCore.pyqtSignal(str)
    fixTimeChanged = PyQt4.QtCore.pyqtSignal(str)
    altitudeReceived = PyQt4.QtCore.pyqtSignal(float)
    nbSatellitesChanged = PyQt4.QtCore.pyqtSignal(int)

    def __init__(self):
        super(GPSDevice, self).__init__()
        self.__isConnected = False
        self.__fix = ""
        self.__fixTime = ""
        self.__nbSatellite = 0

    @property
    def isConnected(self):
        return self.__isConnected

    @isConnected.setter
    def isConnected(self, value):
        self.__isConnected = value

    @property
    def fixTime(self):
        return self.__fixTime

    @fixTime.setter
    def fixTime(self, fixTime):
        self.__fixTime = fixTime
        self.fixTimeChanged.emit(self.__fixTime)

    @property
    def fix(self):
        return self.__fix

    @fix.setter
    def fix(self, fix):
        self.__fix = fix
        self.fixChanged.emit(self.__fix)

    @property
    def nbSatellite(self):
        return self.__nbSatellite

    @nbSatellite.setter
    def nbSatellite(self, nbSatellite):
        self.__nbSatellite = nbSatellite
        self.nbSatellitesChanged.emit(self.__nbSatellite)

    def connect(self):

        raise NotImplementedError

    def disconnect(self):

        raise NotImplementedError


class GlobalSat(GPSDevice):

    def __init__(self, serialController):
        super(GlobalSat, self).__init__()
        self.__serialController = serialController

    def connect(self):
        try:
            self.__serialController.serialConnection.open()
            self.__serialController.updateSerialConnectionState(True)
            self.__isConnected = True
            self.start()

        except Exception as e:

            print e.message

    def disconnect(self):

        try:
            self.__serialController.serialConnection.close()
            self.__serialController.updateSerialConnectionState(False)
            self.__isConnected = False

        except Exception as e:

            print e.message

    def run(self):

        while self.__isConnected:

            if self.__serialController.serialConnection.inWaiting() > 0:

                receivedData = self.__serialController.serialConnection.readline()
                print receivedData

                if NMEASentenceFactory.SENTENCE_TYPE["GPGGA"] in receivedData:

                    try:
                        sentence = NMEASentenceFactory.create(NMEASentenceFactory.SENTENCE_TYPE["GPGGA"],receivedData)
                        self.altitudeReceived.emit(sentence.altitude)
                        self.coordsReceived.emit(sentence.latitude, sentence.longitude)

                        if sentence.fix != self.fix:
                            self.fix = sentence.fix

                        if sentence.nbSatellite != self.nbSatellite:
                            self.nbSatellite = sentence.nbSatellite

                        if sentence.fixTime != self.fixTime:
                            self.fixTime = sentence.fixTime

                        print "yess"
                    except Exception as e:

                        print "NOP"


class NMEASentenceFactory(PyQt4.QtCore.QObject):

    SENTENCE_TYPE = {
        "GPGGA": "GPGGA",
        "GPGSA": "GPGSA",
        "GPGSV": "GPGSV",
        "GPMRC": "GPMRC",
    }

    def __init__(self):
        super(NMEASentenceFactory, self)
        pass

    @staticmethod
    def create(sentenceType, sentenceData):

        NMEASentence = None

        if sentenceType is NMEASentenceFactory.SENTENCE_TYPE['GPGGA']:

            NMEASentence = GPGGASentence(sentenceData)

        return NMEASentence


class NMEASentence(PyQt4.QtCore.QObject):

    def __init__(self):
        super(NMEASentence, self).__init__()
        self.__identifier = ""

    @property
    def identifier(self):
        return self.__identifier

    @identifier.setter
    def identifier(self, identifier):
        self.__identifier = identifier


class GPGGASentence(NMEASentence):

    FIX = {
        0: "INVALID FIX",
        1: "GPS FIX",
        2: "DGPS FIX",
    }

    def __init__(self, sentenceData):
        super(GPGGASentence, self).__init__()

        try:
            sentenceElements = sentenceData.split(",")
            self.identifier     = sentenceElements[0]
            self.__fixTime      = sentenceElements[1]
            self.__latitude     = (float(sentenceElements[2])/100.0)
            self.__longitude    = -(float(sentenceElements[4])/100.0)
            self.__fix          = int(sentenceElements[6])
            self.__nbSatellite  = int(sentenceElements[7])
            self.__altitude     = float(sentenceElements[9])

        except Exception as e:

            print e.message


    @property
    def fixTime(self):
        return self.__fixTime

    @fixTime.setter
    def fixTime(self, fixTime):
        self.__fixTime = fixTime

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
    def fix(self):
        return GPGGASentence.FIX[self.__fix]

    @fix.setter
    def fix(self, fix):
        self.__fix = fix

    @property
    def nbSatellite(self):
        return self.__nbSatellite

    @nbSatellite.setter
    def nbSatellite(self, nbSatellite):
        self.__nbSatellite = nbSatellite

    @property
    def altitude(self):
        return self.__altitude

    @altitude.setter
    def altitude(self, altitude):
        self.__altitude = altitude