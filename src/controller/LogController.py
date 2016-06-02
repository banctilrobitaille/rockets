import PyQt4
from datetime import datetime

from PyQt4.QtCore import pyqtSignal

'''
Created on 2016-01-27

@author: rockets
'''


class LogController(PyQt4.QtCore.QObject):
    errorOccured = PyQt4.QtCore.pyqtSignal(str)
    newInfos = PyQt4.QtCore.pyqtSignal(str)
    newSuccess = PyQt4.QtCore.pyqtSignal(str)
    __INSTANCE = None

    def __init__(self):
        super(LogController, self).__init__()

    """
    TO DO
    """

    def writeLogToFile(self, path, data):
        pass

    """
    TO DO
    """

    def readLogFromFile(self, path):
        pass

    def infos(self, message, dateTime=datetime.now(), verbose=True):
        if verbose:
            self.newInfos.emit(message)

    def error(self, message, dateTime=datetime.now(), verbose=True):
        if verbose:
            self.errorOccured.emit(message)

    def success(self, message, dateTime=datetime.now(), verbose=True):
        if verbose:
            self.newSuccess.emit(message)

    @staticmethod
    def getInstance():

        if LogController.__INSTANCE is None:
            LogController.__INSTANCE = LogController()

        return LogController.__INSTANCE
