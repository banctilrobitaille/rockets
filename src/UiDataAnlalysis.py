import PyQt4.Qwt5
import MapWidget

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
    
    def __init__(self):
        
        PyQt4.QtGui.QFrame.__init__(self)
        self.gridLayout = PyQt4.QtGui.QGridLayout()
    
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
        
        """Parametrage de la police daffichage des titres des axes du graphique"""
        self.plotTitleFont = PyQt4.QtGui.QFont("Helvetica", 11)
        self.plotAxisFont = PyQt4.QtGui.QFont("Helvetica", 8)
        
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
        
        
class GraphTab(DataFrame):
    
    def __init__(self):
        
        DataFrame.__init__(self)

        self.speedPlot = DataGraph("Speed over Time", "Time(SEC)","Speed(MPH)")
        self.accelPlot = DataGraph("Acceleration Over Time", "Time(SEC)","Accel.(MS2)")
        self.altitudePlot = DataGraph("Altitude over Time", "Time(SEC)","Alt.(x1000')")
        self.temperaturePlot = DataGraph("Temperature over Time", "Time(SEC)","Temp.(KELVIN)")
        
        self.addWidget(self.speedPlot, 0, 0)
        self.addWidget(self.accelPlot, 0, 1)
        self.addWidget(self.altitudePlot, 1, 0)
        self.addWidget(self.temperaturePlot, 1, 1)
        
        
class GpsTab(DataFrame):
    
    def __init__(self):
        
        DataFrame.__init__(self)

        self.map = MapWidget.MapnikWidget(self)
        self.map.open("world_style.xml")
        self.addWidget(self.map, 0, 0)
        
        