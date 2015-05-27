import PyQt4.Qwt5
from MapWidget import MapnikWidget
import dashboard
import compass
import led
import UiDataAnlalysis

class MainWindow(PyQt4.QtGui.QMainWindow):

    def __init__(self,serialConnection,parent=None):
        
        PyQt4.QtGui.QMainWindow.__init__(self, parent)
        self.serialConnection = serialConnection
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
        self.__led = led.Led(self)
    
        self.__graphTab = UiDataAnlalysis.GraphTab()
        self.__gpsTab = UiDataAnlalysis.GpsTab()
        
        self.tabWidget = PyQt4.Qt.QTabWidget(self)
        self.tabWidget.addTab(self.__gpsTab,PyQt4.Qt.QIcon("gps.png"),"GPS TRACKING")
        self.tabWidget.addTab(self.__graphTab,PyQt4.Qt.QIcon("graph.jpg"),"ON FLIGHT STATS")
        self.tabWidget.setGeometry(20,250,500,300)
        self.tabWidget.show()
        
        PyQt4.QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
    
    
    def __AddMenu(self):
        
        self.menubar = MenuBar(self,"menubar")
        self.menubar.setGeometry(PyQt4.QtCore.QRect(0, 0, 800, 26))
        self.menuFile = Menu(self.menubar, "menuFile", "File")        
        self.menuView = Menu(self.menubar, "menuView", "View")
        self.menuConnection = Menu(self.menubar, "menuConnection", "Connection")        
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
        
        self.actionAbout = MenuAction(self,"actionAbout","About")
        self.menuAbout.addAction(self.actionAbout)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuConnection.menuAction())
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
        
        pass
    
    def __slotTab_Changed(self):
        
        if self.tabWidget.currentIndex() != 0:
            
            self.resize(800, 650)
            self.tabWidget.setGeometry(20,250,750,350)
            
        else:
            
            self.tabWidget.setGeometry(20,250,500,300)
            self.resize(800, 600)
    
    def __showSerialProperties(self):
        pass
       # self.serialProperties = Ui_frmSerialProperties(self.serialConnection)
       # self.serialProperties.show()


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
        