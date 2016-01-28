import PyQt4
import dashboard
import compass
import UiDataAnlalysis
import UiSerialProperties
import vtkRendering
import vtk
import UiGpsSettings
from PyQt4.Qt import pyqtSlot

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

    def __init__(self,serialConnection,parent=None):
        
        PyQt4.QtGui.QMainWindow.__init__(self, parent)
        self.__setupUi()

    """
    #    Methode __setupUi
    #    Description: Methode initialisant les composants graphiques
    #                 de la fenetre et les positionne.
    #
    #    param:  None
    #    return: None
    """ 
    
    @pyqtSlot(int)
    def on_baudrateChanged(self,baudrate):
        print baudrate
        
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
        
        """Ajout de la barre de menu"""
        self.__AddMenu()
        """Ajout des actions lies differents menus"""
        self.__AddMenuAction()
        """Ajout de la barre de status"""
        self.__AddStatusBar()
        
        self.__dashboard = dashboard.Dashboard(self)
        self.__compass = compass.Compass(self)
        self.__rocket = vtkRendering.rocketRendering(self)
        
        self.ren = vtk.vtkRenderer()
        self.__rocket.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.__rocket.vtkWidget.GetRenderWindow().GetInteractor()
 
        self.reader = vtk.vtkSTLReader()
        self.reader.SetFileName("VTK_Files/original.stl")
 
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
        self.tabWidget.addTab(self.__gpsTab,PyQt4.Qt.QIcon("Image_Files/gps.png"),"GPS TRACKING")
        self.tabWidget.addTab(self.__graphTab,PyQt4.Qt.QIcon("Image_Files/graph.jpg"),"ON FLIGHT STATS")
        self.tabWidget.setGeometry(20,15,500,300)
        self.tabWidget.show()
        
        PyQt4.QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
    
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
        self.actionSerial_Settings = MenuAction(self,"actionSerial_Settings", "Serial Settings")
        self.menuConnection.addAction(self.actionSerial_Settings)
        
        """Initialisaiton et ajout du sous menu <Connect>"""
        self.actionConnect = MenuAction(self,"actionConnect", "Connect")
        self.menuConnection.addAction(self.actionConnect)
        
        """Initialisaiton et ajout du sous menu <Disconnect>"""
        self.actionDisconnect = MenuAction(self,"actionDisconnect", "Disconnect")
        self.menuConnection.addAction(self.actionDisconnect)
        
        """Initialisaiton et ajout du sous menu <Launch Terminal>"""
        self.actionLaunchTerminal = MenuAction(self, "actionLaunchTerminal", "Launch Terminal")
        self.menuConnection.addAction(self.actionLaunchTerminal)
        
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
    
    """
    #    Methode __connectSlot
    #    Description: Methode qui associe les actions (menus) a une methode
    #
    #    param:  None
    #    return: None
    """ 
    def __connectSlot(self):
        
        self.connect(self.actionSerial_Settings, PyQt4.QtCore.SIGNAL("triggered()"),self.__slotSerialSettings_Clicked)
        self.connect(self.actionAbout, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotAbout_Clicked)
        self.connect(self.actionConnect, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotConnect_Clicked)
        self.connect(self.actionDisconnect, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotDisconnect_Clicked)
        self.connect(self.actionLaunchTerminal, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotLaunchTerminal_Clicked)
        self.connect(self.actionSetLocalPosition, PyQt4.QtCore.SIGNAL("triggered()"), self.__slotSetLocalPosition_Clicked)
        
        """Association entre le signal leve lors du changement detat de la connexion serie et la methode
        updateStatusBar qui met a jour letat de la connexion affiche dans la 
        barre detat"""
        #self.dataThread.isconnected.connect(self.updateStatusBar)
        
        """"Association entre le signal leve lors de la reception de donnees et la methode
        updateDashBoard qui met a jour laffichage real time des donnees de vol"""
        #self.dataThread.receivedata.connect(self.updateDashBoard)
        
        """Association entre un changement de tab du widget tabWidget et la methode
        __slotTab_Changed qui redimensionne le tabWidget"""
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
        
        pass
        #self.terminal = terminal.embTerminal()
    
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
        