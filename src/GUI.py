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
from PyQt4.Qt import QPen, QColor, QIcon, QStringList, QPalette
from MapWidget import MapnikWidget
import serial.tools.list_ports
from PyQt4.QtGui import QLCDNumber


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
        
        self.lblPalette = QPalette()
        self.lblPalette.setColor(palette.WindowText,QtGui.QColor(255,255,255))
        
        self.lblSpeed = QtGui.QLabel(self)
        self.lblSpeed.setText("SPEED")
        self.lblSpeed.setPalette(self.lblPalette)
        self.lblSpeed.setGeometry(100, 15, 60,20)
        self.lblSpeed.show()
        
        self.lblAltitude = QtGui.QLabel(self)
        self.lblAltitude.setText("ALTITUDE")
        self.lblAltitude.setPalette(self.lblPalette)
        self.lblAltitude.setGeometry(230, 15, 70,20)
        self.lblAltitude.show()
        
        self.lblAccel = QtGui.QLabel(self)
        self.lblAccel.setText("ACCELERATION")
        self.lblAccel.setPalette(self.lblPalette)
        self.lblAccel.setGeometry(350, 15, 120,20)
        self.lblAccel.show()
        
        self.lblPeak = QtGui.QLabel(self)
        self.lblPeak.setText("PEAK REACHED")
        self.lblPeak.setPalette(self.lblPalette)
        self.lblPeak.setGeometry(585,25,120,20)
        
        self.lcdPalette = QPalette()    
        self.lcdPalette.setColor(palette.WindowText, QtGui.QColor(0, 255, 0))
        
        self.lcdVitesse = QLCDNumber(self)
        self.lcdVitesse.setPalette(self.lcdPalette)
        self.lcdVitesse.setGeometry(75, 180, 100, 30)
        self.lcdVitesse.show()
        
        self.lcdAltitude = QLCDNumber(self)
        self.lcdAltitude.setPalette(self.lcdPalette)
        self.lcdAltitude.setGeometry(215, 180, 100, 30)
        self.lcdAltitude.show()
        
        self.lcdAltitude = QLCDNumber(self)
        self.lcdAltitude.setPalette(self.lcdPalette)
        self.lcdAltitude.setGeometry(355, 180, 100, 30)
        self.lcdAltitude.show()
        
        self.__speed = SpeedoMeter(self)
        self.__speed.setLabel("MPH")
        self.__speed.setDialRange(0.0, 700.0)
        self.__speed.setDialScale(0, 10, 100)
        self.__speed.setGeometry(60,40,130,130)
        
        self.__altitude = SpeedoMeter(self)
        self.__altitude.setLabel("METERS")
        self.__altitude.setDialRange(0.0, 9000.0)
        self.__altitude.setDialScale(0, 5,1500)
        self.__altitude.setGeometry(200,40,130,130) 
        
        self.__accel = SpeedoMeter(self)
        self.__accel.setLabel("M/S2")
        self.__accel.setDialRange(0.0, 150.0)
        self.__accel.setDialScale(0, 10, 50)
        self.__accel.setGeometry(340,40,130,130) 
        
        self.__compass = Qwt.QwtCompass(self)
        self.rose = Qwt.QwtSimpleCompassRose(16,2)
        self.rose.setWidth(0.15)
        self.__compass.setRose(self.rose)
        self.__compass.setGeometry(600,410,140,140)
        self.__compass.show()
        
        self.peakLED = KLed(self)
        self.peakLED.setColor(QtGui.QColor(255,0,0))
        self.peakLED.setGeometry(550,20,30,30)
        self.peakLED.show()
        
        self.map = MapnikWidget(self)
        self.map.setGeometry(20,230,400,300)
        self.map.open("world_style.xml")
        
        self.testgraph = Qwt.QwtPlot(self)

        
        self.tabWidget = PyQt4.Qt.QTabWidget(self)
        self.tabWidget.addTab(self.map,QIcon("gps.png"),"GPS TRACKING")
        self.tabWidget.addTab(self.testgraph,QIcon("graph.jpg"),"ON FLIGHT STATS")
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
        
            self.tabWidget.setGeometry(20,250,600,300)
            
        else:
            
            self.tabWidget.setGeometry(20,250,500,300)
    
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
    

class AttitudeIndicator(Qwt.QwtDial):

    def __init__(self, *args):
        Qwt.QwtDial.__init__(self, *args)
        self.__gradient = 0.0
        self.setMode(Qwt.QwtDial.RotateScale)
        self.setWrapping(True)
        self.setOrigin(270.0)
        self.setScaleOptions(Qwt.QwtDial.ScaleTicks)
        self.setScale(0, 0, 30.0)
        self.setNeedle(AttitudeIndicatorNeedle(
            self.palette().color(QtGui.QPalette.Text)))

    # __init__()

    def angle(self):
        return self.value()

    # angle()
    
    def setAngle(self, angle):
        self.setValue(angle)

    # setAngle()

    def gradient(self):
        return self.__gradient

    # gradient()

    def setGradient(self, gradient):
        self.__gradient = gradient

    # setGradient()
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Plus:
            self.setGradient(self.gradient() + 0.05)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.setGradient(self.gradient() - 0.05)
        else:
            Qwt.QwtDial.keyPressEvent(self, event)

    # keyPressEvent()

    def drawScale(self, painter, center, radius, origin, minArc, maxArc):
        dir = (360.0 - origin) * math.pi / 180.0
        offset = 4
        p0 = Qwt.qwtPolar2Pos(center, offset, dir + math.pi)

        w = self.contentsRect().width()

        # clip region to swallow 180 - 360 degrees
        pa = []
        pa.append(Qwt.qwtPolar2Pos(p0, w, dir - math.pi/2))
        pa.append(Qwt.qwtPolar2Pos(pa[-1], 2 * w, dir + math.pi/2))
        pa.append(Qwt.qwtPolar2Pos(pa[-1], w, dir))
        pa.append(Qwt.qwtPolar2Pos(pa[-1], 2 * w, dir - math.pi/2))

        painter.save()
        painter.setClipRegion(QtGui.QRegion(QtGui.QPolygon(pa)))
        Qwt.QwtDial.drawScale(
            self, painter, center, radius, origin, minArc, maxArc)
        painter.restore()

    # drawScale()
    
    def drawScaleContents(self, painter, center, radius):
        dir = 360 - int(round(self.origin() - self.value()))
        arc = 90 + int(round(self.gradient() * 90))
        skyColor = QtGui.QColor(38, 151, 221)
        painter.save()
        painter.setBrush(skyColor)
        painter.drawChord(
            self.scaleContentsRect(), (dir - arc)*16, 2*arc*16)
        painter.restore()

class AttitudeIndicatorNeedle(Qwt.QwtDialNeedle):

    def __init__(self, color):
        Qwt.QwtDialNeedle.__init__(self)
        palette = QtGui.QPalette()
        #for colourGroup in QtGui.QColor.colorNames():
        #   palette.setColor(colourGroup, QtGui.QPalette.Text, color)
        #self.setPalette(palette)

    # __init__()
    
    def draw(self, painter, center, length, direction, cg):
        direction *= math.pi / 180.0
        triangleSize = int(round(length * 0.1))

        painter.save()

        p0 = QtCore.QPoint(center.x() + 1, center.y() + 1)
        p1 = Qwt.qwtPolar2Pos(p0, length - 2 * triangleSize - 2, direction)

        pa = QtGui.QPolygon([
            Qwt.qwtPolar2Pos(p1, 2 * triangleSize, direction),
            Qwt.qwtPolar2Pos(p1, triangleSize, direction + math.pi/2),
            Qwt.qwtPolar2Pos(p1, triangleSize, direction - math.pi/2),
            ])

        color = self.palette().color(cg, QtGui.QPalette.Text)
        painter.setBrush(color)
        painter.drawPolygon(pa)

        painter.setPen(QtGui.QPen(color, 3))
        painter.drawLine(
            Qwt.qwtPolar2Pos(p0, length - 2, direction + math.pi/2),
            Qwt.qwtPolar2Pos(p0, length - 2, direction - math.pi/2))

        painter.restore()

class SpeedoMeter(Qwt.QwtDial):

    def __init__(self, *args):
        Qwt.QwtDial.__init__(self, *args)
        #self.__label = "KM/H"
        self.setWrapping(False)
        self.setReadOnly(True)
        self.setOrigin(135.0)
        self.setScaleArc(0.0, 270.0)
        #self.setSizeIncrement(0, 1000)
        
        
        self.setNeedle(Qwt.QwtDialSimpleNeedle(
            Qwt.QwtDialSimpleNeedle.Arrow,
            True,
            QtGui.QColor(QtGui.QColor.red),
            QtGui.QColor(QtGui.QColor.blue).light(130)))

        self.setScaleOptions(Qwt.QwtDial.ScaleTicks | Qwt.QwtDial.ScaleLabel)
        #self.setScale(0,10,1000)
        #self.setScaleTicks(2, 4, 8)

    
    def setLabel(self, text):
        self.__label = text
        self.update()

    
    def label(self):
        return self.__label

    def setDialRange(self, minValue, maxValue):
        self.setRange(minValue, maxValue)
    
    def setDialScale(self, minValue, midValue, maxValue):
        self.setScale(minValue, midValue, maxValue)
            
    def drawScaleContents(self, painter, center, radius):
        
        painter.setPen(QPen(QColor(245,245,245), 3))
        rect = QtCore.QRect(50, 0, 2 * radius, 2 * radius - 10)
        rect.moveCenter(center)
        painter.setPen(self.palette().color(QtGui.QPalette.Text))
        painter.drawText(
            rect, QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter, self.__label)
