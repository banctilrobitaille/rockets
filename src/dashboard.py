import PyQt4
from PyQt4.Qt import QPalette
from PyQt4.Qwt5 import Qwt

"""#############################################################################
# 
# Nom du module:          dashboard
# Auteur:                 Benoit Anctil-Robitaille
# Date:                   8 Septembre 2015
# Description:            Le module dashboard.py regroupe les classes necessaires
#                         a laffichage des donnees de vols en temps reel telles
#                         que les classes Speedometer, DigitalNum et Thermometer.
#
##############################################################################"""

"""#
# La classe dashboard
# Description:    Classe representant un dashboard affichant les donnnees de
#                 de vol en temps reel. L'initialisation des composants du 
#                 dashboard et leur affichage se font dans cette classe.
#"""
class Dashboard(PyQt4.QtGui.QFrame):
    
    
    def __init__(self, parent):
        
        PyQt4.QtGui.QFrame.__init__(self, parent)
        
        """Positionnement du frame du dashboard"""
        self.setGeometry(0,360,600,300)
        
        """Initialisation du cadran de la vitesse, du cadran numerique et label descriptif"""
        self.__lbl_speed = Label(self, "SPEED")
        self.__speed_dial = SpeedoMeter(self,"MPH",0.0,700.0,0,3,100)
        self.__lcd_speed = DigitalNum(self, 0)
        
        """Initilisation du cadran de laltitude, du cadran numerique et label descriptif"""
        self.__lbl_altitude = Label(self, "ALTITUDE")
        self.__altitude_dial = SpeedoMeter(self,"x1000''",0.0,27.0,0,0,2)
        self.__lcd_altitude = DigitalNum(self, 0)
        
        """Initialisation du cadran de lacceleration, du cadran numerique et label descriptif"""
        self.__lbl_acceleration = Label(self, "ACCELERATION")
        self.__acceleration_dial = SpeedoMeter(self,"M/S2",0.0,200.0,0,5,50)
        self.__lcd_acceleration = DigitalNum(self, 0)
        
        """Initialisation du cadran numerique et label descriptif"""
        self.__lbl_thermo = Label(self, "TEMPERATURE")
        self.__rocketTemp = Thermometer(self, 0, 100, 70)
        self.__lcd_thermo = DigitalNum(self, 0)
        
        """Positionnement des elements"""
        self.placeTheElement()
        
        """Affichage des elements"""
        self.show()
    
    
    """
    #    Methode placeTheElement
    #    Description: Positionne les elements du dashboard selon des
    #    coordonnees fixes et absolues
    #
    #    param: None
    #    return: None
    """
    def placeTheElement(self):
        
        """Positionnement des elements de vitesse"""
        self.__lbl_speed.setGeometry(60, 15, 60,20)
        self.__speed_dial.setGeometry(20,40,130,130)
        self.__lcd_speed.setGeometry(35, 180, 100, 30)
        
        """Positionnement des elements daltitude"""
        self.__lbl_altitude.setGeometry(190, 15, 70,20)
        self.__altitude_dial.setGeometry(160,40,130,130)
        self.__lcd_altitude.setGeometry(175, 180, 100, 30)
         
        """Positionnement des elements dacceleration"""
        self.__lbl_acceleration.setGeometry(315, 15, 120,20)
        self.__acceleration_dial.setGeometry(300,40,130,130)
        self.__lcd_acceleration.setGeometry(315, 180, 100, 30)
        
        """Posiotionnement des elements thermometre"""
        self.__lbl_thermo.setGeometry(455, 15, 200,20)
        self.__rocketTemp.setGeometry(470, 40, 60, 130)
        self.__lcd_thermo.setGeometry(455, 180, 100, 30)

    """
    #    Methode updateValue
    #    Description: Permet de mettre a jour les valeurs affichees par les 
    #    composants graphiques du dashboard selon les valeurs en parametres
    #
    #    param: None
    #    return: None
    """
    def updateValue(self,speed, accel, alti):
        
        """Mise a jour des valeurs a afficher"""
        self.__speed_dial.setValue(speed)
        self.__acceleration_dial.setValue(accel)
        self.__altitude_dial.setValue(alti)
        
        """Affichage des nouvelles valeurs"""
        self.__lcd_speed.display(str(speed))
        self.__lcd_acceleration.display(str(accel))
        self.__lcd_altitude.display(str(alti)) 
    

        
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
