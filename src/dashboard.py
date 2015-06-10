import PyQt4
from PyQt4.Qt import QPalette
from PyQt4.Qwt5 import Qwt


###DEBUT DE LA CLASSE Dashboard###
class Dashboard(PyQt4.QtGui.QFrame):
    
    
    def __init__(self, parent):
        
        PyQt4.QtGui.QFrame.__init__(self, parent)
        
        self.setGeometry(0,0,600,300)
        
        self.__lbl_speed = Label(self, "SPEED")
        self.__speed_dial = SpeedoMeter(self,"MPH",0.0,700.0,0,3,100)
        self.__lcd_speed = DigitalNum(self, 0)
        
        self.__lbl_altitude = Label(self, "ALTITUDE")
        self.__altitude_dial = SpeedoMeter(self,"x1000''",0.0,27.0,0,0,2)
        self.__lcd_altitude = DigitalNum(self, 0)
        
        self.__lbl_acceleration = Label(self, "ACCELERATION")
        self.__acceleration_dial = SpeedoMeter(self,"M/S2",0.0,200.0,0,5,50)
        self.__lcd_acceleration = DigitalNum(self, 0)
        
        self.__lbl_thermo = Label(self, "TEMPERATURE")
        self.__rocketTemp = Thermometer(self, 0, 100, 70)
        self.__lcd_thermo = DigitalNum(self, 0)
        
        self.placeTheElement()
        self.show()
    
    
    def placeTheElement(self):
        
        self.__lbl_speed.setGeometry(100, 15, 60,20)
        self.__speed_dial.setGeometry(60,40,130,130)
        self.__lcd_speed.setGeometry(75, 180, 100, 30)
        
        self.__lbl_altitude.setGeometry(230, 15, 70,20)
        self.__altitude_dial.setGeometry(200,40,130,130)
        self.__lcd_altitude.setGeometry(215, 180, 100, 30)
         
        self.__lbl_acceleration.setGeometry(350, 15, 120,20)
        self.__acceleration_dial.setGeometry(340,40,130,130)
        self.__lcd_acceleration.setGeometry(355, 180, 100, 30)
        
        self.__lbl_thermo.setGeometry(495, 15, 200,20)
        self.__rocketTemp.setGeometry(510, 40, 60, 130)
        self.__lcd_thermo.setGeometry(495, 180, 100, 30)
            
    def updateValue(self,speed, accel, alti):
        
        self.__speed_dial.setValue(speed)
        self.__acceleration_dial.setValue(accel)
        self.__altitude_dial.setValue(alti)
        self.__lcd_speed.display(str(speed))
        self.__lcd_acceleration.display(str(accel))
        self.__lcd_altitude.display(str(alti)) 
    
###FIN DE LA CLASSE Dashboard###

        
###DEBUT DE LA CLASSE SpeedoMEter###
class SpeedoMeter(Qwt.QwtDial):

    def __init__(self, parent, label, rangeMin, rangeMax, scaleMin, scaleMid, scaleMax):
        
        Qwt.QwtDial.__init__(self, parent)
        self.__label = label
        self.setRange(rangeMin, rangeMax)
        self.setScale(scaleMin, scaleMid, scaleMax)
        self.setWrapping(False)
        self.setReadOnly(True)
        self.setOrigin(135.0)
        self.setScaleArc(0.0, 270.0)
        self.setNeedle(Qwt.QwtDialSimpleNeedle(
            Qwt.QwtDialSimpleNeedle.Arrow,
            True,
            PyQt4.QtGui.QColor(PyQt4.QtGui.QColor.red),
            PyQt4.QtGui.QColor(PyQt4.QtGui.QColor.blue).light(130)))
        self.setScaleOptions(Qwt.QwtDial.ScaleTicks | Qwt.QwtDial.ScaleLabel)
        self.show()

            
    def drawScaleContents(self, painter, center, radius):
        
        painter.setPen(PyQt4.Qt.QPen(PyQt4.QtGui.QColor(245,245,245), 3))
        rect = PyQt4.QtCore.QRect(50, 0, 2 * radius, 2 * radius - 10)
        rect.moveCenter(center)
        painter.setPen(self.palette().color(PyQt4.QtGui.QPalette.Text))
        painter.drawText(
            rect, PyQt4.QtCore.Qt.AlignBottom | PyQt4.QtCore.Qt.AlignHCenter, self.__label)

###FIN DE LA CLASSE SpeedoMeter###


###DEBUT DE LA CLASSE DigitalNum###
class DigitalNum(PyQt4.QtGui.QLCDNumber):
    
    lcd_palette = QPalette()   
    lcd_palette.setColor(lcd_palette.WindowText, PyQt4.QtGui.QColor(0, 255, 0))
    
    def __init__(self,parent, value):
        
        PyQt4.QtGui.QLCDNumber.__init__(self, parent)
        
        self.setPalette(self.lcd_palette)
        self.display(value)
        self.show()
    
###FIN DE LA CLASSE DigitalMum###

#class BatteryBar(PyQt4.QtGui.QProgressBar):
    #def createProgressBar(self):
        
class Thermometer(Qwt.QwtThermo):
    
    def __init__(self,parent, minCelsius, maxCelsius, alarmLevel):
        
        Qwt.QwtDial.__init__(self, parent)
        thermoPalette = QPalette()
        thermoPalette.setColor(thermoPalette.WindowText, PyQt4.QtGui.QColor(255, 255, 255))
        thermoPalette.setColor(thermoPalette.Text,PyQt4.QtGui.QColor(255, 255, 255))
        thermoPalette.setColor(thermoPalette.ButtonText,PyQt4.QtGui.QColor(0, 255, 0))
        thermoPalette.setColor(thermoPalette.Highlight,PyQt4.QtGui.QColor(0, 255, 0))
        self.setPalette(thermoPalette)
        self.setAlarmLevel(alarmLevel)
        self.setRange(minCelsius, maxCelsius)
        self.setScale(minCelsius, maxCelsius)
        self.setValue(95)
        self.show

##DEBUT DE LA CLASSE Label###
class Label(PyQt4.QtGui.QLabel):
    
    lbl_palette = QPalette()
    lbl_palette.setColor(lbl_palette.WindowText, PyQt4.QtGui.QColor(255, 255, 255))
    
    def __init__(self, parent, text):
        
        PyQt4.QtGui.QLabel.__init__(self, parent)
        self.setText(text)
        self.setPalette(self.lbl_palette)
        self.show()
    
###FIN DE LA CLASSE Label###
