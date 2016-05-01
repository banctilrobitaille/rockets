import PyQt4


class MainToolBar(PyQt4.QtGui.QToolBar):

    ROCKET_ON_ICON_PATH     = './Image_Files/rocketON.png'
    ROCKET_OFF_ICON_PATH    = './Image_Files/rocketOFF.png'
    DISCOVER_ON_ICON_PATH  = './Image_Files/discoverON.png'
    DISCOVER_OFF_ICON_PATH  = './Image_Files/discoverOFF.png'
    STREAM_ON_ICON_PATH     = './Image_Files/streamON.png'
    STREAM_OFF_ICON_PATH    = './Image_Files/streamOFF.png'
    CAMERA_ON_ICON_PATH   = './Image_Files/cameraON.png'
    CAMERA_OFF_ICON_PATH  = './Image_Files/cameraOFF.png'

    def __init__(self):

        super(MainToolBar, self).__init__()
        self.__rocketActionDict = {}
        self.__selectedRocketAction = None

        self.__discoverAction = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon(MainToolBar.DISCOVER_OFF_ICON_PATH), 'Discover', self)
        self.__streamAction = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon(MainToolBar.STREAM_OFF_ICON_PATH), 'Stream', self)
        self.__cameraAction = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon(MainToolBar.CAMERA_OFF_ICON_PATH), 'Start Camera', self)

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
                              "QLabel {color : white; padding-top : 20px; padding-bottom: 5px; qproperty-alignment: AlignCenter;}")
        self.setToolButtonStyle(PyQt4.QtCore.Qt.ToolButtonTextBesideIcon|PyQt4.QtCore.Qt.AlignLeading)
        self.addAction(self.discoverAction)
        self.addSeparator()
        self.addAction(self.streamAction)
        self.addSeparator()
        self.addAction(self.cameraAction)
        self.addSeparator()
        self.addWidget(PyQt4.QtGui.QLabel("ROCKET LIST"))
        self.cameraAction.setDisabled(True)
        self.streamAction.setDisabled(True)
        self.setIconSize(PyQt4.QtCore.QSize(80,80))


    def addRocketAction(self, rocketID, rocketName):

        rocketAction = PyQt4.QtGui.QAction(PyQt4.QtGui.QIcon(MainToolBar.ROCKET_OFF_ICON_PATH), rocketName + "\n" + "ID: " + str(hex(rocketID)), self)
        self.addAction(rocketAction)
        self.__rocketActionDict[rocketID] = rocketAction

    def resetRocketList(self):

        self.__rocketActionDict.clear()

    def getActionFromRocketID(self, rocketID):

        return self.__rocketActionDict[rocketID]