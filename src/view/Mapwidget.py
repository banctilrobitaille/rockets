from mpl_toolkits.basemap import Basemap
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import PyQt4


class Map(PyQt4.QtGui.QWidget):

    def __init__(self, parent):

        super(Map, self).__init__(parent)

        self.__setupMap()

        self.__baseStationMarker = None
        self.__rocketMarker = None

        self.__baseStationMarkerLon = 0
        self.__baseStationMarkerLat = 0

        self.__rocketMarkerLon = 0
        self.__rocketMarketLat = 0

        self.__gpsFix = PyQt4.QtGui.QLabel("Invalid")
        #self.__gpsFix.setAlignment(PyQt4.QtCore.Qt.AlignLeft)
        self.__nbSatellite = PyQt4.QtGui.QLabel("0")
        #self.__nbSatellite.setAlignment(PyQt4.QtCore.Qt.AlignLeft)

        self.__addGPSInfo()
        self.show()



    @property
    def baseStationMarker(self):
        self.__baseStationMarker

    @baseStationMarker.setter
    def baseStationMarker(self,marker):
        self.__baseStationMarker = marker

    @property
    def rocketMarker(self):
        self.__baseStationMarker

    @rocketMarker.setter
    def rocketMarker(self,marker):
        self.__rocketMarker = marker

    @property
    def gpsFix(self):
        return self.__gpsFix

    @gpsFix.setter
    def gpsFix(self, gpsFix):
        self.__gpsFix.setText(gpsFix)

    @property
    def nbSatellite(self):
        return self.__nbSatellite

    @nbSatellite.setter
    def nbSatellite(self, nbSatellite):
        self.__nbSatellite.setText(str(nbSatellite))

    def __setupMap(self):

        self.fig = Figure(figsize=(12,12),frameon=False, tight_layout=False)
        self.axes = self.fig.add_axes([0,0,1,1])
        grid = np.random.rand(10, 10)
        self.canvas = FigureCanvas(self.fig)
        self.layout = PyQt4.QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.canvas)
        self.m = Basemap(width=6000000,height=4500000,projection='lcc',
            resolution=None,lat_0=46,lon_0=-71,ax=self.axes)
        self.m.shadedrelief()
        self.axes.imshow(grid,interpolation="quadric", aspect='auto')
        self.canvas.draw()

    def __addGPSInfo(self):

        satelliteIcon = PyQt4.QtGui.QLabel()
        #satelliteIcon.setAlignment(PyQt4.QtCore.Qt.AlignLeft)
        #satelliteIcon.setSizePolicy(PyQt4.QtGui.QSizePolicy.Expanding, PyQt4.QtGui.QSizePolicy.Expanding)
        satelliteIcon.setMinimumSize(32,32)
        satelliteIcon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/satellite.png'))

        fixIcon = PyQt4.QtGui.QLabel()
        #fixIcon.setAlignment(PyQt4.QtCore.Qt.AlignLeft)
        #fixIcon.setSizePolicy(PyQt4.QtGui.QSizePolicy.Expanding, PyQt4.QtGui.QSizePolicy.Expanding)
        fixIcon.setMinimumSize(32,32)
        fixIcon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/fix.png'))

        self.__gpsInfoFrame = PyQt4.QtGui.QFrame(self)
        self.__gpsInfoFrame.setGeometry(450,0,230,60)
        self.__gpsInfoFrame.setStyleSheet("QFrame {background : rgba(0,177,106,230)}"
                                          "QFrame QLabel {color: white;background : rgba(30,139,195,0);padding-top: 5px;"
                                          "padding-bottom: 5px;}")
        gpsInfoLayout = PyQt4.QtGui.QHBoxLayout()
        gpsInfoLayout.addWidget(satelliteIcon)
        gpsInfoLayout.addWidget(self.__nbSatellite)
        gpsInfoLayout.addWidget(fixIcon)
        gpsInfoLayout.addWidget(self.__gpsFix)
        self.__gpsInfoFrame.setLayout(gpsInfoLayout)
        self.__gpsInfoFrame.show()

    def updateBaseStationMarker(self, lon, lat):

        self.__baseStationMarkerLon = lon
        self.__baseStationMarkerLat = lat
        self.__updateMarkers()

    def updateRocketMarker(self,lon, lat):

        self.__rocketMarkerLon = lon
        self.__rocketMarketLat = lat
        self.__updateMarkers()

    def __updateMarkers(self):

        if self.__baseStationMarker is not None:
            self.__baseStationMarker[0].remove()

        if self.__rocketMarker is not None:
            self.__rocketMarker[0].remove()

        x,y = self.m(self.__baseStationMarkerLon,self.__baseStationMarkerLat)
        self.__baseStationMarker = self.m.plot(x,y, marker="D", markersize=10, color='b')

        x,y = self.m(self.__rocketMarkerLon,self.__rocketMarketLat)
        self.__rocketMarker = self.m.plot(x,y, marker="D", markersize=10, color='r')

        self.canvas.draw()
