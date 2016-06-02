import PyQt4


class Flight(PyQt4.QtCore.QObject):
    def __init__(self):
        super(Flight, self).__init__()
        self.__startTime = None
        self.__endTime = None
        self.__rocket = None
        self.__launchCoordinate = None
        self.__landCoordinate = None
        self.__timeToApogee = None
        self.__apogee = None
        self.__maxSpeed = None
        self.__maxAcceleration = None
        self.__maxTemperature = None
        self.__minTemperature = None

    @property
    def startTime(self):
        return self.__startTime

    @startTime.setter
    def startTime(self, startTime):
        self.__startTime = startTime

    @property
    def endTime(self):
        return self.__endTime

    @endTime.setter
    def endTime(self, endTime):
        self.__endTime = endTime

    @property
    def rocket(self):
        return self.__rocket

    @rocket.setter
    def rocket(self, rocket):
        self.__rocket = rocket

    @property
    def launchCoordinate(self):
        return self.__launchCoordinate

    @launchCoordinate.setter
    def launchCoordinate(self, launchCoordinate):
        self.__launchCoordinate = launchCoordinate

    @property
    def landCoordinate(self):
        return self.__landCoordinate

    @landCoordinate.setter
    def landCoordinate(self, landCoordinate):
        self.__landCoordinate = landCoordinate

    @property
    def timeToApogee(self):
        return self.__timeToApogee

    @timeToApogee.setter
    def timeToApogee(self, timeToApogee):
        self.__timeToApogee = timeToApogee

    @property
    def apogee(self):
        return self.__apogee

    @apogee.setter
    def apogee(self, apogee):
        self.__apogee = apogee

    @property
    def maxSpeed(self):
        return self.__maxSpeed

    @maxSpeed.setter
    def maxSpeed(self, maxSpeed):
        self.__maxSpeed = maxSpeed

    @property
    def maxAcceleration(self):
        return self.__maxAcceleration

    @maxAcceleration.setter
    def maxAcceleration(self, maxAcceleration):
        self.__maxAcceleration = maxAcceleration

    @property
    def maxTemperature(self):
        return self.__maxTemperature

    @maxTemperature.setter
    def maxTemperature(self, maxTemperature):
        self.__maxTemperature = maxTemperature

    @property
    def minTemperature(self):
        return self.__minTemperature

    @minTemperature.setter
    def minTemperature(self, minTemperature):
        self.__minTemperature = minTemperature
