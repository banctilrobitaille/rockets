from datetime import datetime


class FlightController(object):
    __INSTANCE = None

    def __init__(self):
        self.__flightModel = None
        self.__flightModels = []

    @property
    def flightsModel(self):
        return self.__flightModels

    def updateStartTime(self, startTime):
        self.__flightModel.startTime = startTime

    def updateEndTime(self, endTime):
        self.__flightModel.endTime = endTime

    def updateRocket(self, rocket):
        self.__flightModel.rocket = rocket

    def updateLaunchCoordinate(self, launchCoordinate):
        self.__flightModel.launchCoordinate = launchCoordinate

    def updateLandCoordinate(self, landCoordinate):
        self.__flightModel.landCoordinate = landCoordinate

    def updateTimeToApogee(self, timeToApogee):
        self.__flightModel.timeToApogee = timeToApogee

    def updateMaxSpeed(self, maxSpeed):
        self.__flightModel.maxSpeed = maxSpeed

    def updateMaxAcceleration(self, maxAcceleration):
        self.__flightModel.maxAcceleration = maxAcceleration

    def updateMaxTemperature(self, maxTemperature):
        self.__flightModel.maxTemperature = maxTemperature

    def updateMinTemperature(self, minTemperature):
        self.__flightModel.minTemperature = minTemperature

    def updateStateTime(self, state):
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
