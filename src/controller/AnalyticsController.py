import PyQt4
from model.Analytics import CommunicationAnalytics


class CommunicationAnalyticsController(PyQt4.QtCore.QObject):
    __INSTANCE = None

    def __init__(self):
        super(CommunicationAnalyticsController, self).__init__()
        self.__communicationAnalyticsModel = CommunicationAnalytics.getInstance()

        self.__nbOfFrameSent = 0
        self.__nbOfFrameReceived = 0
        self.__nbOfBadFrameReceived = 0
        self.__nbOfBadFrameSent = 0
        self.__averageNbOfRetries = 0

    def incrementNbOfFrameSent(self):
        self.__communicationAnalyticsModel.nbOfFrameSent += 1

    def incrementNbOfFrameReceived(self):
        self.__communicationAnalyticsModel.nbOfFrameReceived += 1

    def incrementNbOfBadFrameReceived(self):
        self.__communicationAnalyticsModel.nbOfBadFrameReceived += 1

    def incrementNbOfBadFrameSent(self):
        self.__communicationAnalyticsModel.nbOfBadFrameSent += 1

    def incrementNbOfRetries(self):
        self.__communicationAnalyticsModel.nbOfRetries += 1

    def incrementNbOfFrameLost(self):
        self.__communicationAnalyticsModel.nbOfFrameLost += 1

    def updateAverageNbOfRetries(self):
        self.__communicationAnalyticsModel.averageNbOfRetries = (
            self.__communicationAnalyticsModel.nbOfRetries / self.__communicationAnalyticsModel.nbOfRetries)

    @staticmethod
    def getInstance():
        if CommunicationAnalyticsController.__INSTANCE is None:
            CommunicationAnalyticsController.__INSTANCE = CommunicationAnalyticsController()

        return CommunicationAnalyticsController.__INSTANCE
