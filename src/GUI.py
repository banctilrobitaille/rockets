# -*- coding: utf-8 -*-

import UiMainWindow
from PyQt4 import QtCore, QtGui
from PyQt4.Qwt5 import Qwt
from serialIO import  SerialConnection
import PyQt4
from PyQt4.Qt import QIcon, QFont
from MapWidget import MapnikWidget
import serial.tools.list_ports
import dashboard
import compass
import led


class baseStationApplication(QtGui.QApplication):
        
    def __init__(self, args):
        
        QtGui.QApplication.__init__(self, args)
        self.serialConnection = SerialConnection()
        self.mainWindow = UiMainWindow.MainWindow(self.serialConnection)
        self.mainWindow.show()
        self.exec_()
        

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
    
