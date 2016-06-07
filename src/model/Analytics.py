import PyQt4


class CommunicationAnalytics(PyQt4.QtCore.QObject):
    __INSTANCE = None

    def __init__(self):
        super(CommunicationAnalytics, self).__init__()
        self.__nbOfFrameSent = 0
        self.__nbOfFrameReceived = 0
        self.__nbOfBadFrameReceived = 0
        self.__nbOfBadFrameSent = 0
        self.__nbOfRetries = 0
        self.__averageNbOfRetries = 0
        self.__nbOfFrameLost = 0
        self.__nbOfCommandSent = 0
        self.__retryHistory = {'Time': [], 'Retry': [0, ]}
        self.__firstRetryTimeReference = None
        self.__commandSentDict = {}
        self.__FrameSent = []
        self.__FrameReceived = []

    @property
    def nbOfFrameSent(self):
        return self.__nbOfFrameSent

    @nbOfFrameSent.setter
    def nbOfFrameSent(self, nbOfFrameSent):
        self.__nbOfFrameSent = nbOfFrameSent

    @property
    def nbOfFrameReceived(self):
        return self.__nbOfFrameReceived

    @nbOfFrameReceived.setter
    def nbOfFrameReceived(self, nbOfFrameReceived):
        self.__nbOfFrameReceived = nbOfFrameReceived

    @property
    def nbOfBadFrameReceived(self):
        return self.__nbOfBadFrameReceived

    @nbOfBadFrameReceived.setter
    def nbOfBadFrameReceived(self, nbOfBadFrameReceived):
        self.__nbOfBadFrameReceived = nbOfBadFrameReceived

    @property
    def nbOfBadFrameSent(self):
        return self.__nbOfBadFrameSent

    @nbOfBadFrameSent.setter
    def nbOfBadFrameSent(self, nbOfBadFrameSent):
        self.__nbOfBadFrameSent = nbOfBadFrameSent

    @property
    def frameSent(self):
        return self.__FrameSent

    @frameSent.setter
    def frameSent(self, frameSent):
        self.__FrameSent = frameSent

    @property
    def frameReceived(self):
        return self.__FrameReceived

    @frameReceived.setter
    def frameReceived(self, frameReceived):
        self.__FrameReceived = frameReceived

    @property
    def nbOfRetries(self):
        return self.__nbOfRetries

    @nbOfRetries.setter
    def nbOfRetries(self, nbOfRetries):
        self.__nbOfRetries = nbOfRetries

    @property
    def averageNbOfRetries(self):
        return self.__averageNbOfRetries

    @averageNbOfRetries.setter
    def averageNbOfRetries(self, averageNbOfRetries):
        self.__averageNbOfRetries = averageNbOfRetries

    @property
    def nbOfFrameLost(self):
        return self.__nbOfFrameLost

    @nbOfFrameLost.setter
    def nbOfFrameLost(self, nbOfFrameLost):
        self.__nbOfFrameLost = nbOfFrameLost

    @property
    def nbOfCommandSent(self):
        return self.__nbOfCommandSent

    @nbOfCommandSent.setter
    def nbOfCommandSent(self, nbOfCommandSent):
        self.__nbOfCommandSent = nbOfCommandSent

    @property
    def retryHistory(self):
        return self.__retryHistory

    @retryHistory.setter
    def retryHistory(self, retryHistory):
        self.__retryHistory = retryHistory

    @property
    def firstRetryTimeReference(self):
        return self.__firstRetryTimeReference

    @firstRetryTimeReference.setter
    def firstRetryTimeReference(self, firstRetryTimeReference):
        self.__firstRetryTimeReference = firstRetryTimeReference

    @property
    def commandSentDict(self):
        return self.__commandSentDict

    @commandSentDict.setter
    def commandSentDict(self, commandSentDict):
        self.__commandSentDict = commandSentDict

    @staticmethod
    def getInstance():

        if CommunicationAnalytics.__INSTANCE is None:
            CommunicationAnalytics.__INSTANCE = CommunicationAnalytics()

        return CommunicationAnalytics.__INSTANCE