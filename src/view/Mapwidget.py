import PyQt4

import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
from controller.GeoTrackingUtils import GeoTrackingUtil

from UICompass import Compass


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
        self.__nbSatellite = PyQt4.QtGui.QLabel("0")

        self.__addGPSInfo()
        self.__addGeoTrackingInfo()
        self.__addCompass()
        self.show()

    @property
    def baseStationMarker(self):
        self.__baseStationMarker

    @baseStationMarker.setter
    def baseStationMarker(self, marker):
        self.__baseStationMarker = marker

    @property
    def rocketMarker(self):
        self.__baseStationMarker

    @rocketMarker.setter
    def rocketMarker(self, marker):
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

        self.fig = Figure(figsize=(12, 12), frameon=False, tight_layout=False)
        self.axes = self.fig.add_axes([0, 0, 1, 1])
        self.grid = np.random.rand(10, 10)
        self.canvas = FigureCanvas(self.fig)
        self.layout = PyQt4.QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.canvas)
        self.m = Basemap(width=6000000, height=4500000, projection='lcc',
                         resolution=None, lat_0=45, lon_0=-73, ax=self.axes)
        self.m.shadedrelief()
        self.axes.imshow(self.grid, interpolation="quadric", aspect='auto')
        self.canvas.draw()

    def __addGPSInfo(self):

        satelliteIcon = PyQt4.QtGui.QLabel()
        satelliteIcon.setMinimumSize(32, 32)
        satelliteIcon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/satellite.png'))

        fixIcon = PyQt4.QtGui.QLabel()
        fixIcon.setMinimumSize(32, 32)
        fixIcon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/fix.png'))

        self.__gpsInfoFrame = PyQt4.QtGui.QFrame(self)
        self.__gpsInfoFrame.setGeometry(450, 0, 230, 60)
        self.__gpsInfoFrame.setStyleSheet("QFrame {background : rgba(0,177,106,230)}"
                                          "QFrame QLabel {color: white;background : rgba(30,139,195,0);padding-top: "
                                          "5px;"
                                          "padding-bottom: 5px;}")
        gpsInfoLayout = PyQt4.QtGui.QHBoxLayout()
        gpsInfoLayout.addWidget(satelliteIcon)
        gpsInfoLayout.addWidget(self.__nbSatellite)
        gpsInfoLayout.addWidget(fixIcon)
        gpsInfoLayout.addWidget(self.__gpsFix)
        self.__gpsInfoFrame.setLayout(gpsInfoLayout)
        self.__gpsInfoFrame.show()

    def __addGeoTrackingInfo(self):

        self.geoTrackingInfosFrame = PyQt4.QtGui.QFrame(self)
        self.geoTrackingInfosFrame.setGeometry(0, 430, 500, 60)
        self.geoTrackingInfosFrame.setStyleSheet("QFrame {background : transparent}"
                                                 "QFrame QLabel {color: black;background : rgba(30,139,195,"
                                                 "0);padding-top: "
                                                 "5px;"
                                                 "padding-bottom: 5px;}")
        geoTrackingInfoLayout = PyQt4.QtGui.QHBoxLayout()
        geoTrackingInfoLayout.addWidget(PyQt4.QtGui.QLabel("Rocket Long.: {}".format(self.__rocketMarkerLon)))
        geoTrackingInfoLayout.addWidget(PyQt4.QtGui.QLabel("Rocket Lat.: {}".format(self.__rocketMarketLat)))
        geoTrackingInfoLayout.addWidget(PyQt4.QtGui.QLabel("Distance: {}KM".format(
            str(GeoTrackingUtil.distanceBetweenCoordinates({'longitude': self.__baseStationMarkerLon,
                                                            'latitude' :
                                                                self.__baseStationMarkerLat},
                                                           {'longitude': self.__rocketMarkerLon,
                                                            'latitude' :
                                                                self.__rocketMarketLat})))))
        geoTrackingInfoLayout.addWidget(PyQt4.QtGui.QLabel("Bearing: {}Degrees".format(
            str(GeoTrackingUtil.bearingFromCoordinates({'longitude': self.__baseStationMarkerLon,
                                                            'latitude' :
                                                                self.__baseStationMarkerLat},
                                                           {'longitude': self.__rocketMarkerLon,
                                                            'latitude' :
                                                                self.__rocketMarketLat})))))
        self.geoTrackingInfosFrame.setLayout(geoTrackingInfoLayout)
        self.geoTrackingInfosFrame.show()

    def __addCompass(self):
        self.__compass = Compass(self)

    def updateBaseStationMarker(self, lon, lat):

        self.__baseStationMarkerLon = lon
        self.__baseStationMarkerLat = lat
        self.__updateMarkers()

    def updateRocketMarker(self, lon, lat):

        print lon
        print lat
        self.__rocketMarkerLon = lon
        self.__rocketMarketLat = lat
        self.__updateMarkers()

    def __updateMarkers(self):

        if self.__baseStationMarker is not None:
            self.__baseStationMarker[0].remove()

        if self.__rocketMarker is not None:
            self.__rocketMarker[0].remove()

        x, y = self.m(self.__baseStationMarkerLon, self.__baseStationMarkerLat)
        self.__baseStationMarker = self.m.plot(x, y, marker="D", markersize=10, color='b')

        x, y = self.m(self.__rocketMarkerLon, self.__rocketMarketLat)
        self.__rocketMarker = self.m.plot(x, y, marker="D", markersize=10, color='r')

        self.__updateCompass()

        self.canvas.draw()

    def __updateCompass(self):
        self.__compass.setValue(GeoTrackingUtil.bearingFromCoordinates({'longitude': self.__baseStationMarkerLon,
                                                                        'latitude' : self.__baseStationMarkerLat},
                                                                       {'longitude': self.__rocketMarkerLon,
                                                                        'latitude' : self.__rocketMarketLat}))
