import PyQt4
from PyQt4.QtCore import pyqtSlot


class MainToolBar(PyQt4.QtGui.QToolBar):
    ROCKET_ON_ICON_PATH = './Image_Files/rocketON.png'
    ROCKET_OFF_ICON_PATH = './Image_Files/rocketOFF.png'
    DISCOVER_ON_ICON_PATH = './Image_Files/discoverON.png'
    DISCOVER_OFF_ICON_PATH = './Image_Files/discoverOFF.png'
    STREAM_ON_ICON_PATH = './Image_Files/streamON.png'
    STREAM_OFF_ICON_PATH = './Image_Files/streamOFF.png'
    CAMERA_ON_ICON_PATH = './Image_Files/cameraON.png'
    CAMERA_OFF_ICON_PATH = './Image_Files/cameraOFF.png'

    def __init__(self):

        super(MainToolBar, self).__init__()
        self.__rocketActionDict = {}
        self.__selectedRocketAction = None

        self.__discoverAction = ToolbarAction(MainToolBar.DISCOVER_OFF_ICON_PATH, MainToolBar.DISCOVER_ON_ICON_PATH,
                                              'Discover', self)
        self.__streamAction = ToolbarAction(MainToolBar.STREAM_OFF_ICON_PATH, MainToolBar.STREAM_ON_ICON_PATH, 'Stream',
                                            self)
        self.__cameraAction = ToolbarAction(MainToolBar.CAMERA_OFF_ICON_PATH, MainToolBar.CAMERA_ON_ICON_PATH,
                                            'Start Camera', self)

        self.setup()

    @property
    def selectedRocketAction(self):
        return self.__selectedRocketAction

    @selectedRocketAction.setter
    def selectedRocketAction(self, selectedRocketAction):

        if self.__selectedRocketAction is not None:
            self.__selectedRocketAction.setIcon(PyQt4.QtGui.QIcon(MainToolBar.ROCKET_OFF_ICON_PATH))

        self.__selectedRocketAction = selectedRocketAction

        if selectedRocketAction is None:
            self.__cameraAction.setDisabled(True)
            self.__streamAction.setDisabled(True)
        else:
            self.__selectedRocketAction.setIcon(PyQt4.QtGui.QIcon(MainToolBar.ROCKET_ON_ICON_PATH))
            self.__cameraAction.setDisabled(False)
            self.__streamAction.setDisabled(False)

        self.__cameraAction.setIcon(PyQt4.QtGui.QIcon(MainToolBar.CAMERA_OFF_ICON_PATH))
        self.__streamAction.setIcon(PyQt4.QtGui.QIcon(MainToolBar.STREAM_OFF_ICON_PATH))

    @property
    def discoverAction(self):
        return self.__discoverAction

    @discoverAction.setter
    def discoverAction(self, discoverAction):
        self.__discoverAction = discoverAction

    @property
    def streamAction(self):
        return self.__streamAction

    @streamAction.setter
    def streamAction(self, streamAction):
        self.__streamAction = streamAction

    @property
    def cameraAction(self):
        return self.__cameraAction

    @cameraAction.setter
    def cameraAction(self, cameraAction):
        self.__cameraAction = cameraAction

    @property
    def rocketActionDict(self):
        return self.__rocketActionDict

    @rocketActionDict.setter
    def rocketActionDict(self, rocketActionDict):
        self.__rocketActionDict = rocketActionDict

    def setup(self):

        self.setStyleSheet("QToolBar {background: rgba(29,29,29,90);}"
                           "QToolButton { color : white; border-radius: 0px;}"
                           "QToolButton:hover {color : black; background: white}"
                           "QToolButton:!enabled {}"
                           "QLabel {color : white; padding-top : 20px; padding-bottom: 5px; qproperty-alignment: "
                           "AlignCenter;}")
        self.setToolButtonStyle(PyQt4.QtCore.Qt.ToolButtonTextBesideIcon | PyQt4.QtCore.Qt.AlignLeading)
        self.addAction(self.discoverAction)
        self.addSeparator()
        self.addAction(self.streamAction)
        self.addSeparator()
        self.addAction(self.cameraAction)
        self.addSeparator()
        self.addWidget(PyQt4.QtGui.QLabel("ROCKET LIST"))
        self.cameraAction.setDisabled(True)
        self.streamAction.setDisabled(True)
        self.setIconSize(PyQt4.QtCore.QSize(80, 80))

    def addRocketAction(self, rocketID, rocketName):

        rocketAction = ToolbarAction(MainToolBar.ROCKET_OFF_ICON_PATH, MainToolBar.ROCKET_ON_ICON_PATH,
                                     rocketName + "\n" + "ID: " + str(hex(rocketID)), self)
        self.addAction(rocketAction)
        self.__rocketActionDict[rocketID] = rocketAction

    def resetRocketList(self):

        for rocketID, rocketAction in self.__rocketActionDict.items():
            self.removeAction(rocketAction)

        self.__rocketActionDict.clear()

    def getActionFromRocketID(self, rocketID):

        return self.__rocketActionDict[rocketID]

    def animateToolbarAction(self, action):

        action.animate()

    def disableAllActions(self):
        [(lambda action: action.setDisabled(True))(action) for action in self.actions()]

    def enableRocketDiscovery(self):
        self.discoverAction.setDisabled(False)
        [(lambda rocketID, action: action.setDisabled(False))(rocketID, action) for rocketID, action in
         self.rocketActionDict.items()]


class ToolbarAction(PyQt4.QtGui.QAction):
    def __init__(self, offIconPath, onIconPath, iconText, parent):
        super(ToolbarAction, self).__init__(PyQt4.QtGui.QIcon(offIconPath), iconText, parent)
        self.__animatedIcon = PyQt4.QtGui.QMovie('./Image_Files/loader.gif')
        self.__animatedIcon.frameChanged.connect(self.__setIcon)
        self.__onIconPath = onIconPath
        self.__offIconPath = offIconPath

    @property
    def onIcon(self):
        self.__onIconPath

    @onIcon.setter
    def onIcon(self, iconPath):
        self.__onIconPath = iconPath

    @property
    def offIcon(self):
        self.__offIconPath

    @onIcon.setter
    def offIcon(self, iconPath):
        self.__offIconPath = iconPath

    def animate(self):

        if self.__animatedIcon.loopCount is not -1:
            self.__animatedIcon.finished.connect(self.__animatedIcon.start)

        self.__animatedIcon.start()

    @pyqtSlot(bool)
    def stopAnimation(self, status):
        self.__animatedIcon.stop()
        self.setDisabled(False)
        if status:
            self.setIcon(PyQt4.QtGui.QIcon(self.__onIconPath))
        else:
            self.setIcon(PyQt4.QtGui.QIcon(self.__offIconPath))

    @pyqtSlot(int)
    def __setIcon(self, frame):
        self.setIcon(PyQt4.QtGui.QIcon(self.__animatedIcon.currentPixmap()))
