import PyQt4
from PyQt4.Qt import QPalette, QColor, QFont
from PyQt4.Qwt5 import Qwt

"""#############################################################################
# 
# Nom du module:          dashboard
# Auteur:                 Benoit Anctil-Robitaille, Amine Waddah
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
        self.setGeometry(100,500,800,400)
        
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
        self.__lbl_speed.setGeometry(90, 65, 60,15)
        self.__speed_dial.setGeometry(30,100,175,175)
        self.__lcd_speed.setGeometry(50, 300, 130, 50)
        
        """Positionnement des elements daltitude"""
        self.__lbl_altitude.setGeometry(270, 25, 120,15)
        self.__altitude_dial.setGeometry(205,50,220,220)
        self.__lcd_altitude.setGeometry(250, 300, 130, 50)
         
        """Positionnement des elements dacceleration"""
        self.__lbl_acceleration.setGeometry(450, 65, 200,15)
        self.__acceleration_dial.setGeometry(425,100,175,175)
        self.__lcd_acceleration.setGeometry(455, 300, 130, 50)
        
        """Posiotionnement des elements thermometre"""
        self.__lbl_thermo.setGeometry(615, 65, 200,20)
        self.__rocketTemp.setGeometry(625, 90, 80, 195)
        self.__lcd_thermo.setGeometry(625, 300, 130, 50)

    """
    #    Methode updateValue
    #    Description: Permet de mettre a jour les valeurs affichees par les 
    #    composants graphiques du dashboard selon les valeurs en parametres
    #
    #    param: speed, accel, alti les nouvelles valeurs a afficher
    #    return: None
    """
    def updateValue(self,speed, acceleration, altitude, temperature):
        
        """Mise a jour des valeurs a afficher"""
        self.__speed_dial.setValue(speed)
        self.__acceleration_dial.setValue(acceleration)
        self.__altitude_dial.setValue(altitude)
        self.__rocketTemp.setValue(temperature)
        
        """Affichage des nouvelles valeurs"""
        self.__lcd_speed.display(str(speed))
        self.__lcd_acceleration.display(str(acceleration))
        self.__lcd_altitude.display(str(altitude))
        self.__lcd_thermo.display(str(temperature))
        
    def updateSpeed(self, speed):
        
        self.__speed_dial.setValue(speed)
        self.__lcd_speed.display(str(speed))
        
    def updateAcceleration(self, acceleration):
        
        self.__acceleration_dial.setValue(acceleration)
        self.__lcd_acceleration.display(str(acceleration))
        
    def updateAltitude(self, altitude):
        
        self.__altitude_dial.setValue(altitude)
        self.__lcd_altitude.display(str(altitude))
    
    def updateTemperature(self, temperature):
        
        self.__rocketTemp.updateValue(temperature)
        self.__lcd_thermo.display(str(temperature))

"""#
# La classe Speedometer
# Description:    Classe representant un cadrant qui affiche la vitesse de la fusee
#                 en temps reel
#"""
class SpeedoMeter(Qwt.QwtDial):
    
    """
    #    Constructeur
    #    Description: Constructeur de la classe Speedometer
    #
    #    param: label: le texte a afficher dans le cadran ex: MPH
    #           rangeMin: La valeur de depart du cadran
    #           rangeMax: La valeur maximale du cadran
    #           scaleMin: Pas de trace pour les petits traits
    #           scaleMid: Nombre de traits entre les grands traits
    #           scaleMax: Pas de trace pour les grand traits
    #
    #    return: None
    """
    def __init__(self, parent, label, rangeMin, rangeMax, scaleMin, scaleMid, scaleMax):
        
        Qwt.QwtDial.__init__(self, parent)
        
        """Initialisation du label affichant la metrique de mesure"""
        self.__label = label
        
        """Parametrage de la valeur minimum et maximum du cadran"""
        self.setRange(rangeMin, rangeMax) 
        self.setScale(scaleMin, scaleMid, scaleMax)
        self.setWrapping(False)
        self.setReadOnly(True)
        self.setOrigin(135.0)
        self.setLineWidth(2)
        self.palette = QPalette()
        self.palette.setColor(self.palette.Text, QColor(211,211,211))
        self.palette.setColor(self.palette.WindowText, QColor(55,55,55))
        self.palette.setColor(self.palette.Base, QColor(55,55,55))
        self.setPalette(self.palette)
        """Parametrage de la longueur d'arc en degre que parcourera l'aiguille"""
        self.setScaleArc(0.0, 270.0)
        self.setNeedle(Qwt.QwtDialSimpleNeedle(
            Qwt.QwtDialSimpleNeedle.Arrow,
            True,
            QColor(255,0,0),
            QColor(211,211,211)))
        self.setScaleOptions(Qwt.QwtDial.ScaleTicks | Qwt.QwtDial.ScaleLabel)
        self.show()
    
    """
    #    Methode drawScaleContent
    #    Description: Affichage de la metrique de mesure ex: MPH
    #
    #    param: painter: L'objet painter
    #           center: Le centre du cadran 
    #           radius: La rayon du cadran 
    #    return: None
    """           
    def drawScaleContents(self, painter, center, radius):
        
        rect = PyQt4.QtCore.QRect(50, 0, 2 * radius, 2 * radius - 10)
        rect.moveCenter(center)
        font = QFont("Arial", 15)
        painter.setPen(self.palette.color(self.palette.Text))
        painter.setFont(font)
        painter.drawText(
            rect, PyQt4.QtCore.Qt.AlignBottom | PyQt4.QtCore.Qt.AlignHCenter, self.__label)

"""#
# La classe DigitalNum
# Description:    Classe representant un affichage numerique. Celle ci sert
#                 sert a afficher les valeurs afficher par les cadrants de
#                 vitesse, acceleration, altitude, temperature etc.
#               
#"""
class DigitalNum(PyQt4.QtGui.QLCDNumber):
    
    """Palette de couleur verte"""
    lcd_palette = QPalette()   
    lcd_palette.setColor(lcd_palette.WindowText, PyQt4.QtGui.QColor(0, 255, 0))
    
    def __init__(self,parent, value):
        
        PyQt4.QtGui.QLCDNumber.__init__(self, parent)
        
        """Affectation de la palette de couleur a lobjet parent"""
        self.setPalette(self.lcd_palette)
        
        """Affichage du widget"""
        self.display(value)
        self.show()
        
    
"""#
# La classe Thermometer
# Description:    Classe representant un thermometre. Celle ci sert
#                 sert a afficher la temperature interne et/ou externe
#                 de la fusee
#               
#"""      
class Thermometer(Qwt.QwtThermo):
    
    """
    #    Constructeur
    #    Description: Constructeur de Thermometer
    #
    #    param: parent: L'objet parent (conteneur)
    #           minCelsius: Valeur minimum du thermometre en celsius
    #           maxCelsius: Valeur maximale du thermometre en celsius
    #           alarmLevel: Valeur a laquelle la couleur de linducateur change
    #    return: None
    """
    def __init__(self,parent, minCelsius, maxCelsius, alarmLevel):
        
        Qwt.QwtDial.__init__(self, parent)
        thermoPalette = QPalette()
        
        """Couleur des lignes indicatrices"""
        thermoPalette.setColor(thermoPalette.WindowText, PyQt4.QtGui.QColor(255, 255, 255))
        
        """Couleur des chiffres indicateurs"""
        thermoPalette.setColor(thermoPalette.Text,PyQt4.QtGui.QColor(255, 255, 255))
        
        """Couleur en dessous de la valeur alarmLevel"""
        thermoPalette.setColor(thermoPalette.ButtonText,PyQt4.QtGui.QColor(0, 255, 0))
        
        """Couleur sous la valeur alarmLevel"""
        thermoPalette.setColor(thermoPalette.Highlight,PyQt4.QtGui.QColor(0, 255, 0))
        
        thermoPalette.setColor(thermoPalette.Base,PyQt4.QtGui.QColor(0, 255, 0))
        
        """Application de la palette de couleur"""
        self.setPalette(thermoPalette)
        
        self.setAlarmColor(QColor(255,0,0))
        self.setFillColor(QColor(255,102,0))
        
        """Parametrage du niveau dalarme et de la graduation"""
        self.setAlarmLevel(alarmLevel)
        self.setAlarmEnabled(True)
        self.setRange(minCelsius, maxCelsius)
        self.setScale(minCelsius, maxCelsius)
        self.setValue(0)
        
        """Affichage de lobjet"""
        self.show()
    
    def updateValue(self, temperature):
        
        self.setValue(temperature)

"""#
# La classe Label
# Description:    Classe representant un label de blanche . Celle ci sert
#                 sert a afficher du texte.
#               
#"""
class Label(PyQt4.QtGui.QLabel):
    
    """Initialisation de la palette de couleur"""
    lbl_palette = QPalette()
    
    """La couleur du texte est blanche"""
    lbl_palette.setColor(lbl_palette.WindowText, PyQt4.QtGui.QColor(255, 255, 255))
    
    """
    #    Constructeur
    #    Description: Constructeur de Label
    #
    #    param: parent: L'objet parent (conteneur)
    #           text:   Le texte du label
    #    return: None
    """
    def __init__(self, parent, text):
        
        PyQt4.QtGui.QLabel.__init__(self, parent)
        self.setStyleSheet("""
        QLabel {
            font: 15pt;
        }
        """)
        self.setText(text)
        self.setPalette(self.lbl_palette)
        self.show()
    
