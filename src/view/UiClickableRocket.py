import PyQt4
from UiMotherboardStats import MotherboardStats
from PyQt4.QtCore import pyqtSlot, pyqtSignal


class ClickableRocketWidget(PyQt4.QtGui.QFrame):

    def __init__(self, parent):
        super(ClickableRocketWidget, self).__init__(parent)

        self.setGeometry(950,530,350,350)
        self.setMouseTracking(True)
        self.__nose = RocketNose(self)
        self.__body = RocketBody(self)
        self.__bottom = RocketBottom(self)
        self.connectSlot()
        self.show()


    def connectSlot(self):

        self.__body.clicked.connect(self.__on_Body_Clicked)

    @pyqtSlot()
    def __on_Body_Clicked(self):

        self.motherboardStatsView = MotherboardStats()


class RocketNose(PyQt4.QtGui.QFrame):

    def __init__(self, parent):
        super(RocketNose, self).__init__(parent)
        self.setGeometry(0,0,350,115)
        self.setMouseTracking(True)
        self.setStyleSheet("QFrame {background-image: url(./Image_Files/payloadOFF.png);"
                           " background-repeat: no-repeat}"
                           "QFrame:hover {background-image: url(./Image_Files/payloadON.png);"
                           "  background-repeat: no-repeat}")
        self.show()


class RocketBody(PyQt4.QtGui.QFrame):

    clicked = PyQt4.QtCore.pyqtSignal()

    def __init__(self, parent):
        super(RocketBody, self).__init__(parent)
        self.setGeometry(-1,100,350,115)
        self.setMouseTracking(True)
        self.setStyleSheet("QFrame {background-image: url(./Image_Files/motherBoardOFF.png);"
                           " background-repeat: no-repeat}"
                           "QFrame:hover {background-image: url(./Image_Files/motherBoardON.png);"
                           "  background-repeat: no-repeat}")
        self.show()


    def mouseReleaseEvent(self, ev):
        self.clicked.emit()

class RocketBottom(PyQt4.QtGui.QFrame):

    def __init__(self, parent):
        super(RocketBottom, self).__init__(parent)
        self.setGeometry(-1,190,350,115)
        self.setMouseTracking(True)
        self.setStyleSheet("QFrame {background-image: url(./Image_Files/motorRocket.png);"
                           " background-repeat: no-repeat}"
                           "QFrame:hover {background-image: url(./Image_Files/motorRocket.png);"
                           "  background-repeat: no-repeat}")
        self.show()