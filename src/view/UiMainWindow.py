import PyQt4
import dashboard
import UiDataAnlalysis
import UiSerialProperties
import vtkRendering
import vtk
import UiGpsSettings
from PyQt4.Qt import pyqtSlot
import StatePanel
import UiToolbar
from UiSlidingMessage import ErrorSlidingMessage, NotificationSlidingMessage, SuccessSlidingMessage
from UiClickableRocket import ClickableRocketWidget
from controller.Communication import FrameFactory
from controller.LogController import LogController
from Exception import SerialDeviceException
from controller.ReportGenerator import CommunicationAnalyticsReportGenerator, FlightReportGenerator

"""#############################################################################
# 
# Nom du module:          UiMainWindow
# Auteur:                 Benoit Anctil-Robitaille, Amine Waddah
# Date:                   8 Septembre 2015
# Description:            Le module UiMainWindow.py regroupe les classes necessaires
#                         a laffichage de la fenetre permettant principale.
#
##############################################################################"""


class MainWindow(PyQt4.QtGui.QMainWindow):
    def __init__(self, basestationController, parent=None):

        PyQt4.QtGui.QMainWindow.__init__(self, parent)

        self.__LOGGER = LogController.getInstance()
        self.__baseStationController = basestationController
        self.__rfdSerialController = self.__baseStationController.RFD900SerialController
        self.__xbeeSerialController = self.__baseStationController.XBeeSerialController
        self.__rocketIDToAction = {}

        self.__setupUi()
        self.__connectSlot()

        try:
            self.__baseStationController.connectSerialDevices()
        except SerialDeviceException.UnableToConnectException as e:
            self.__toolbar.disableAllActions()

    """
    #    Methode __setupUi
    #    Description: Methode initialisant les composants graphiques
    #                 de la fenetre et les positionne.
    #
    #    param:  None
    #    return: None
    """

    def __setupUi(self):

        self.setObjectName("MainWindow")
        self.resize(PyQt4.Qt.QDesktopWidget().availableGeometry(self).size())
        self.setMouseTracking(False)
        self.centralwidget = PyQt4.QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        palette = PyQt4.QtGui.QPalette()
        palette.setColor(PyQt4.QtGui.QPalette.Background, PyQt4.QtCore.Qt.black)
        self.setPalette(palette)
        self.setWindowTitle("Station de Base RockETS v0.1")
        self.__systemTrayIcon = PyQt4.QtGui.QSystemTrayIcon(PyQt4.QtGui.QIcon('./Image_Files/rocketsLogo32x32.png'),
                                                            self)
        self.__systemTrayIcon.show()
        self.setWindowIcon(PyQt4.QtGui.QIcon('./Image_Files/rocketsLogo32x32.png'))

        """Ajout de la barre de menu"""
        self.__AddMenu()
        """Ajout des actions lies differents menus"""
        self.__AddMenuAction()
        """Ajout de la barre de status"""
        self.__AddStatusBar()

        self.__addToolBar()

        self.__dashboard = dashboard.Dashboard(self)
        self.__gpsTab = UiDataAnlalysis.GpsTab(self)
        self.__graphTab = UiDataAnlalysis.GraphTab(self)
        # self.__rocket = vtkRendering.rocketRendering(self)
        self.__clickableRocket = ClickableRocketWidget(self)
        self.__statePanel = StatePanel.StatePanel(self)

        # self.ren = vtk.vtkRenderer()
        # self.__rocket.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        # self.iren = self.__rocket.vtkWidget.GetRenderWindow().GetInteractor()

        # self.reader = vtk.vtkSTLReader()
        # self.reader.SetFileName("VTK_Files/original.stl")

        # Create a mapper
        # mapper = vtk.vtkPolyDataMapper()
        # mapper.SetInputConnection(self.reader.GetOutputPort())

        # Create an actor
        # actor = vtk.vtkActor()
        # actor.SetMapper(mapper)

        # actor.GetProperty().SetColor(1,0,0)
        # actor.SetOrientation(100,0,0)
        # self.ren.AddActor(actor)


        PyQt4.QtCore.QMetaObject.connectSlotsByName(self)

    """
    #    Methode __AddMenu
    #    Description: Methode initialisant la barre de menu de linterface
    #                 et les menus de la barre de menus
    #
    #    param:  None
    #    return: None
    """

    def __AddMenu(self):

        self.menubar = MenuBar(self, "menubar")

        """Positionnement de la barre de menu au haut de linterface"""
        self.menubar.setGeometry(PyQt4.QtCore.QRect(0, 0, 800, 26))
        self.menuConnection = Menu(self.menubar, "menuConnection", "Connection")
        self.menuReport = Menu(self.menubar, "menuReport", "Report")
        self.menuAbout = Menu(self.menubar, "menuAbout", "Help")
        self.setMenuBar(self.menubar)

    """
    #    Methode __AddMenuAction
    #    Description: Methode initialisant les sous menus (action) des menus
    #                 de la barre de menus
    #
    #    param:  None
    #    return: None
    """

    def __AddMenuAction(self):

        """Initialisaiton et ajout du sous menu <Serial Settings>"""
        self.actionRFD900_Settings = MenuAction(self, "actionSerial_Settings", "RFD900 Settings")
        self.menuConnection.addAction(self.actionRFD900_Settings)

        self.actionXBEE_Settings = MenuAction(self, "actionSerial_Settings", "XBEE Serial Settings")
        self.menuConnection.addAction(self.actionXBEE_Settings)

        """Initialisaiton et ajout du sous menu <Connect>"""
        self.actionConnect = MenuAction(self, "actionConnect", "Connect")
        self.menuConnection.addAction(self.actionConnect)

        """Initialisaiton et ajout du sous menu <Disconnect>"""
        self.actionDisconnect = MenuAction(self, "actionDisconnect", "Disconnect")
        self.menuConnection.addAction(self.actionDisconnect)

        self.actionGenerateAnalytics = MenuAction(self, "actionGenerateAnalytics", "Generate Analytics Report")
        self.menuReport.addAction(self.actionGenerateAnalytics)

        self.actionGenerateFlightReport = MenuAction(self, "actionGenerateFlightReport", "Generate Flight Report")
        self.menuReport.addAction(self.actionGenerateFlightReport)

        """Initialisaiton et ajout du sous menu <About>"""
        self.actionAbout = MenuAction(self, "actionAbout", "About")
        self.menuAbout.addAction(self.actionAbout)

        """Ajout des menus en tant que action dans la barre de menu"""
        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuReport.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

    """
    #    Methode __AddStatusBar
    #    Description: Methode qui initialise et ajoute la barre detat
    #                 a linterface principale
    #
    #    param:  None
    #    return: None
    """

    def __AddStatusBar(self):
        self.__statusBar = PyQt4.QtGui.QStatusBar(self)

        self.__statusBarMessage = PyQt4.QtGui.QLabel("")

        self.__statusBar.addWidget(self.__statusBarMessage)
        self.setStatusBar(self.__statusBar)

    def __addToolBar(self):

        self.__toolbar = UiToolbar.MainToolBar()
        self.addToolBar(PyQt4.QtCore.Qt.LeftToolBarArea, self.__toolbar)
        self.__updateToolBarRocketList()

    def __updateToolBarRocketList(self):

        self.__toolbar.resetRocketList()

        for rocketID, rocket in self.__baseStationController.baseStation.availableRocket.items():
            self.__toolbar.addRocketAction(rocket.ID, rocket.name)
            self.__toolbar.getActionFromRocketID(rocket.ID).triggered.connect(
                    lambda: self.__on_Rocket_Clicked(rocket.ID))

    """
    #    Methode __connectSlot
    #    Description: Methode qui associe les actions (menus) a une methode
    #
    #    param:  None
    #    return: None
    """

    def __connectSlot(self):

        self.connect(self.actionRFD900_Settings, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_RFD900_Settings_Clicked)
        self.connect(self.actionXBEE_Settings, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_XBEE_Settings_Clicked)
        self.connect(self.actionAbout, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotAbout_Clicked)
        self.connect(self.actionConnect, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_Connect_Clicked)
        self.connect(self.actionDisconnect, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotDisconnect_Clicked)
        self.connect(self.actionGenerateAnalytics, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_GenerateAnalytics_Clicked)
        self.connect(self.actionGenerateFlightReport, PyQt4.QtCore.SIGNAL("triggered()"),
                     self.__on_GenerateFlightReport_Clicked)

        self.connect(self.__toolbar.discoverAction, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_Discover_Clicked)
        self.connect(self.__toolbar.streamAction, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_Stream_Clicked)
        self.connect(self.__toolbar.cameraAction, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_Camera_Clicked)

        self.__LOGGER.errorOccured.connect(self.__on_Error)
        self.__LOGGER.newInfos.connect(self.__on_Notif)
        self.__LOGGER.newSuccess.connect(self.__on_Success)

        self.__rfdSerialController.stateChanged.connect(self.__on_serialConnectionStateChanged)

        self.__baseStationController.baseStation.availableRocketChanged.connect(self.__on_AvailableRocketChanged)
        self.__baseStationController.baseStation.connectedRocketChanged.connect(self.__on_connectedRocketChanged)
        self.__baseStationController.baseStation.coordsChanged.connect(self.__on_BaseStationCoordsChanged)

        self.__baseStationController.GPS.fixTimeChanged.connect(self.__on_FixTimeChanged)
        self.__baseStationController.GPS.fixChanged.connect(self.__on_FixChanged)
        self.__baseStationController.GPS.nbSatellitesChanged.connect(self.__on_SatellitesChanged)

        self.__baseStationController.RFD900.newCommandStreamer.connect(self.__on_Command_Sent)
        self.__baseStationController.RFD900.discoveringRocket.connect(self.__on_DiscoveringRocket_Changed)

        self.__baseStationController.XBee.newCommandStreamer.connect(self.__on_Command_Sent)

    def __connectRocketSlot(self):

        self.__baseStationController.baseStation.connectedRocket.speedChanged.connect(self.__on_SpeedChanged)
        self.__baseStationController.baseStation.connectedRocket.accelerationChanged.connect(
                self.__on_AccelerationChanged)
        self.__baseStationController.baseStation.connectedRocket.altitudeChanged.connect(self.__on_AltitudeChanged)
        self.__baseStationController.baseStation.connectedRocket.temperatureChanged.connect(
                self.__on_TemperatureChanged)
        self.__baseStationController.baseStation.connectedRocket.cameraStateChanged.connect(
                self.__on_CameraState_Changed)
        self.__baseStationController.baseStation.connectedRocket.coordsChanged.connect(self.__on_RocketCoordsChanged)
        self.__baseStationController.baseStation.connectedRocket.stateChanged.connect(self.__on_RocketStateChanged)
        self.__baseStationController.baseStation.connectedRocket.streamingStateChanged.connect(
                self.__on_StreamingState_Changed)

    @pyqtSlot(object)
    def __on_AvailableRocketChanged(self, availableRocket):

        self.__toolbar.resetRocketList()

        for rocketID, rocket in availableRocket.items():
            self.__toolbar.addRocketAction(rocketID, rocket.name)
            self.__toolbar.getActionFromRocketID(rocket.ID).triggered.connect(
                    lambda: self.__on_Rocket_Clicked(rocket.ID))

    @pyqtSlot(object)
    def __on_connectedRocketChanged(self, rocket):

        if rocket is not None:
            self.__connectRocketSlot()
            self.__toolbar.selectedRocketAction = self.__toolbar.getActionFromRocketID(rocket.ID)
        else:
            self.__toolbar.selectedRocketAction = None

    @pyqtSlot(int)
    def __on_SpeedChanged(self, speed):

        self.__dashboard.updateSpeed(round(speed / 1.46666666666667, 2))
        self.__graphTab.addSpeedData(round(speed / 1.46666666666667, 2))

    @pyqtSlot(float)
    def __on_AccelerationChanged(self, acceleration):

        self.__dashboard.updateAcceleration(round(acceleration * 0.3048, 2))
        self.__graphTab.addAccelerationData(round(acceleration * 0.3048, 2))

    @pyqtSlot(float)
    def __on_AltitudeChanged(self, altitude):

        self.__dashboard.updateAltitude(altitude)
        self.__graphTab.addAltitudeData(altitude)

    @pyqtSlot(float)
    def __on_TemperatureChanged(self, temperature):

        self.__dashboard.updateTemperature(temperature)
        self.__graphTab.addTemperatureData(temperature)

    @pyqtSlot(int)
    def __on_RocketStateChanged(self, state):
        self.__statePanel.updateState(state)

    @pyqtSlot(str)
    def __on_FixTimeChanged(self, fixTime):
        pass

    @pyqtSlot(str)
    def __on_FixChanged(self, fix):

        self.__gpsTab.map.gpsFix = fix

    @pyqtSlot(bool)
    def __on_CameraState_Changed(self, state):

        if state:
            self.__toolbar.cameraAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.CAMERA_ON_ICON_PATH))
        else:
            self.__toolbar.cameraAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.CAMERA_OFF_ICON_PATH))

    @pyqtSlot(bool)
    def __on_StreamingState_Changed(self, state):

        if state:
            self.__toolbar.streamAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.STREAM_ON_ICON_PATH))
        else:
            self.__toolbar.streamAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.STREAM_OFF_ICON_PATH))

    @pyqtSlot(int)
    def __on_SatellitesChanged(self, nbSatellite):

        self.__gpsTab.map.nbSatellite = nbSatellite

    @pyqtSlot(bool)
    def __on_DiscoveringRocket_Changed(self, discoveringRocket):

        if discoveringRocket:
            self.__toolbar.discoverAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.DISCOVER_ON_ICON_PATH))
        else:
            self.__toolbar.discoverAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.DISCOVER_OFF_ICON_PATH))

    @pyqtSlot(object)
    def __on_Command_Sent(self, commandStreamer):

        if commandStreamer.command is FrameFactory.COMMAND["START_CAMERA"] or \
                        commandStreamer.command is FrameFactory.COMMAND["STOP_CAMERA"]:
            commandStreamer.commandStreamEnded.connect(self.__toolbar.cameraAction.stopAnimation)
        elif commandStreamer.command is FrameFactory.COMMAND["START_STREAM"] or \
                        commandStreamer.command is FrameFactory.COMMAND["STOP_STREAM"]:
            commandStreamer.commandStreamEnded.connect(self.__toolbar.streamAction.stopAnimation)

    @pyqtSlot(str)
    def __on_Error(self, errorMessage):
        ErrorSlidingMessage(errorMessage, self).reveal()

    @pyqtSlot(str)
    def __on_Notif(self, notifMessage):
        NotificationSlidingMessage(notifMessage, self).reveal()

    @pyqtSlot(str)
    def __on_Success(self, sucessMessage):
        SuccessSlidingMessage(sucessMessage, self).reveal()

    @pyqtSlot(bool)
    def __on_serialConnectionStateChanged(self, isConnected):

        if isConnected:

            self.statusbar.removeWidget(self.__statusBarMessage)
            self.__statusBarMessage = PyQt4.QtGui.QLabel("Connected")
            self.__statusBarMessage.setStyleSheet('QLabel {color: green}')
            self.statusbar.addWidget(self.__statusBarMessage)
            self.statusbar.update()
        else:

            self.statusbar.removeWidget(self.__statusBarMessage)
            self.__statusBarMessage = PyQt4.QtGui.QLabel("Not Connected")
            self.__statusBarMessage.setStyleSheet('QLabel {color: red}')
            self.statusbar.addWidget(self.__statusBarMessage)
            self.statusbar.update()

    @pyqtSlot(float, float)
    def __on_BaseStationCoordsChanged(self, latitude, longitude):

        self.__gpsTab.map.updateBaseStationMarker(longitude, latitude)

    @pyqtSlot(float, float)
    def __on_RocketCoordsChanged(self, latitude, longitude):

        self.__gpsTab.map.updateRocketMarker(longitude, latitude)

    def __on_Camera_Clicked(self):

        self.__toolbar.animateToolbarAction(self.__toolbar.cameraAction)
        self.__toolbar.cameraAction.setDisabled(True)

        if self.__baseStationController.baseStation.connectedRocket.cameraON:

            cameraMsg = PyQt4.QtGui.QMessageBox(PyQt4.QtGui.QMessageBox.Question, "CAMERA WARNING",
                                                "Do you really want to close connected rocket's cameras ?",
                                                PyQt4.QtGui.QMessageBox.Yes | PyQt4.QtGui.QMessageBox.No)

            cameraMsg.setStyleSheet(
                    "QMessageBox {color:rgba(249,105,14,100);background-color:rgba(29,29,29,50); border:0px}"
                    "QMessageBox QLabel {color : rgba(249,105,14);}"
                    "QMessageBox QPushButton {background-color : white;}"
                    "QMessageBox QPushButton:hover {background-color: rgb(236,236,236);}")
            result = cameraMsg.exec_()

            if result == PyQt4.QtGui.QMessageBox.Yes:
                self.__baseStationController.XBee.StopCamera()
            else:
                cameraMsg.close()
        else:
            self.__baseStationController.XBee.StartCamera()

    def __on_Stream_Clicked(self):

        self.__toolbar.animateToolbarAction(self.__toolbar.streamAction)
        self.__toolbar.streamAction.setDisabled(True)

        if self.__baseStationController.baseStation.connectedRocket.isStreaming:
            self.__baseStationController.RFD900.stopStream()
        else:
            self.__baseStationController.RFD900.startStream()

    def __on_Rocket_Clicked(self, rocketID):

        if self.__baseStationController.baseStation.connectedRocket is \
                self.__baseStationController.baseStation.availableRocket[rocketID]:

            rocketMsg = PyQt4.QtGui.QMessageBox(PyQt4.QtGui.QMessageBox.Warning, "ROCKET WARNING",
                                                "Do you really want to disconnect from rocket ?",
                                                PyQt4.QtGui.QMessageBox.Yes | PyQt4.QtGui.QMessageBox.No)

            rocketMsg.setIconPixmap(PyQt4.QtGui.QPixmap(UiToolbar.MainToolBar.ROCKET_OFF_ICON_PATH))
            rocketMsg.setStyleSheet(
                    "QMessageBox {color:rgba(249,105,14,100);background-color:rgba(29,29,29,50); border:0px}"
                    "QMessageBox QLabel {color : rgba(249,105,14);}"
                    "QMessageBox QPushButton {background-color : white;}"
                    "QMessageBox QPushButton:hover {background-color: rgb(236,236,236);}")
            result = rocketMsg.exec_()

            if result == PyQt4.QtGui.QMessageBox.Yes:
                self.__toolbar.rocketActionDict[rocketID].setIcon(
                        PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.ROCKET_OFF_ICON_PATH))
                self.__baseStationController.disconnectFromRocket(rocketID)
                self.__dashboard.resetValue()
                self.__graphTab.resetAllGraph()
                self.__statePanel
            else:
                rocketMsg.close()
        else:

            self.__baseStationController.updateConnectedRocket(rocketID)

    def __on_RFD900_Settings_Clicked(self):

        self.__showSerialProperties(self.__rfdSerialController)

    def __on_XBEE_Settings_Clicked(self):

        self.__showSerialProperties(self.__xbeeSerialController)

    def __on_Connect_Clicked(self):
        try:
            self.__baseStationController.connectSerialDevices()
            self.__statusBarMessage.setText("Ready to connect !")
            self.__statusBarMessage.setStyleSheet('QLabel {color: green}')
            self.__toolbar.enableRocketDiscovery()
        except SerialDeviceException.UnableToConnectException as e:
            self.__toolbar.disableAllActions()
            self.__statusBarMessage.setText(
                    "Communication devices not working properly, please configure them and reconnect")
            self.__statusBarMessage.setStyleSheet('QLabel {color: red}')

    def __slotDisconnect_Clicked(self):
        pass

    def __slotSetLocalPosition_Clicked(self):

        self.__showGPSProperties()

    def __showSerialProperties(self, serialController):

        self.serialProperties = UiSerialProperties.SerialPropertiesWindow(serialController)
        self.serialProperties.show()

    def __showGPSProperties(self):

        self.gpsProperties = UiGpsSettings.GpsSettingWindow(self.__gpsTab.map)
        self.gpsProperties.show()

    def __slotAbout_Clicked(self):

        PyQt4.QtGui.QMessageBox.about(self, "About", "Base Station for RockETS 2015")

        # self.__gpsTab.map.updateMarker(-90,46.8)
        reportGeneratot = CommunicationAnalyticsReportGenerator()
        reportGeneratot.generateTelemetryAnalyticReport()
        reportGeneratot.createReportFile()

    def __on_Discover_Clicked(self):

        if self.__baseStationController.RFD900.isDiscoveringRocket:
            self.__baseStationController.RFD900.stopRocketDiscovery()
        else:
            self.__baseStationController.RFD900.startRocketDiscovery()

    def __on_GenerateAnalytics_Clicked(self):
        CommunicationAnalyticsReportGenerator().generateTelemetryAnalyticReport()

    def __on_GenerateFlightReport_Clicked(self):
        reportGenerator = FlightReportGenerator()
        reportGenerator.generateReportContent()
        reportGenerator.createReportFile()

class MenuBar(PyQt4.QtGui.QMenuBar):
    def __init__(self, parent, objectName):
        PyQt4.QtGui.QMenuBar.__init__(self, parent)
        self.setObjectName(objectName)


class Menu(PyQt4.QtGui.QMenu):
    def __init__(self, parent, objectName, objectTitle):
        PyQt4.QtGui.QMenu.__init__(self, parent)
        self.setObjectName(objectName)
        self.setTitle(objectTitle)


class MenuAction(PyQt4.QtGui.QAction):
    def __init__(self, parent, objectName, text):
        PyQt4.QtGui.QAction.__init__(self, parent)
        self.setObjectName(objectName)
        self.setText(text)
