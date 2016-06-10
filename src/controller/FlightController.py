from datetime import datetime


class FlightController(object):
    __INSTANCE = None

    def __init__(self):
        self.__flightModel = None
        self.__flightModels = []

    @property
    def flightModels(self):
        return self.__flightModels

    @property
    def flightModel(self):
        return self.__flightModel

    def updateStartTime(self, startTime):
        self.__flightModel.startTime = startTime

    def updateEndTime(self, endTime):
        self.__flightModel.endTime = endTime

    def updateRocket(self, rocket):
        self.__flightModel.rocket = rocket

    def updateApogee(self, apogee):
        if self.__flightModel.apogee < apogee:
            self.__flightModel.apogee = apogee

    def updateLaunchCoordinate(self, launchCoordinate):
        self.__flightModel.launchCoordinate = launchCoordinate

    def updateLandCoordinate(self, landCoordinate):
        self.__flightModel.landCoordinate = landCoordinate

    def updateTimeToApogee(self, timeToApogee):
        self.__flightModel.timeToApogee = timeToApogee

    def updateMaxSpeed(self, maxSpeed):
        if maxSpeed > self.__flightModel.maxSpeed:
            self.__flightModel.maxSpeed = maxSpeed

    def updateMaxAcceleration(self, maxAcceleration):
        if maxAcceleration > self.__flightModel.maxAcceleration:
            self.__flightModel.maxAcceleration = maxAcceleration

    def updateMaxTemperature(self, maxTemperature):
        if maxTemperature > self.__flightModel.maxTemperature:
            self.__flightModel.maxTemperature = maxTemperature

    def updateMinTemperature(self, minTemperature):
        if self.__flightModel.minTemperature is 0 or minTemperature < self.__flightModel.minTemperature:
            self.__flightModel.minTemperature = minTemperature

    def updateStateTime(self, state):
        if self.__flightModel.stateTime[state] is None:
            self.__flightModel.stateTime[state] = datetime.now()

    def withFlight(self, flight):
        self.__flightModel = flight
        self.__flightModels.append(flight)
        return self

    @staticmethod
    def getInstance():
        if FlightController.__INSTANCE is None:
            FlightController.__INSTANCE = FlightController()

        return FlightController.__INSTANCE
