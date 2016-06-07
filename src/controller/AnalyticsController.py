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

    def incrementNbOfRetries(self, datetime):
        if self.__communicationAnalyticsModel.firstRetryTimeReference is None:
            self.__communicationAnalyticsModel.firstRetryTimeReference = datetime

            self.__communicationAnalyticsModel.retryHistory['Time'].append(datetime)
            self.__communicationAnalyticsModel.retryHistory['Retry'][-1] += 1

        elif float((datetime - self.__communicationAnalyticsModel.retryHistory['Time'][-1]).seconds) > 10:
            self.__communicationAnalyticsModel.retryHistory['Time'].append(datetime)
            self.__communicationAnalyticsModel.retryHistory['Retry'].append(1)
        else:
            self.__communicationAnalyticsModel.retryHistory['Retry'][-1] += 1

        self.__communicationAnalyticsModel.nbOfRetries += 1
        self.updateAverageNbOfRetries()

    def incrementNbOfFrameLost(self):
        self.__communicationAnalyticsModel.nbOfFrameLost += 1

    def incrementNbOfCommandSent(self, commandSent):
        if commandSent in self.__communicationAnalyticsModel.commandSentDict:
            self.__communicationAnalyticsModel.commandSentDict[commandSent] += 1
        else:
            self.__communicationAnalyticsModel.commandSentDict[commandSent] = 1

        self.__communicationAnalyticsModel.nbOfCommandSent += 1
        self.updateAverageNbOfRetries()

    def updateAverageNbOfRetries(self):
        self.__communicationAnalyticsModel.averageNbOfRetries = (
            self.__communicationAnalyticsModel.nbOfRetries / self.__communicationAnalyticsModel.nbOfCommandSent)

    @staticmethod
    def getInstance():
        if CommunicationAnalyticsController.__INSTANCE is None:
            CommunicationAnalyticsController.__INSTANCE = CommunicationAnalyticsController()

        return CommunicationAnalyticsController.__INSTANCE
