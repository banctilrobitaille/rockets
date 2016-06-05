import PyQt4
import serial
from serial.tools import list_ports


class SerialPropertiesWindow(PyQt4.QtGui.QWidget):
    def __init__(self, serialController, parent=None):

        PyQt4.QtGui.QWidget.__init__(self, parent)
        self.__serialController = serialController
        self.__setupUi()

    def __setupUi(self):

        self.setStyleSheet("QWidget {background: rgba(29,29,29,85);color : white; border: 0px;}"
                           "QComboBox {border: 1px;border-color: rgba(255,255,255);border-style: solid; color : "
                           "white; padding: 1px 0px 1px 3px;}"
                           "QPushButton { color : white; background : rgba(29,29,29,85); border: 1px;border-color: "
                           "rgba(255,255,255);border-style: solid;}"
                           "QPushButton:hover { color : rgba(29,29,29,100); background : white; border: "
                           "1px;border-color: black;border-style: solid;}"
                           "QLineEdit { color: white; background: rgba(29,29,29,85);border: 1px;border-color: rgba("
                           "255,255,255);border-style: solid;}")

        self.setObjectName("frmSerialProperties")
        self.setFixedSize(447, 192)
        self.setWindowTitle("Serial Connection Properties")

        self.btnCancel = PyQt4.QtGui.QPushButton(self)
        self.btnCancel.setGeometry(PyQt4.QtCore.QRect(210, 150, 93, 28))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setText("Cancel")

        self.btnSave = PyQt4.QtGui.QPushButton(self)
        self.btnSave.setGeometry(PyQt4.QtCore.QRect(320, 150, 93, 28))
        self.btnSave.setObjectName("btnSave")
        self.btnSave.setText("Save")

        self.gbConfig = PyQt4.QtGui.QGroupBox(self)
        self.gbConfig.setGeometry(PyQt4.QtCore.QRect(10, 10, 431, 131))
        self.gbConfig.setObjectName("gbConfig")
        self.gbConfig.setTitle("Serial Properties")

        self.comboCOMPort = PyQt4.QtGui.QComboBox(self.gbConfig)
        self.comboCOMPort.setGeometry(PyQt4.QtCore.QRect(190, 20, 191, 31))
        self.comboCOMPort.setObjectName("comboCOMPort")

        if self.__serialController.serialConnection.port is not None:

            for port in filter(lambda serialport: (serialport[0] !=
                    self.__serialController.serialConnection.port) and ("USB" in serialport[0]), list_ports.comports()):
                self.comboCOMPort.addItem(port[0])
            self.comboCOMPort.addItem(self.__serialController.serialConnection.port)
            self.comboCOMPort.setCurrentIndex(self.comboCOMPort.findText(self.__serialController.serialConnection.port))
        else:
            for port in list_ports.comports():
                self.comboCOMPort.addItem(port[0])

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

        if self.__serialController.serialConnection._parity != serial.PARITY_NONE:
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
        self.txtBaudRate.setText(str(self.__serialController.serialConnection._baudrate))

        self.lblStopBits = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblStopBits.setGeometry(PyQt4.QtCore.QRect(220, 90, 60, 22))
        self.lblStopBits.setObjectName("lblStopBits")
        self.lblStopBits.setText("StopBits:")

        self.txtStopBits = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtStopBits.setGeometry(PyQt4.QtCore.QRect(280, 90, 31, 22))
        self.txtStopBits.setObjectName("txtStopBits")
        self.txtStopBits.setText(str(self.__serialController.serialConnection._stopbits))

        self.lblDataBits = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblDataBits.setGeometry(PyQt4.QtCore.QRect(320, 90, 60, 22))
        self.lblDataBits.setObjectName("lblDataBits")
        self.lblDataBits.setText("DataBits:")

        self.txtDataBits = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtDataBits.setGeometry(PyQt4.QtCore.QRect(380, 90, 41, 22))
        self.txtDataBits.setObjectName("txtDataBits")
        self.txtDataBits.setText(str(self.__serialController.serialConnection._bytesize))

        PyQt4.QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()

    def __connectSlot(self):

        self.connect(self.btnCancel, PyQt4.QtCore.SIGNAL("clicked()"), self.__slotBtnCancel_Clicked)
        self.connect(self.btnSave, PyQt4.QtCore.SIGNAL("clicked()"), self.__slotBtnSave_Clicked)

    def __slotBtnSave_Clicked(self):

        if self.checkYes.isChecked():
            self.__serialController.updateSerialConnectionSettings(str(self.comboCOMPort.currentText()),
                                                                   int(self.txtBaudRate.text()),
                                                                   int(self.txtStopBits.text()),
                                                                   serial.PARITY_EVEN, int(self.txtDataBits.text()))
        else:
            self.__serialController.updateSerialConnectionSettings(str(self.comboCOMPort.currentText()),
                                                                   int(self.txtBaudRate.text()),
                                                                   int(self.txtStopBits.text()),
                                                                   serial.PARITY_NONE, int(self.txtDataBits.text()))
        self.close()

    def __slotBtnCancel_Clicked(self):
        self.close()
