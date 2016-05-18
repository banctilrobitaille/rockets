import PyQt4
from datetime import datetime


class DataOverTimeHistory(PyQt4.QtCore.QObject):

    def __init__(self):
        super(DataOverTimeHistory, self).__init__()
        self.__referenceTimeStamp = None
        self.__max = 0
        self.__min = 0
        self.__average = 0
        self.__nbData = 0
        self.__time = []
        self.__value = []

    @property
    def max(self):
        return self.__max

    @max.setter
    def max(self, value):
        self.__max = value

    @property
    def min(self):
        return self.__min

    @min.setter
    def min(self, value):
        self.__min = value

    @property
    def average(self):
        return self.__average

    @average.setter
    def average(self, value):
        self.__average = value

    @property
    def nbData(self):
        return self.__nbData

    def addData(self, timestamp, value):

        if self.__referenceTimeStamp is None:
            self.__referenceTimeStamp = timestamp

        self.__time.append(float((datetime.now() - self.__referenceTimeStamp).seconds))
        self.__value.append(value)
        self.__nbData += 1

        if value > self.__max:
            self.__max = value
        elif value < self.__min:
            self.__min = value

        self.__average = (sum(self.__value)/self.__nbData)

    def isEmpty(self):

        return len(self.__xData) is 0 and len(self.__yData) is 0

    def clear(self):

        self.__max = 0
        self.__min = 0
        self.__average = 0
        self.__nbData = 0
        self.__time = []
        self.__value = []



