# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python34\Lib\site-packages\PyQt4\uic\serialProperties.ui'
#
# Created: Sat Feb 28 14:48:15 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!


from PyQt4 import QtCore, QtGui
from PyQt4.Qwt5 import Qwt
from serialIO import  SerialConnection, SerialUtility
import sys
import math
import PyQt4
from PyQt4.Qt import QPen, QColor, QIcon, QStringList, QPalette, QFont
from MapWidget import MapnikWidget
import serial.tools.list_ports
from PyQt4.QtGui import QLCDNumber
from PyKDE4.kdeui import KLed
import dashboard
import compass
import led


class baseStationApplication(QtGui.QApplication):
        
    def __init__(self, args):
        
        QtGui.QApplication.__init__(self, args)
        self.serialConnection = SerialConnection()
        self.mainWindow = Ui_MainWindow(self.serialConnection)
        self.mainWindow.show()
        self.exec_()
        
    
class Ui_MainWindow(QtGui.QMainWindow):

    def __init__(self,serialConnection,parent=None):
        
        QtGui.QMainWindow.__init__(self, parent)
        self.serialConnection = serialConnection
        self.__setupUi()
        
    def __setupUi(self):
        
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.setMouseTracking(False)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
        self.setPalette(palette)
        self.setWindowTitle("Station de Base RockETS v0.1")
        
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")
        
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuView.setTitle("View")
        

        self.menuConnection = QtGui.QMenu(self.menubar)
        self.menuConnection.setObjectName("menuConnection")
        self.menuConnection.setTitle("Connection")
        
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuAbout.setTitle("Help")
        
        self.setMenuBar(self.menubar)
        
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.lblNotConnected = QtGui.QLabel("Not Connected")
        self.lblNotConnected.setStyleSheet('QLabel {color: red}')
        self.statusbar.addWidget(self.lblNotConnected)
        self.setStatusBar(self.statusbar)
        
        self.actionLoad_Log_File = QtGui.QAction(self)
        self.actionLoad_Log_File.setObjectName("actionLoad_Log_File")
        self.actionLoad_Log_File.setText("Load Log File")
        self.menuFile.addAction(self.actionLoad_Log_File)
        
        self.actionDisplay_Settings = QtGui.QAction(self)
        self.actionDisplay_Settings.setObjectName("actionDisplay_Settings")
        self.actionDisplay_Settings.setText("Display Settings")
        self.menuView.addAction(self.actionDisplay_Settings)
        
        self.actionSerial_Settings = QtGui.QAction(self)
        self.actionSerial_Settings.setObjectName("actionSerial_Settings")
        self.actionSerial_Settings.setText("Serial Settings")
        self.menuConnection.addAction(self.actionSerial_Settings)
        
        self.actionConnect = QtGui.QAction(self)
        self.actionConnect.setObjectName("actionConnect")
        self.actionConnect.setText("Connect")
        self.menuConnection.addAction(self.actionConnect)
        
        
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText("About")
        self.menuAbout.addAction(self.actionAbout)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        
                
        self.painter = QtGui.QPainter()
        
        self.__dashboard = dashboard.Dashboard(self)
        self.__compass = compass.Compass(self)
        self.__led = led.Led(self)
        
        self.map = MapnikWidget(self)
        self.map.setGeometry(20,230,400,300)
        self.map.open("world_style.xml")
        
        self.statFrame = QtGui.QFrame()
        self.gridLayout = QtGui.QGridLayout()
        self.plotTitleFont = QFont("Helvetica", 11)
        self.plotAxisFont = QFont("Helvetica", 8)
        
        self.speedPlot = Qwt.QwtPlot()
        self.speedTitle = Qwt.QwtText("Speed over Time")
        self.speedTitle.setFont(self.plotTitleFont)
        self.speedPlot.setTitle(self.speedTitle)
        self.speedPlot.setAxisTitle(0, "Speed(MPH)")
        self.speedPlot.setAxisTitle(2, "Time(SEC)")
        
        self.accelPlot = Qwt.QwtPlot()
        self.accelTitle = Qwt.QwtText("Acceleration Over Time")
        self.accelTitle.setFont(self.plotTitleFont)
        self.accelPlot.setTitle(self.accelTitle)
        self.accelPlot.setAxisTitle(0, "Acceleration(MS2)")
        self.accelPlot.setAxisTitle(2, "Time(SEC)")
        
        self.altitudePlot = Qwt.QwtPlot()
        self.altitudePlot.setTitle("Altitude over Time")
        self.altitudePlot.setAxisTitle(0, "Altitude(x1000'')")
        self.altitudePlot.setAxisTitle(2, "Time(SEC)")
        
        self.temperaturePlot = Qwt.QwtPlot()
        self.temperaturePlot.setTitle("Temperature over Time")
        self.temperaturePlot.setAxisTitle(0, "Temperature(KELVIN)")
        self.temperaturePlot.setAxisTitle(2, "Time(SEC)")
        
        self.gridLayout.addWidget(self.speedPlot, 0,0)
        self.gridLayout.addWidget(self.accelPlot, 0,1)
        self.gridLayout.addWidget(self.altitudePlot, 1,0)
        self.gridLayout.addWidget(self.temperaturePlot, 1,1)
        
        self.statFrame.setLayout(self.gridLayout)

        
        self.tabWidget = PyQt4.Qt.QTabWidget(self)
        self.tabWidget.addTab(self.map,QIcon("gps.png"),"GPS TRACKING")
        self.tabWidget.addTab(self.statFrame,QIcon("graph.jpg"),"ON FLIGHT STATS")
        self.tabWidget.setGeometry(20,250,500,300)
        self.tabWidget.show()
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
        
    def __connectSlot(self):
        
        self.connect(self.actionSerial_Settings, QtCore.SIGNAL("triggered()"),self.__slotSerialSettings_Clicked)
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.__slotAbout_Clicked)
        self.connect(self.actionConnect, QtCore.SIGNAL("triggered()"), self.__slotConnect_Clicked)
        self.tabWidget.currentChanged.connect(self.__slotTab_Changed)
       
    def __slotAbout_Clicked(self):
        
        QtGui.QMessageBox.about(self, "About", "Base Station for RockETS 2015")
    
    def __slotSerialSettings_Clicked(self):
        
        self.__showSerialProperties()
        
    def __slotDisplaySettings_Clicked(self):
        pass
    
    def __slotLoadLogFile_Clicked(self):
        pass
    
    def __slotConnect_Clicked(self):
        
        pass
    
    def __slotTab_Changed(self):
        
       # QtGui.QMessageBox.about(self, "About", )
        
        if self.tabWidget.currentIndex() != 0:
            
            self.resize(800, 650)
            #self.__compass.setGeometry(900,710,140,140)
            self.tabWidget.setGeometry(20,250,750,350)
            
        else:
            
            self.tabWidget.setGeometry(20,250,500,300)
            #self.__compass.setGeometry(600,410,140,140)
            self.resize(800, 600)
    
    def __showSerialProperties(self):
        
        self.serialProperties = Ui_frmSerialProperties(self.serialConnection)
        self.serialProperties.show()
        

class Ui_frmSerialProperties(QtGui.QWidget):
    
    def __init__(self,serialConnection,parent=None):
        
        QtGui.QWidget.__init__(self, parent)
        self.serialConnection = serialConnection
        self.__setupUi()
    
    def __setupUi(self):
        
        self.setObjectName("frmSerialProperties")
        self.setFixedSize(447, 192)
        self.setWindowTitle("Serial Connection Properties")
        
        self.btnCancel = QtGui.QPushButton(self)
        self.btnCancel.setGeometry(QtCore.QRect(320, 150, 93, 28))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setText("Cancel")
        
        self.btnSave = QtGui.QPushButton(self)
        self.btnSave.setGeometry(QtCore.QRect(210, 150, 93, 28))
        self.btnSave.setObjectName("btnSave")
        self.btnSave.setText("Save")
        
        self.gbConfig = QtGui.QGroupBox(self)
        self.gbConfig.setGeometry(QtCore.QRect(10, 10, 431, 131))
        self.gbConfig.setObjectName("gbConfig")
        self.gbConfig.setTitle("Serial Properties")
        
        self.comboCOMPort = QtGui.QComboBox(self.gbConfig)
        self.comboCOMPort.setGeometry(QtCore.QRect(190, 20, 191, 31))
        self.comboCOMPort.setObjectName("comboCOMPort")
        
        for port in serial.tools.list_ports.comports():
            self.comboCOMPort.addItem(str(port))#SerialUtility.ListComPort())
        self.lblListePort = QtGui.QLabel(self.gbConfig)
        self.lblListePort.setGeometry(QtCore.QRect(30, 20, 121, 20))
        self.lblListePort.setObjectName("lblListePort")
        self.lblListePort.setText("COM Port List")
        
        self.lblParity = QtGui.QLabel(self.gbConfig)
        self.lblParity.setGeometry(QtCore.QRect(30, 50, 41, 16))
        self.lblParity.setObjectName("lblParity")
        self.lblParity.setText("Parity:")
        
        self.checkYes = QtGui.QCheckBox(self.gbConfig)
        self.checkYes.setGeometry(QtCore.QRect(70, 50, 51, 20))
        self.checkYes.setObjectName("checkYes")
        self.checkYes.setText("Yes")
        
        self.checkNo = QtGui.QCheckBox(self.gbConfig)
        self.checkNo.setGeometry(QtCore.QRect(130, 50, 51, 20))
        self.checkNo.setObjectName("checkNo")
        self.checkNo.setText("No")
    
        if self.serialConnection._parity:
            self.checkYes.setChecked(self.serialConnection._parity)
        else:
            self.checkNo.setChecked(not self.serialConnection._parity)
        
        self.lblBaudRate = QtGui.QLabel(self.gbConfig)
        self.lblBaudRate.setGeometry(QtCore.QRect(7, 90, 71, 20))
        self.lblBaudRate.setObjectName("lblBaudRate")
        self.lblBaudRate.setText("BaudRate:")
        
        self.txtBaudRate = QtGui.QLineEdit(self.gbConfig)
        self.txtBaudRate.setGeometry(QtCore.QRect(100, 90, 100, 22))
        self.txtBaudRate.setObjectName("txtBaudRate")
        self.txtBaudRate.setText(str(self.serialConnection._baudRate))
        
        self.lblStopBits = QtGui.QLabel(self.gbConfig)
        self.lblStopBits.setGeometry(QtCore.QRect(220, 90, 60, 22))
        self.lblStopBits.setObjectName("lblStopBits")
        self.lblStopBits.setText("StopBits:")
        
        self.txtStopBits = QtGui.QLineEdit(self.gbConfig)
        self.txtStopBits.setGeometry(QtCore.QRect(280, 90, 31, 22))
        self.txtStopBits.setObjectName("txtStopBits")
        self.txtStopBits.setText(self.serialConnection._stopBits)
        
        self.lblDataBits = QtGui.QLabel(self.gbConfig)
        self.lblDataBits.setGeometry(QtCore.QRect(320, 90, 60, 22))
        self.lblDataBits.setObjectName("lblDataBits")
        self.lblDataBits.setText("DataBits:")
        
        self.txtDataBits = QtGui.QLineEdit(self.gbConfig)
        self.txtDataBits.setGeometry(QtCore.QRect(380, 90, 41, 22))
        self.txtDataBits.setObjectName("txtDataBits")
        self.txtDataBits.setText(self.serialConnection._dataBits)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
        
    def __connectSlot(self):
        
        self.connect(self.btnCancel, QtCore.SIGNAL("clicked()"), self.__slotBtnCancel_Clicked)
        self.connect(self.btnSave, QtCore.SIGNAL("clicked()"), self.__slotBtnSave_Clicked)
    
    def __slotBtnSave_Clicked(self):
        
        
        self.serialConnection._baudRate = int(self.txtBaudRate.text())
        self.serialConnection._dataBits = self.txtDataBits.text()
        self.serialConnection._stopBits = self.txtStopBits.text()
        
        if self.checkYes.isChecked():
            self.serialConnection._parity = True
        else:
            self.serialConnection._parity = False
        
        self.close()
    
    def __slotBtnCancel_Clicked(self):
        self.close()
    
