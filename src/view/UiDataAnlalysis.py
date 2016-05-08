import PyQt4.Qwt5
import Mapwidget
from PyQt4.Qt import QPalette, QColor, QPen
from PyQt4.QtCore import pyqtSlot
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
from PyQt4.Qwt5.qplt import SolidLine, DashDotDotLine
from PyQt4.Qwt5.Qwt import QwtPlotMarker, QwtText
from datetime import datetime
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

    graphClicked = PyQt4.QtCore.pyqtSignal(object)

    """
    #    Constructeur
    #    Description: Constructeur de la classe DataGraph
    #
    #    param: graphTitle: Titre du graphique
    #           xAxixTitle: Titre de laxe des x
    #           yAxisTitle: Titre de laxe des y
    #    return: None
    """
    def __init__(self, graphTitle, xAxisTitle, yAxisTitle, curveColor,row, column):


        PyQt4.Qwt5.Qwt.QwtPlot.__init__(self)
        self.xData = [0]
        self.yData = [0]
        self.__maxData = 0
        self.lastDataTimeStamp = None
        self.__isFullSize = False
        self.__row = row
        self.__column = column

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
        
        self.__maxValueMarker = QwtPlotMarker()
        self.__maxValueMarker.setLineStyle(QwtPlotMarker.HLine)
        self.__maxValueMarker.setLinePen(QPen(QColor(0,153,204),1.0,DashDotDotLine))
        self.__maxValueMarker.attach(self)
        
        self.curve = PyQt4.Qwt5.Qwt.QwtPlotCurve()
        self.curve.setPen(QPen(curveColor,2.0,SolidLine))
        self.curve.attach(self)
        self.replot()

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, row):
        self.__row = row

    @property
    def column(self):
        return self.__column

    @column.setter
    def column(self,column):
        self.__column = column

    @property
    def isFullSize(self):
        return self.__isFullSize

    @isFullSize.setter
    def isFullSize(self, state):
        self.__isFullSize = state

    def mousePressEvent(self, event):

        self.graphClicked.emit(self)

    def addData(self, value):

        xvalue = 0

        if self.lastDataTimeStamp is None:
            xvalue = 0
            self.lastDataTimeStamp = datetime.now()
        else:
            xvalue = float((datetime.now() - self.lastDataTimeStamp).seconds)

        if value > self.__maxData:
            self.__maxValueMarker.setLabel(QwtText("Peak: "+ str(value)))
            self.__maxValueMarker.setValue(xvalue,value)
            self.__maxData = value

        self.xData.append(xvalue)
        self.yData.append(value)
        self.curve.setData(self.xData, self.yData)
        self.replot()


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
        self.setGeometry(830,15,700,500)

        """Initialisation des differents graphiques realtime"""
        self.speedPlot = DataGraph("Speed over Time", "Time(SEC)","Speed(MPH)", QColor(255,0,0),0,0)
        self.accelPlot = DataGraph("Acceleration Over Time", "Time(SEC)","Accel.(MS2)",QColor(255,0,0),0,1)
        self.altitudePlot = DataGraph("Altitude over Time", "Time(SEC)","Alt.(x1000')",QColor(255,0,0),1,0)
        self.temperaturePlot = DataGraph("Temperature over Time", "Time(SEC)","Temp.(Celsius)",QColor(255,1,0),1,1)

        self.speedPlot.graphClicked.connect(self.updateDisplay)
        self.accelPlot.graphClicked.connect(self.updateDisplay)
        self.altitudePlot.graphClicked.connect(self.updateDisplay)
        self.temperaturePlot.graphClicked.connect(self.updateDisplay)

        """Ajout des widgets dans le frame selon un gridlayout"""
        self.addWidget(self.speedPlot, 0, 0)
        self.addWidget(self.accelPlot, 0, 1)
        self.addWidget(self.altitudePlot, 1, 0)
        self.addWidget(self.temperaturePlot, 1, 1)

    @property
    def graphList(self):
        return [self.speedPlot, self.accelPlot, self.altitudePlot, self.temperaturePlot]

    @pyqtSlot(object)
    def updateDisplay(self, clickedGraph):

        if not clickedGraph.isFullSize:
            for graph in self.graphList:
                if graph is not clickedGraph:
                    graph.hide()
            self.gridLayout.addWidget(graph,0,0,2,2)
            clickedGraph.isFullSize = True
        else:
            clickedGraph.isFullSize = False
            for graph in self.graphList:
                self.addWidget(graph, graph.row, graph.column)
                graph.show()


    def addAccelerationData(self, value):

        self.accelPlot.addData(value)

    def addTemperatureData(self, value):

        self.temperaturePlot.addData(value)

    def addSpeedData(self, value):

        self.speedPlot.addData(value)

    def addAltitudeData(self, value):

        self.altitudePlot.addData(value)
        
"""#
# La classe GPSTab
# Description:    Classe representant un frame contenant laffichage de la map GPS
#                 
#"""  
class GpsTab(DataFrame):
    
    def __init__(self, parent):
        
        """Initialisation de lobjet parent"""
        DataFrame.__init__(self, parent)
        self.setGeometry(120,15,700,500)
        """Initialisation de la map GPS"""
        #self.map = MapWidget.MapnikWidget(self)
        self.map = Mapwidget.Map(self)

        """Ouverture de la carte a afficher"""
        #self.map.open("Mapnik_Files/world_style.xml")
        
        """Ajout du widget au frame daffichage (objet courant(self))"""
        self.addWidget(self.map, 0, 0)
        self.show()
        
        