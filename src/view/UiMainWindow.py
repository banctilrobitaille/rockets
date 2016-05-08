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
from UiSlidingMessage import SlidingMessage
from UiClickableRocket import ClickableRocketWidget
from src.controller.BaseStationController import BaseStationController
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

    def __init__(self,basestationController,parent=None):
        
        PyQt4.QtGui.QMainWindow.__init__(self, parent)

        self.__baseStationController    = basestationController
        self.__rfdSerialController      = self.__baseStationController.RFD900SerialController
        self.__xbeeSerialController     = self.__baseStationController.XBeeSerialController
        self.__rocketIDToAction = {}

        self.__setupUi()
        self.__connectSlot()

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
        palette.setColor(PyQt4.QtGui.QPalette.Background,PyQt4.QtCore.Qt.black)
        self.setPalette(palette)
        self.setWindowTitle("Station de Base RockETS v0.1")
        
        """Ajout de la barre de menu"""
        self.__AddMenu()
        """Ajout des actions lies differents menus"""
        self.__AddMenuAction()
        """Ajout de la barre de status"""
        self.__AddStatusBar()

        self.__addToolBar()



        self.__dashboard = dashboard.Dashboard(self)
        #self.__compass = compass.Compass(self)
        self.__gpsTab = UiDataAnlalysis.GpsTab(self)
        self.__graphTab = UiDataAnlalysis.GraphTab(self)
        #self.__rocket = vtkRendering.rocketRendering(self)
        self.__clickableRocket = ClickableRocketWidget(self)
        self.__statePanel = StatePanel.StatePanel(self)

        self.__slidingMessage = SlidingMessage("Successfully entered in discover mode", self)

        #self.ren = vtk.vtkRenderer()
        #self.__rocket.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        #self.iren = self.__rocket.vtkWidget.GetRenderWindow().GetInteractor()
 
        #self.reader = vtk.vtkSTLReader()
        #self.reader.SetFileName("VTK_Files/original.stl")
 
        # Create a mapper
        #mapper = vtk.vtkPolyDataMapper()
        #mapper.SetInputConnection(self.reader.GetOutputPort())
 
        # Create an actor
        #actor = vtk.vtkActor()
        #actor.SetMapper(mapper)
        
        #actor.GetProperty().SetColor(1,0,0)
        #actor.SetOrientation(100,0,0)
        #self.ren.AddActor(actor)
        

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
        
        self.menubar = MenuBar(self,"menubar")
        
        """Positionnement de la barre de menu au haut de linterface"""
        self.menubar.setGeometry(PyQt4.QtCore.QRect(0, 0, 800, 26))
        self.menuFile = Menu(self.menubar, "menuFile", "File")        
        self.menuView = Menu(self.menubar, "menuView", "view")
        self.menuConnection = Menu(self.menubar, "menuConnection", "Connection")
        self.menuGPS = Menu(self.menubar, "menuGPS", "GPS")           
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
        
        """Initialisaiton et ajout du sous menu <Load Log File>"""
        self.actionLoad_Log_File = MenuAction(self,"actionLoad_Log_File", "Load Log File")
        self.menuFile.addAction(self.actionLoad_Log_File)
        
        """Initialisaiton et ajout du sous menu <Display Settings>"""
        self.actionDisplay_Settings = MenuAction(self,"actionDisplay_Settings", "Display Settings")
        self.menuView.addAction(self.actionDisplay_Settings)
        
        """Initialisaiton et ajout du sous menu <Serial Settings>"""
        self.actionRFD900_Settings = MenuAction(self,"actionSerial_Settings", "RFD900 Settings")
        self.menuConnection.addAction(self.actionRFD900_Settings)

        self.actionXBEE_Settings = MenuAction(self,"actionSerial_Settings", "XBEE Serial Settings")
        self.menuConnection.addAction(self.actionXBEE_Settings)

        """Initialisaiton et ajout du sous menu <Connect>"""
        self.actionConnect = MenuAction(self,"actionConnect", "Connect")
        self.menuConnection.addAction(self.actionConnect)
        
        """Initialisaiton et ajout du sous menu <Disconnect>"""
        self.actionDisconnect = MenuAction(self,"actionDisconnect", "Disconnect")
        self.menuConnection.addAction(self.actionDisconnect)
        
        """Initialisaiton et ajout du sous menu <Set base station position>"""
        self.actionSetLocalPosition = MenuAction(self, "actionSetLocalPosition", "Set base station position")
        self.menuGPS.addAction(self.actionSetLocalPosition)
        
        """Initialisaiton et ajout du sous menu <About>"""
        self.actionAbout = MenuAction(self,"actionAbout","About")
        self.menuAbout.addAction(self.actionAbout)
        
        """Ajout des menus en tant que action dans la barre de menu"""
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuGPS.menuAction())
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
        
        self.statusbar = PyQt4.QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        
        """Par defaut letat est non connecte ecris en rouge"""
        self.lblNotConnected = PyQt4.QtGui.QLabel("Not Connected")
        self.lblNotConnected.setStyleSheet('QLabel {color: red}')
        
        """Ajout de la barre detat"""
        self.statusbar.addWidget(self.lblNotConnected)
        self.setStatusBar(self.statusbar)

    def __addToolBar(self):

        self.__toolbar = UiToolbar.MainToolBar()
        self.addToolBar(PyQt4.QtCore.Qt.LeftToolBarArea, self.__toolbar)
        self.__updateToolBarRocketList()


    def __updateToolBarRocketList(self):

        self.__toolbar.resetRocketList()

        for rocketID, rocket in self.__baseStationController.baseStation.availableRocket.items():

            self.__toolbar.addRocketAction(rocket.ID, rocket.name)
            self.__toolbar.getActionFromRocketID(rocket.ID).triggered.connect(lambda: self.__on_Rocket_Clicked(rocket.ID))

    """
    #    Methode __connectSlot
    #    Description: Methode qui associe les actions (menus) a une methode
    #
    #    param:  None
    #    return: None
    """ 
    def __connectSlot(self):
        
        self.connect(self.actionRFD900_Settings, PyQt4.QtCore.SIGNAL("triggered()"),self.__on_RFD900_Settings_Clicked)
        self.connect(self.actionXBEE_Settings, PyQt4.QtCore.SIGNAL("triggered()"),self.__on_XBEE_Settings_Clicked)
        self.connect(self.actionAbout, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotAbout_Clicked)
        self.connect(self.actionConnect, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotConnect_Clicked)
        self.connect(self.actionDisconnect, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotDisconnect_Clicked)
        self.connect(self.actionSetLocalPosition, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotSetLocalPosition_Clicked)

        self.connect(self.__toolbar.discoverAction, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_Discover_Clicked)
        self.connect(self.__toolbar.streamAction, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_Stream_Clicked)
        self.connect(self.__toolbar.cameraAction, PyQt4.QtCore.SIGNAL("triggered()"), self.__on_Camera_Clicked)

        self.__rfdSerialController.stateChanged.connect(self.__on_serialConnectionStateChanged)
        self.__baseStationController.baseStation.availableRocketChanged.connect(self.__on_AvailableRocketChanged)
        self.__baseStationController.baseStation.connectedRocketChanged.connect(self.__on_connectedRocketChanged)
        self.__baseStationController.baseStation.coordsChanged.connect(self.__on_BaseStationCoordsChanged)

        self.__baseStationController.GPS.fixTimeChanged.connect(self.__on_FixTimeChanged)
        self.__baseStationController.GPS.fixChanged.connect(self.__on_FixChanged)
        self.__baseStationController.GPS.nbSatellitesChanged.connect(self.__on_SatellitesChanged)

        self.__baseStationController.RFD900.newCommandStreamer.connect(self.__on_Command_Sent)
        self.__baseStationController.RFD900.errorOccured.connect(self.__on_Error)
        self.__baseStationController.RFD900.discoveringRocket.connect(self.__on_DiscoveringRocket_Changed)

        self.__baseStationController.XBee.newCommandStreamer.connect(self.__on_Command_Sent)
        self.__baseStationController.XBee.errorOccured.connect(self.__on_Error)

    def __connectRocketSlot(self):

        self.__baseStationController.baseStation.connectedRocket.speedChanged.connect(self.__on_SpeedChanged)
        self.__baseStationController.baseStation.connectedRocket.accelerationChanged.connect(self.__on_AccelerationChanged)
        self.__baseStationController.baseStation.connectedRocket.altitudeChanged.connect(self.__on_AltitudeChanged)
        self.__baseStationController.baseStation.connectedRocket.temperatureChanged.connect(self.__on_TemperatureChanged)
        self.__baseStationController.baseStation.connectedRocket.cameraStateChanged.connect(self.__on_CameraState_Changed)
        self.__baseStationController.baseStation.connectedRocket.coordsChanged.connect(self.__on_RocketCoordsChanged)
        self.__baseStationController.baseStation.connectedRocket.stateChanged.connect(self.__on_RocketStateChanged)

    @pyqtSlot(object)
    def __on_AvailableRocketChanged(self, availableRocket):

        self.__toolbar.resetRocketList()

        for rocketID,rocket in availableRocket.items():

            self.__toolbar.addRocketAction(rocketID, rocket.name)
            self.__toolbar.getActionFromRocketID(rocket.ID).triggered.connect(lambda: self.__on_Rocket_Clicked(rocket.ID))

    @pyqtSlot(object)
    def __on_connectedRocketChanged(self, rocket):

        if rocket is not None:

            self.__connectRocketSlot()
            self.__toolbar.selectedRocketAction = self.__toolbar.getActionFromRocketID(rocket.ID)
        else:

            self.__toolbar.selectedRocketAction = None

    @pyqtSlot(int)
    def __on_SpeedChanged(self, speed):
        
        self.__dashboard.updateSpeed(speed)
        self.__graphTab.addSpeedData(speed)
    
    @pyqtSlot(float)
    def __on_AccelerationChanged(self, acceleration):
        
        self.__dashboard.updateAcceleration(acceleration)
        self.__graphTab.addAccelerationData(acceleration)
    
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

    @pyqtSlot(int)
    def __on_SatellitesChanged(self, nbSatellite):

        self.__gpsTab.map.nbSatellite = nbSatellite

    def __slotAbout_Clicked(self):
        
        PyQt4.QtGui.QMessageBox.about(self, "About", "Base Station for RockETS 2015")
        self.__slidingMessage.reveal()
        #self.__gpsTab.map.updateMarker(-90,46.8)

    def __on_Discover_Clicked(self):

        if self.__baseStationController.RFD900.isDiscoveringRocket:
            self.__baseStationController.RFD900.stopRocketDiscovery()
        else:
            self.__baseStationController.RFD900.startRocketDiscovery()

    @pyqtSlot(bool)
    def __on_DiscoveringRocket_Changed(self, discoveringRocket):

        if discoveringRocket:
            self.__toolbar.discoverAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.DISCOVER_ON_ICON_PATH))
        else:
            self.__toolbar.discoverAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.DISCOVER_OFF_ICON_PATH))

    @pyqtSlot(object)
    def __on_Command_Sent(self, commandStreamer):

        commandStreamer.rocketDidNotRespond.connect(self.__on_Error)

    @pyqtSlot(str)
    def __on_Error(self, errorMessage):

        SlidingMessage(errorMessage, self).reveal()

    def __on_Camera_Clicked(self):

        if self.__baseStationController.baseStation.connectedRocket.cameraON:

            cameraMsg = PyQt4.QtGui.QMessageBox( PyQt4.QtGui.QMessageBox.Question, "CAMERA WARNING",
                                                 "Do you really want to close connected rocket's cameras ?",
                                                 PyQt4.QtGui.QMessageBox.Yes | PyQt4.QtGui.QMessageBox.No)

            cameraMsg.setStyleSheet("QMessageBox {color:rgba(249,105,14,100);background-color:rgba(29,29,29,50); border:0px}"
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

        if self.__baseStationController.RFD900.streaming:
            self.__baseStationController.RFD900.stopStream()
            self.__toolbar.streamAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.STREAM_OFF_ICON_PATH))
        else:
            self.__baseStationController.RFD900.startStream()
            self.__toolbar.streamAction.setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.STREAM_ON_ICON_PATH))



    def __on_Rocket_Clicked(self, rocketID):

        if self.__baseStationController.baseStation.connectedRocket is \
                self.__baseStationController.baseStation.availableRocket[rocketID]:

            rocketMsg = PyQt4.QtGui.QMessageBox(PyQt4.QtGui.QMessageBox.Warning, "ROCKET WARNING",
                                                 "Do you really want to disconnect from rocket ?",
                                                 PyQt4.QtGui.QMessageBox.Yes | PyQt4.QtGui.QMessageBox.No)

            rocketMsg.setIconPixmap(PyQt4.QtGui.QPixmap(UiToolbar.MainToolBar.ROCKET_OFF_ICON_PATH))
            rocketMsg.setStyleSheet("QMessageBox {color:rgba(249,105,14,100);background-color:rgba(29,29,29,50); border:0px}"
                                    "QMessageBox QLabel {color : rgba(249,105,14);}"
                                    "QMessageBox QPushButton {background-color : white;}"
                                    "QMessageBox QPushButton:hover {background-color: rgb(236,236,236);}")
            result = rocketMsg.exec_()

            if result == PyQt4.QtGui.QMessageBox.Yes:
                self.__toolbar.rocketActionDict[rocketID].setIcon(PyQt4.QtGui.QIcon(UiToolbar.MainToolBar.ROCKET_OFF_ICON_PATH))
                self.__baseStationController.disconnectFromRocket(rocketID)
            else:
                rocketMsg.close()
        else:

            self.__baseStationController.updateConnectedRocket(rocketID)


    def __on_RFD900_Settings_Clicked(self):
        
        self.__showSerialProperties(self.__rfdSerialController)

    def __on_XBEE_Settings_Clicked(self):

        self.__showSerialProperties(self.__xbeeSerialController)

    
    def __slotConnect_Clicked(self):
        pass
    
        
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
    
    
    @pyqtSlot(bool)
    def __on_serialConnectionStateChanged(self, isConnected):
        
        if isConnected:
            
            self.statusbar.removeWidget(self.lblNotConnected)
            self.lblNotConnected = PyQt4.QtGui.QLabel("Connected")
            self.lblNotConnected.setStyleSheet('QLabel {color: green}')
            self.statusbar.addWidget(self.lblNotConnected)
            self.statusbar.update()
        else:
            
            self.statusbar.removeWidget(self.lblNotConnected)
            self.lblNotConnected = PyQt4.QtGui.QLabel("Not Connected")
            self.lblNotConnected.setStyleSheet('QLabel {color: red}')
            self.statusbar.addWidget(self.lblNotConnected)
            self.statusbar.update()
    
    @pyqtSlot(float, float)
    def __on_BaseStationCoordsChanged(self,latitude, longitude):

        self.__gpsTab.map.updateBaseStationMarker(longitude, latitude)

    @pyqtSlot(float, float)
    def __on_RocketCoordsChanged(self, latitude, longitude):

        self.__gpsTab.map.updateRocketMarker(longitude, latitude)


class MenuBar(PyQt4.QtGui.QMenuBar):
    
    def __init__(self, parent, objectName):
        
        PyQt4.QtGui.QMenuBar.__init__(self,parent)
        self.setObjectName(objectName)

class Menu(PyQt4.QtGui.QMenu):
    
    def __init__(self, parent, objectName, objectTitle):
        
        PyQt4.QtGui.QMenu.__init__(self,parent)
        self.setObjectName(objectName)
        self.setTitle(objectTitle)
      
        
class MenuAction(PyQt4.QtGui.QAction):
    
    def __init__(self,parent, objectName, text):
        
        PyQt4.QtGui.QAction.__init__(self,parent)
        self.setObjectName(objectName)
        self.setText(text)
        