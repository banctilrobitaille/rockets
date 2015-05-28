import PyQt4
import serial.tools

class SerialPropertiesWindow(PyQt4.QtGui.QWidget):
    
    def __init__(self,serialConnection,parent=None):
        
        PyQt4.QtGui.QWidget.__init__(self, parent)
        self.serialConnection = serialConnection
        self.__setupUi()
    
    def __setupUi(self):
        
        self.setObjectName("frmSerialProperties")
        self.setFixedSize(447, 192)
        self.setWindowTitle("Serial Connection Properties")
        
        self.btnCancel = PyQt4.QtGui.QPushButton(self)
        self.btnCancel.setGeometry(PyQt4.QtCore.QRect(320, 150, 93, 28))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setText("Cancel")
        
        self.btnSave = PyQt4.QtGui.QPushButton(self)
        self.btnSave.setGeometry(PyQt4.QtCore.QRect(210, 150, 93, 28))
        self.btnSave.setObjectName("btnSave")
        self.btnSave.setText("Save")
        
        self.gbConfig = PyQt4.QtGui.QGroupBox(self)
        self.gbConfig.setGeometry(PyQt4.QtCore.QRect(10, 10, 431, 131))
        self.gbConfig.setObjectName("gbConfig")
        self.gbConfig.setTitle("Serial Properties")
        
        self.comboCOMPort = PyQt4.QtGui.QComboBox(self.gbConfig)
        self.comboCOMPort.setGeometry(PyQt4.QtCore.QRect(190, 20, 191, 31))
        self.comboCOMPort.setObjectName("comboCOMPort")
        
        for port in serial.tools.list_ports.comports():
            self.comboCOMPort.addItem(str(port))#SerialUtility.ListComPort())

        self.lblListePort = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblListePort.setGeometry(PyQt4.QtCore.QRect(30, 20, 121, 20))
        self.lblListePort.setObjectName("lblListePort")
        self.lblListePort.setText("COM Port List")
        
        self.lblParity = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblParity.setGeometry(PyQt4.QtCore.QRect(30, 50, 41, 16))
        self.lblParity.setObjectName("lblParity")
        self.lblParity.setText("Parity:")
        
        self.checkYes = PyQt4.QtGui.QCheckBox(self.gbConfig)
        self.checkYes.setGeometry(PyQt4.QtCore.QRect(70, 50, 51, 20))
        self.checkYes.setObjectName("checkYes")
        self.checkYes.setText("Yes")
        
        self.checkNo = PyQt4.QtGui.QCheckBox(self.gbConfig)
        self.checkNo.setGeometry(PyQt4.QtCore.QRect(130, 50, 51, 20))
        self.checkNo.setObjectName("checkNo")
        self.checkNo.setText("No")
    
        if self.serialConnection._parity:
            self.checkYes.setChecked(self.serialConnection._parity)
        else:
            self.checkNo.setChecked(not self.serialConnection._parity)
        
        self.lblBaudRate = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblBaudRate.setGeometry(PyQt4.QtCore.QRect(7, 90, 71, 20))
        self.lblBaudRate.setObjectName("lblBaudRate")
        self.lblBaudRate.setText("BaudRate:")
        
        self.txtBaudRate = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtBaudRate.setGeometry(PyQt4.QtCore.QRect(100, 90, 100, 22))
        self.txtBaudRate.setObjectName("txtBaudRate")
        self.txtBaudRate.setText(str(self.serialConnection._baudRate))
        
        self.lblStopBits = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblStopBits.setGeometry(PyQt4.QtCore.QRect(220, 90, 60, 22))
        self.lblStopBits.setObjectName("lblStopBits")
        self.lblStopBits.setText("StopBits:")
        
        self.txtStopBits = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtStopBits.setGeometry(PyQt4.QtCore.QRect(280, 90, 31, 22))
        self.txtStopBits.setObjectName("txtStopBits")
        self.txtStopBits.setText(self.serialConnection._stopBits)
        
        self.lblDataBits = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblDataBits.setGeometry(PyQt4.QtCore.QRect(320, 90, 60, 22))
        self.lblDataBits.setObjectName("lblDataBits")
        self.lblDataBits.setText("DataBits:")
        
        self.txtDataBits = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtDataBits.setGeometry(PyQt4.QtCore.QRect(380, 90, 41, 22))
        self.txtDataBits.setObjectName("txtDataBits")
        self.txtDataBits.setText(self.serialConnection._dataBits)

        PyQt4.QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
        
    def __connectSlot(self):
        
        self.connect(self.btnCancel, PyQt4.QtCore.SIGNAL("clicked()"), self.__slotBtnCancel_Clicked)
        self.connect(self.btnSave, PyQt4.QtCore.SIGNAL("clicked()"), self.__slotBtnSave_Clicked)
    
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
    