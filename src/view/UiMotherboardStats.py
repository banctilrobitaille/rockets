import PyQt4
from view.dashboard import Thermometer

class MotherboardStats(PyQt4.QtGui.QWidget):

    def __init__(self):
        super(MotherboardStats,self).__init__(None)

        self.__setupUI()

        self.__lblTitle = PyQt4.QtGui.QLabel("TEMPERATURE SENSORS")
        self.__lblTitle.fontChange(PyQt4.Qt.QFont("Arial",20))
        self.__lblTitle.setAlignment(PyQt4.QtCore.Qt.AlignLeft)
        self.__layout = PyQt4.QtGui.QVBoxLayout()
        self.__layout.addWidget(self.__lblTitle,0)
        self.__layout.addWidget(MotherboardFrame(self),1)
        self.__layout.addWidget(ThermometerFrame(self),1)
        self.setLayout(self.__layout)
        self.show()

    def __setupUI(self):

        self.setGeometry(300,300,1000,600)
        self.setWindowTitle("PCB Stats")
        self.setStyleSheet("QWidget {background-color: black; color: white}")


class MotherboardFrame(PyQt4.QtGui.QFrame):

    def __init__(self, parent):
        super(MotherboardFrame, self).__init__(parent)
        self.setStyleSheet("QFrame {background-image: url(./Image_Files/motherboard.png);"
                           " background-repeat: no-repeat}")
        self.sensorLed = {

            TemperatureSensorLed(self,100,50),
            TemperatureSensorLed(self,205,120),
            TemperatureSensorLed(self,310,150),
            TemperatureSensorLed(self,470,150),
            TemperatureSensorLed(self,625,120),
            TemperatureSensorLed(self,720,120),
            TemperatureSensorLed(self,812,120),
            TemperatureSensorLed(self,895,30),
        }

        self.show()


class TemperatureSensorLed(PyQt4.QtGui.QWidget):

    SIZE = 40

    STATUS = {
        'GOOD'      : "GOOD",
        'WARNING'   : "WARNING",
        'CRITICAL'  : "CRITICAL",
    }

    COLOR = {

        'GOOD'      : PyQt4.Qt.QColor(0,255,0),
        'WARNING'   : PyQt4.Qt.QColor(255,69,0),
        'CRITICAL'  : PyQt4.Qt.QColor(255,0,0),

    }

    def __init__(self, parent, x, y, status="GOOD"):
        super(TemperatureSensorLed, self).__init__(parent)

        self.__status = status
        self.__updateColor()
        self.setGeometry(x,y,self.SIZE,self.SIZE)


    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    def __updateColor(self):
        self.setColor(self.COLOR[self.__status])

    def paintEvent(self, event):
        paint = PyQt4.QtGui.QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(PyQt4.QtGui.QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(PyQt4.QtGui.Qt.white)
        paint.drawRect(event.rect())
        # for circle make the ellipse radii match
        radx = 100
        rady = 100
        # draw red circles
        paint.setPen(PyQt4.QtGui.Qt.red)
        for k in range(125, 220, 10):
            center = PyQt4.QtGui.QPoint(k, k)
            # optionally fill each circle yellow
            paint.setBrush(PyQt4.QtGui.Qt.yellow)
            paint.drawEllipse(center, radx, rady)
        paint.end()


class ThermometerFrame(PyQt4.QtGui.QFrame):

    def __init__(self, parent):
        super(ThermometerFrame, self).__init__(parent)

        self.__layout = PyQt4.QtGui.QHBoxLayout()

        self.__label = [

            PyQt4.QtGui.QLabel("Switch #1"),
            PyQt4.QtGui.QLabel("Switch #2"),
            PyQt4.QtGui.QLabel("Stratologger"),
            PyQt4.QtGui.QLabel("RFD900"),
            PyQt4.QtGui.QLabel("PCB Parachute"),
            PyQt4.QtGui.QLabel("PCB Temperature"),
            PyQt4.QtGui.QLabel("Station inertielle"),
            PyQt4.QtGui.QLabel("Switch #3"),
        ]

        self.__thermometers = [

            Thermometer(self,0,100,60),
            Thermometer(self,0,100,60),
            Thermometer(self,0,100,60),
            Thermometer(self,0,100,60),
            Thermometer(self,0,100,60),
            Thermometer(self,0,100,60),
            Thermometer(self,0,100,60),
            Thermometer(self,0,100,60),
        ]

        for i in range(0, len(self.__thermometers)):

            thermometerSensor = PyQt4.QtGui.QFrame()
            layout = PyQt4.QtGui.QVBoxLayout()
            self.__label[i].setAlignment(PyQt4.QtCore.Qt.AlignCenter)
            layout.addWidget(self.__label[i],0)
            layout.addWidget(self.__thermometers[i],1)
            thermometerSensor.setLayout(layout)
            self.__layout.addWidget(thermometerSensor)

        self.setLayout(self.__layout)

    @property
    def thermometers(self):
        return self.__thermometers
