import PyQt4
import serial

class SerialPropertiesWindow(PyQt4.QtGui.QWidget):
    
    def __init__(self,rfdController,parent=None):
        
        PyQt4.QtGui.QWidget.__init__(self, parent)
        self.__rfdController = rfdController
        self.__serialConnection = self.__rfdController.serialConnection
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
        
        self.comboCOMPort.addItem("/dev/ttyS0")

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
        self.checkYes.setAutoExclusive(True)
        
        self.checkNo = PyQt4.QtGui.QCheckBox(self.gbConfig)
        self.checkNo.setGeometry(PyQt4.QtCore.QRect(130, 50, 51, 20))
        self.checkNo.setObjectName("checkNo")
        self.checkNo.setText("No")
        self.checkNo.setAutoExclusive(True)
    
        if self.__serialConnection._parity != serial.PARITY_NONE:
            self.checkYes.setChecked(True)
        else:
            self.checkNo.setChecked(True)
        
        self.lblBaudRate = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblBaudRate.setGeometry(PyQt4.QtCore.QRect(7, 90, 71, 20))
        self.lblBaudRate.setObjectName("lblBaudRate")
        self.lblBaudRate.setText("BaudRate:")
        
        self.txtBaudRate = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtBaudRate.setGeometry(PyQt4.QtCore.QRect(100, 90, 100, 22))
        self.txtBaudRate.setObjectName("txtBaudRate")
        self.txtBaudRate.setText(str(self.__serialConnection._baudrate))
        
        self.lblStopBits = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblStopBits.setGeometry(PyQt4.QtCore.QRect(220, 90, 60, 22))
        self.lblStopBits.setObjectName("lblStopBits")
        self.lblStopBits.setText("StopBits:")
        
        self.txtStopBits = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtStopBits.setGeometry(PyQt4.QtCore.QRect(280, 90, 31, 22))
        self.txtStopBits.setObjectName("txtStopBits")
        self.txtStopBits.setText(str(self.__serialConnection._stopbits))
        
        self.lblDataBits = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblDataBits.setGeometry(PyQt4.QtCore.QRect(320, 90, 60, 22))
        self.lblDataBits.setObjectName("lblDataBits")
        self.lblDataBits.setText("DataBits:")
        
        self.txtDataBits = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtDataBits.setGeometry(PyQt4.QtCore.QRect(380, 90, 41, 22))
        self.txtDataBits.setObjectName("txtDataBits")
        self.txtDataBits.setText(str(self.__serialConnection._bytesize))

        PyQt4.QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
        
    def __connectSlot(self):
        
        self.connect(self.btnCancel, PyQt4.QtCore.SIGNAL("clicked()"), self.__slotBtnCancel_Clicked)
        self.connect(self.btnSave, PyQt4.QtCore.SIGNAL("clicked()"), self.__slotBtnSave_Clicked)
    
    def __slotBtnSave_Clicked(self):
        
        
        self.__rfdController.updateSerialConnectionBaudrate(int(self.txtBaudRate.text())) 
        self.__rfdController.updateSerialConnectionByteSize(int(self.txtDataBits.text()))
        self.__rfdController.updateSerialConnectionStopbits(int(self.txtStopBits.text()))
        
        if self.checkYes.isChecked():
            self.__rfdController.updateSerialConnectionParity(serial.PARITY_EVEN)
        else:
            self.__rfdController.updateSerialConnectionParity(serial.PARITY_NONE)
        
        self.close()
    
    def __slotBtnCancel_Clicked(self):
        self.close()
    
