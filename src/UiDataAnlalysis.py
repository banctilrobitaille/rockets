import PyQt4.Qwt5
import MapWidget
        
class DataFrame(PyQt4.QtGui.QFrame):
    
    def __init__(self):
        
        PyQt4.QtGui.QFrame.__init__(self)
        self.gridLayout = PyQt4.QtGui.QGridLayout()
    
    def addWidget(self,widget, xGridPosition, yGridPosition):
        
        self.gridLayout.addWidget(widget, xGridPosition, yGridPosition)
        self.setLayout(self.gridLayout)
        
class DataGraph(PyQt4.Qwt5.Qwt.QwtPlot):
    
    def __init__(self, graphTitle, xAxisTitle, yAxisTitle):
        
        PyQt4.Qwt5.Qwt.QwtPlot.__init__(self)
        
        self.plotTitleFont = PyQt4.QtGui.QFont("Helvetica", 11)
        self.plotAxisFont = PyQt4.QtGui.QFont("Helvetica", 8)
        
        self.setGraphTitle(graphTitle, self.plotTitleFont)
        self.setXAxisTitle(xAxisTitle, self.plotAxisFont)
        self.setYAxisTitle(yAxisTitle, self.plotAxisFont)
        
        
    def setGraphTitle(self,graphTitle, font):
        
        self.graphTitle = PyQt4.Qwt5.Qwt.QwtText(graphTitle)
        self.graphTitle.setFont(self.plotTitleFont)
        self.setTitle(self.graphTitle)
        
    def setXAxisTitle(self,xAxisTitle, font):
        
        self.xAxisTitle = PyQt4.Qwt5.Qwt.QwtText(xAxisTitle)
        self.xAxisTitle.setFont(font)
        self.setAxisTitle(2, self.xAxisTitle)
        
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

        self.__map = MapWidget.MapnikWidget(self)
        self.__map.open("world_style.xml")
        self.addWidget(self.__map, 0, 0)
        
        