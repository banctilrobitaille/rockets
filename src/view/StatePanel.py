import PyQt4
from PyKDE4.kdeui import KLed
from model.Rocket import Rocket
'''
Created on 2016-01-31

@author: rockets
'''
from PyQt4.Qt import QColor, QFont

class StatePanel(PyQt4.QtGui.QFrame):

    def __init__(self, parent):

        super(PyQt4.QtGui.QFrame,self).__init__(parent)
        self.__curentState = None
        self.__previousState = None
        self.__stateDict = {}
        self.setGeometry(1250,530, 250,300)
        self.palette = PyQt4.Qt.QPalette()
        self.palette.setColor(self.palette.WindowText, QColor(245,245,245))
        self.gridLayout = PyQt4.QtGui.QGridLayout()
        self.__stateDict[0] = State(name="INITIALIZING")
        self.__stateDict[1] = State(name="ON THE PAD")
        self.__stateDict[2] = State(name="IN FLIGHT")
        self.__stateDict[3] = State(name="DROGUE DESCENT")
        self.__stateDict[4] = State(name="MAIN DESCENT")
        self.__stateDict[5] = State(name="ON THE GROUND")
        self.__addStateToPanel()
        self.setLayout(self.gridLayout)
        self.show()
    
    def __addStateToPanel(self):
        
        for id, state in self.__stateDict.items():

            self.gridLayout.addWidget(state.icon,id,0)
            self.gridLayout.addWidget(state.name,id,1)

    def updateState(self, stateID):

        if self.__curentState is None:
            self.__stateDict[0].status = State.STATUS['COMPLETED']
            self.__curentState = self.__stateDict[stateID]
        elif self.__curentState is not self.__stateDict[stateID]:
            self.__curentState.status = State.STATUS['COMPLETED']
            self.__curentState = self.__stateDict[stateID]
            self.__curentState.status = State.STATUS['IN_PROGRESS']

class State(PyQt4.QtCore.QObject):

    STATUS = {

        'NOT_DONE'    : 0,
        'IN_PROGRESS' : 1,
        'COMPLETED'   : 2,
    }

    def __init__(self, name="",status=0):

        self.__status = status
        self.__name = PyQt4.QtGui.QLabel(name)
        self.__name.fontChange(QFont("Arial",20))
        self.__name.setStyleSheet("QLabel {color: white}")
        self.__icon = PyQt4.QtGui.QLabel()
        self.__icon.setAlignment(PyQt4.QtCore.Qt.AlignCenter)
        self.__icon.setSizePolicy(PyQt4.QtGui.QSizePolicy.Expanding, PyQt4.QtGui.QSizePolicy.Expanding)
        self.__icon.setMinimumSize(32,32)
        self.__icon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/not.png'))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, icon):

        self.__icon = icon

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):

        self.__status = status

        if status is State.STATUS['NOT_DONE']:
            self.__icon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/not.png'))
        elif status is State.STATUS['IN_PROGRESS']:
            self.__icon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/running.png'))
        else:
            self.__icon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/check.png'))

