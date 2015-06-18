import PyQt4
import dashboard
import compass
import UiDataAnlalysis
import UiSerialProperties
import terminal
import serialIO
import vtkRendering
import vtk
import UiGpsSettings


class MainWindow(PyQt4.QtGui.QMainWindow):

    def __init__(self,serialConnection,parent=None):
        
        PyQt4.QtGui.QMainWindow.__init__(self, parent)
        self.serialConnection = serialConnection
        self.dataThread = serialIO.Thread(self.serialConnection)
        self.__setupUi()
        
    def __setupUi(self):
        
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.setMouseTracking(False)
        self.centralwidget = PyQt4.QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        palette = PyQt4.QtGui.QPalette()
        palette.setColor(PyQt4.QtGui.QPalette.Background,PyQt4.QtCore.Qt.black)
        self.setPalette(palette)
        self.setWindowTitle("Station de Base RockETS v0.1")
        
        self.__AddMenu()
        self.__AddMenuAction()
        self.__AddStatusBar()
        
        self.__dashboard = dashboard.Dashboard(self)
        self.__compass = compass.Compass(self)
        self.__rocket = vtkRendering.rocketRendering(self)
        
        self.ren = vtk.vtkRenderer()
        self.__rocket.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.__rocket.vtkWidget.GetRenderWindow().GetInteractor()
 
        self.reader = vtk.vtkSTLReader()
        self.reader.SetFileName("original.stl")
 
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.reader.GetOutputPort())
 
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        actor.GetProperty().SetColor(1,0,0)
        actor.SetOrientation(100,0,0)
        self.ren.AddActor(actor)
        
    
        self.__graphTab = UiDataAnlalysis.GraphTab()
        self.__gpsTab = UiDataAnlalysis.GpsTab()
        
        self.tabWidget = PyQt4.Qt.QTabWidget(self)
        self.tabWidget.addTab(self.__gpsTab,PyQt4.Qt.QIcon("gps.png"),"GPS TRACKING")
        self.tabWidget.addTab(self.__graphTab,PyQt4.Qt.QIcon("graph.jpg"),"ON FLIGHT STATS")
        self.tabWidget.setGeometry(20,15,500,300)
        self.tabWidget.show()
        
        PyQt4.QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
    
    
    def __AddMenu(self):
        
        self.menubar = MenuBar(self,"menubar")
        self.menubar.setGeometry(PyQt4.QtCore.QRect(0, 0, 800, 26))
        self.menuFile = Menu(self.menubar, "menuFile", "File")        
        self.menuView = Menu(self.menubar, "menuView", "View")
        self.menuConnection = Menu(self.menubar, "menuConnection", "Connection")
        self.menuGPS = Menu(self.menubar, "menuGPS", "GPS")           
        self.menuAbout = Menu(self.menubar, "menuAbout", "Help")
        self.setMenuBar(self.menubar)
    
    def __AddMenuAction(self):
        
        self.actionLoad_Log_File = MenuAction(self,"actionLoad_Log_File", "Load Log File")
        self.menuFile.addAction(self.actionLoad_Log_File)
        
        self.actionDisplay_Settings = MenuAction(self,"actionDisplay_Settings", "Display Settings")
        self.menuView.addAction(self.actionDisplay_Settings)
        
        self.actionSerial_Settings = MenuAction(self,"actionSerial_Settings", "Serial Settings")
        self.menuConnection.addAction(self.actionSerial_Settings)
        
        self.actionConnect = MenuAction(self,"actionConnect", "Connect")
        self.menuConnection.addAction(self.actionConnect)
        
        self.actionDisconnect = MenuAction(self,"actionDisconnect", "Disconnect")
        self.menuConnection.addAction(self.actionDisconnect)
        
        self.actionLaunchTerminal = MenuAction(self, "actionLaunchTerminal", "Launch Terminal")
        self.menuConnection.addAction(self.actionLaunchTerminal)
        
        self.actionSetLocalPosition = MenuAction(self, "actionSetLocalPosition", "Set base station position")
        self.menuGPS.addAction(self.actionSetLocalPosition)
        
        self.actionAbout = MenuAction(self,"actionAbout","About")
        self.menuAbout.addAction(self.actionAbout)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuGPS.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
    
    def __AddStatusBar(self):
        
        self.statusbar = PyQt4.QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.lblNotConnected = PyQt4.QtGui.QLabel("Not Connected")
        self.lblNotConnected.setStyleSheet('QLabel {color: red}')
        self.statusbar.addWidget(self.lblNotConnected)
        self.setStatusBar(self.statusbar)
    
    def __connectSlot(self):
        
        self.connect(self.actionSerial_Settings, PyQt4.QtCore.SIGNAL("triggered()"),self.__slotSerialSettings_Clicked)
        self.connect(self.actionAbout, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotAbout_Clicked)
        self.connect(self.actionConnect, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotConnect_Clicked)
        self.connect(self.actionDisconnect, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotDisconnect_Clicked)
        self.connect(self.actionLaunchTerminal, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotLaunchTerminal_Clicked)
        self.connect(self.actionSetLocalPosition, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotSetLocalPosition_Clicked)
        self.dataThread.isconnected.connect(self.updateStatusBar)
        self.dataThread.receivedata.connect(self.updateDashBoard)
        self.tabWidget.currentChanged.connect(self.__slotTab_Changed)
       
    def __slotAbout_Clicked(self):
        
        PyQt4.QtGui.QMessageBox.about(self, "About", "Base Station for RockETS 2015")
    
    def __slotSerialSettings_Clicked(self):
        
        self.__showSerialProperties()
        
    def __slotDisplaySettings_Clicked(self):
        pass
    
    def __slotLoadLogFile_Clicked(self):
        pass
    
    def __slotConnect_Clicked(self):
    
        self.dataThread.startCommunication()
        
        
    def __slotDisconnect_Clicked(self):
        
        self.dataThread.stopCommunication()
    
    def __slotLaunchTerminal_Clicked(self):
        
        self.terminal = terminal.embTerminal()
    
    def __slotSetLocalPosition_Clicked(self):
        
        self.__showGPSProperties()
        
    def __slotTab_Changed(self):
        
        if self.tabWidget.currentIndex() != 0:
            
            #self.resize(800, 650)
            self.tabWidget.setGeometry(20,15,750,350)
            
        else:
            
            self.tabWidget.setGeometry(20,15,500,300)
            #self.resize(800, 600)
    
    def __showSerialProperties(self):

        self.serialProperties = UiSerialProperties.SerialPropertiesWindow(self.serialConnection)
        self.serialProperties.show()
    
    def __showGPSProperties(self):

        self.gpsProperties = UiGpsSettings.GpsSettingWindow(self.__gpsTab.map)
        self.gpsProperties.show()
    
    def updateStatusBar(self, isConnected):
        
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
    
    def updateDashBoard(self,speed, accel, alti):
        
        self.__dashboard.updateValue(speed, accel, alti)        
    
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
        