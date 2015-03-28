# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python34\Lib\site-packages\PyQt4\uic\serialProperties.ui'
#
# Created: Sat Feb 28 14:48:15 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!
#erfew

from PyQt4 import QtCore, QtGui
from PyQt4.Qwt5 import Qwt
from serialIO import  SerialConnection #, SerialUtility
import sys
import math
import PyQt4
from PyQt4.Qt import QPen, QColor

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
        
        self.actionConnect_Settings = QtGui.QAction(self)
        self.actionConnect_Settings.setObjectName("actionConnect_Settings")
        self.actionConnect_Settings.setText("Connect")
        self.menuConnection.addAction(self.actionConnect_Settings)
        
        
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText("About")
        self.menuAbout.addAction(self.actionAbout)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        
        self.painter = QtGui.QPainter()
        
        self.__pitch = SpeedoMeter(self)
        self.__pitch.setGeometry(260,50,150,150)
               
        
        self.__roll = AttitudeIndicator(self)
        self.__roll.setGeometry(420,50,150,150)

        self.__yaw = AttitudeIndicator(self)
        self.__yaw.setGeometry(580,50,150,150)
        
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
        
    def __connectSlot(self):
        
        self.connect(self.actionSerial_Settings, QtCore.SIGNAL("triggered()"),self.__slotSerialSettings_Clicked)
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.__slotAbout_Clicked)
       
    def __slotAbout_Clicked(self):
        
        QtGui.QMessageBox.about(self, "About", "Base Station for RockETS 2015")
    
    def __slotSerialSettings_Clicked(self):
        
        self.__showSerialProperties()
        
    def __slotDisplaySettings_Clicked(self):
        pass
    
    def __slotLoadLogFile_Clicked(self):
        pass
    
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
        self.comboCOMPort.addItems("COM 1")#SerialUtility.ListComPort())
        
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
        self.txtBaudRate.setText(self.serialConnection._baudRate)
        
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
        
        
        self.serialConnection._baudRate = self.txtBaudRate.text()
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
        self.__label = 'km/h'
        self.setWrapping(False)
        self.setReadOnly(True)

        self.setOrigin(135.0)
        self.setScaleArc(0.0, 270.0)
        self.setSizeIncrement(0, 1000)
        
        
        
        self.setNeedle(Qwt.QwtDialSimpleNeedle(
            Qwt.QwtDialSimpleNeedle.Arrow,
            True,
            QtGui.QColor(QtGui.QColor.red),
            QtGui.QColor(QtGui.QColor.blue).light(130)))

        self.setScaleOptions(Qwt.QwtDial.ScaleTicks | Qwt.QwtDial.ScaleLabel)
        self.setScale(0,10,100)
        self.setScaleTicks(2, 4, 8)

    # __init__()
    
    def setLabel(self, text):
        self.__label = text
        self.update()

    # setLabel()
    
    def label(self):
        return self.__label

    # label()
    
    def drawScaleContents(self, painter, center, radius):
        
        painter.setPen(QPen(QColor(245,245,245), 3))
        rect = QtCore.QRect(50, 0, 2 * radius, 2 * radius - 10)
        rect.moveCenter(center)
        painter.setPen(self.palette().color(QtGui.QPalette.Text))
        painter.drawText(
            rect, QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter, self.__label)


if __name__ == "__main__":
    
    app = baseStationApplication(sys.argv)

