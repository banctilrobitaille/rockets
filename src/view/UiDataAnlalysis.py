import PyQt4.Qwt5
import MapWidget
from PyQt4.Qt import QPalette, QColor
"""#############################################################################
# 
# Nom du module:          UiDataAnalysis
# Auteur:                 Benoit Anctil-Robitaille, Amine Waddah
# Date:                   8 Septembre 2015
# Description:            Le module UiDataAnalysis.py regroupe les classes necessaires
#                         a laffichage des composants danalyse de donnees en temps reel
#                         tels que les graphiques et laffichage des coordonnees GPS.
#
##############################################################################"""

"""#
# La classe DataFrame
# Description:    Classe representant un frame contenant des widgets quelconque
#"""
class DataFrame(PyQt4.QtGui.QFrame):
    
    def __init__(self, parent):
        
        PyQt4.QtGui.QFrame.__init__(self, parent)
        self.gridLayout = PyQt4.QtGui.QGridLayout()
        self.setLineWidth(3)
        self.setFrameStyle(PyQt4.QtGui.QFrame.Panel | PyQt4.QtGui.QFrame.Raised)
    
    def addWidget(self,widget, xGridPosition, yGridPosition):
        
        self.gridLayout.addWidget(widget, xGridPosition, yGridPosition)
        self.setLayout(self.gridLayout)

"""#
# La classe DataGraph
# Description:    Classe representant un graphique. Cette classe est utilisee
#                 pour afficher en temps reel des statistique sous forme de graphique
#                 telle que la vitesse en fonction du temps, laltitude en fonction du 
#                 temps, lacceleration en fonction du temps, etc.
#"""   
class DataGraph(PyQt4.Qwt5.Qwt.QwtPlot):

    """
    #    Constructeur
    #    Description: Constructeur de la classe DataGraph
    #
    #    param: graphTitle: Titre du graphique
    #           xAxixTitle: Titre de laxe des x
    #           yAxisTitle: Titre de laxe des y
    #    return: None
    """
    def __init__(self, graphTitle, xAxisTitle, yAxisTitle):
        
        PyQt4.Qwt5.Qwt.QwtPlot.__init__(self)
        
        self.setCanvasBackground(QColor(45,45,45))
        self.palette = QPalette()
        self.palette.setColor(self.palette.Text, QColor(245,245,245))
        self.setPalette(self.palette)
        """Parametrage de la police daffichage des titres des axes du graphique"""
        self.plotTitleFont = PyQt4.QtGui.QFont("Helvetica", 15)
        self.plotAxisFont = PyQt4.QtGui.QFont("Helvetica", 15)
        
        """Affectation des titres aux differents axes"""
        self.setGraphTitle(graphTitle, self.plotTitleFont)
        self.setXAxisTitle(xAxisTitle, self.plotAxisFont)
        self.setYAxisTitle(yAxisTitle, self.plotAxisFont)
        
    """
    #    Methode setGraphTitle
    #    Description: Methode affectant un titre au graphique
    #
    #    param: graphTitle: Titre du graphique
    #           font:       Police daffichage du titre
    #    return: None
    """        
    def setGraphTitle(self,graphTitle, font):
        
        self.graphTitle = PyQt4.Qwt5.Qwt.QwtText(graphTitle)
        self.graphTitle.setFont(self.plotTitleFont)
        self.setTitle(self.graphTitle)
    
    """
    #    Methode setXAxisTitle
    #    Description: Methode affectant un titre a laxe des ordones
    #
    #    param: xAxisTitle: Titre de laxe des ordones
    #           font:       Police daffichage du titre
    #    return: None
    """       
    def setXAxisTitle(self,xAxisTitle, font):
        
        self.xAxisTitle = PyQt4.Qwt5.Qwt.QwtText(xAxisTitle)
        self.xAxisTitle.setFont(font)
        self.setAxisTitle(2, self.xAxisTitle)

    """
    #    Methode setYAxisTitle
    #    Description: Methode affectant un titre a laxe des abscisses
    #
    #    param: yAxisTitle: Titre de laxe des abscisses
    #           font:       Police daffichage du titre
    #    return: None
    """    
    def setYAxisTitle(self,yAxisTitle, font):
        
        self.yAxisTitle = PyQt4.Qwt5.Qwt.QwtText(yAxisTitle)
        self.yAxisTitle.setFont(font)
        self.setAxisTitle(0, self.yAxisTitle)
        
"""#
# La classe GraphTab
# Description:    Classe representant un frame contenant les differents graphiques
#                 daffichage.
#"""  
class GraphTab(DataFrame):
    
    def __init__(self, parent):
        
        """Initialiation de lobjet parent"""
        DataFrame.__init__(self,parent)
        
        self.setGeometry(930,15,900,600)
        """Initialisation des differents graphiques realtime"""
        self.speedPlot = DataGraph("Speed over Time", "Time(SEC)","Speed(MPH)")
        self.accelPlot = DataGraph("Acceleration Over Time", "Time(SEC)","Accel.(MS2)")
        self.altitudePlot = DataGraph("Altitude over Time", "Time(SEC)","Alt.(x1000')")
        self.temperaturePlot = DataGraph("Temperature over Time", "Time(SEC)","Temp.(KELVIN)")
        
        """Ajout des widgets dans le frame selon un gridlayout"""
        self.addWidget(self.speedPlot, 0, 0)
        self.addWidget(self.accelPlot, 0, 1)
        self.addWidget(self.altitudePlot, 1, 0)
        self.addWidget(self.temperaturePlot, 1, 1)
        
        
"""#
# La classe GPSTab
# Description:    Classe representant un frame contenant laffichage de la map GPS
#                 
#"""  
class GpsTab(DataFrame):
    
    def __init__(self, parent):
        
        """Initialisation de lobjet parent"""
        DataFrame.__init__(self, parent)
        self.setGeometry(20,15,900,600)
        """Initialisation de la map GPS"""
        self.map = MapWidget.MapnikWidget(self)
        
        """Ouverture de la carte a afficher"""
        self.map.open("Mapnik_Files/world_style.xml")
        
        """Ajout du widget au frame daffichage (objet courant(self))"""
        self.addWidget(self.map, 0, 0)
        self.show()
        
        